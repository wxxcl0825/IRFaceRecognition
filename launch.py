from threading import Thread
from main import main
from server import socket_service_image

if __name__ == "__main__":
    Thread(target=main).start()
    Thread(target=socket_service_image).start()