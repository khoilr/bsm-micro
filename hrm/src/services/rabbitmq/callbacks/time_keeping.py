import json
import os
import uuid
from datetime import datetime, timedelta, timezone

import pika
import requests
from dotenv import load_dotenv

from src.database.dao.employee import Employee as EmployeeDAO
from src.database.dao.time import Time as TimeDAO
from src.database.models.employee import Employee as EmployeeModel
from src.database.models.time import Time as TimeModel
from src.logger import logger

load_dotenv()
hrm_exchange = os.environ.get("HRM_EXCHANGE", "hrm_exchange")


def publish(ch, data):
    ch.basic_publish(
        exchange=hrm_exchange,
        routing_key="",
        body=json.dumps(data),
        properties=pika.BasicProperties(
            delivery_mode=pika.DeliveryMode.Persistent,
        ),
    )
    logger.info(" [x] Sent message to telegram notification queue")


def get_employee(_id: str, name: str):
    url = "http://103.157.218.115/HRM/hs/HRM/V1/AllEmployee"
    basic_auth = ("LongPT", "123456")

    response = requests.get(url, auth=basic_auth, timeout=10)
    response_json = response.json()["Information"]

    employees = list(filter(lambda x: x["Description"] == name, response_json))

    if len(employees) == 0:
        return None

    employee = EmployeeDAO.get_or_create(
        id=uuid.UUID(_id),
        hrm_id=employees[0]["Code"],
        name=employees[0]["Description"],
    )
    return employee


def checkin(employee: EmployeeModel, img: str, ch):
    url = "http://103.157.218.115/HRM/hs/HRM/v1/CheckInCam"
    payload = {"EmployeeID": employee.hrm_id}
    basic_auth = ("Administrator", "")

    response = requests.post(url, auth=basic_auth, json=payload, timeout=10)

    if response.status_code != 200:
        logger.error("Error while checkin")
        return None

    response_json = response.json()
    checkin_at = datetime.strptime(response_json["Checkin"], "%d.%m.%Y %H:%M:%S")

    time = TimeDAO.create(
        id=response_json["Number"],
        employee=employee,
        checkin_at=checkin_at,
        checkin_img=img,
    )

    logger.info(f"{employee.name} checked in at {checkin_at}")

    publish(ch, time.to_dict())

    return time


def checkout(time: TimeModel, img: str, ch) -> TimeModel:
    url = "http://103.157.218.115/HRM/hs/HRM/v1/CkeckOutCam"
    payload = {"Number": time.id}
    basic_auth = ("Administrator", "")

    response = requests.post(url, auth=basic_auth, json=payload, timeout=10)

    if response.status_code != 200:
        logger.error("Error while checkout")
        return None

    response_json = response.json()
    checkout_at = datetime.strptime(response_json["Checkout"], "%d.%m.%Y %H:%M:%S")

    time = TimeDAO.update(
        time,
        checkout_at=checkout_at,
        completed=True,
        checkout_img=img,
    )

    logger.info(f"{time.employee.name} checked out at {checkout_at}")

    publish(ch, time.to_dict())

    return time


def callback(ch, method, properties, body):
    logger.info(" [x] Received message")
    data = json.loads(body)
    _id = data["person_id"]
    person_name = data["person_name"]

    employee = get_employee(_id, person_name)

    if employee:
        logger.info(f'Employee "{employee.name}" found')

        now = datetime.utcnow()
        now = now.replace(tzinfo=timezone.utc).astimezone(tz=timezone(timedelta(hours=7)))
        time = TimeDAO.get_latest_in_date(employee.id, now.date())

        # Checkin between 7:00AM and 10:00AM
        # and no checkin today
        if 7 <= now.hour <= 12 and not time:
            # if now.hour <= 12 and not time:
            checkin(employee, data["drew_image_url"], ch)
        # Checkout after 5:30PM
        # and have checked in
        # and haven't checked out
        elif now.hour >= 17 and now.minute >= 30 and time and not time.completed:
            checkout(time, data["drew_image_url"], ch)
