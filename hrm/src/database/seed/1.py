import requests
from src.database.dao.mapping import MappingDAO


def create_employees():
    url = "http://103.157.218.115/HRM/hs/HRM/V1/AllEmployee"
    basic_auth = ("LongPT", "123456")

    response = requests.get(url, auth=basic_auth)
    print(response.json())

    MappingDAO.create
