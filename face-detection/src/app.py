from src.services.rabbitmq import FaceDetectionService


async def app():
    face_detection_service = FaceDetectionService()
    await face_detection_service.connect()
    await face_detection_service.declare_exchange()
    await face_detection_service.start_consuming()
    await face_detection_service.close()
