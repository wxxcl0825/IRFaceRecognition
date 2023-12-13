import time
import os
from threading import Thread
from client import Client
from detect import detect
import subprocess
from tts import speak

pic_path = "../IRpic"
timeout = 2


def shot():
    while True:
        temp_file = f"{pic_path}/temp.jpg"
        process = subprocess.Popen(f"libcamera-jpeg --autofocus-mode continuous -o {temp_file} -t 2 >/dev/null 2>&1",
                                   shell=True)
        process.wait()  # 等待直到 temp.jpg 文件被创建
        os.rename(temp_file, f"{pic_path}/{int(time.time())}.jpg")


def upload():
    s = Client(port=6123)
    while True:
        files = os.listdir(pic_path)
        for file in files:
            file_time = file[:-4]
            if file == "temp.jpg":
                continue
            if detect(os.path.join(pic_path, file)):
                s.upload(os.path.join(pic_path, file))
                # print("upload successfully!")
            os.remove(os.path.join(pic_path, file))


def recieve():
    r = Client(port=6124)
    while True:
        message = r.receive_message()
        if (message):
            print(f"Received message from server: {message}")
            speak(f"你好，{message.split('0')[0]}")


if __name__ == "__main__":
    Thread(target=shot).start()
    Thread(target=upload).start()
    t = Thread(target=recieve)
    t.start()
    t.join()
