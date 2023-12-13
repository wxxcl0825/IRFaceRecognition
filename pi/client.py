import socket
import sys
import struct
import time
import os


class Client:
    def __init__(self, port):
        self.reconnect_delay = 2  # seconds
        self.port = port
        self.connect_to_server()

    def connect_to_server(self):
        while True:
            try:
                self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.s.connect(('10.186.114.135', self.port))
                break  # Exit the loop if the connection is successful
            except socket.error as e:
                print(f"Error: {e}")
                self.s.close()
                time.sleep(self.reconnect_delay)
                print("Reconnecting to the server...")

    def upload(self, fp):
        # <send_time> <file_size>
        print(f"fp:{fp} size:{os.stat(fp).st_size}")
        try:
            fhead = struct.pack(b'128sq', str(int(time.time())).encode(), os.stat(fp).st_size)
            with open(fp, 'rb') as f:
                self.s.send(fhead)
                while True:
                    data = f.read(1024)
                    if not data:
                        break
                    self.s.send(data)
            print("Success")
        except socket.error as e:
            print(f"Error: {e}")
            print("Connection lost. Reconnecting...")
            self.s.close()
            self.connect_to_server()

    def receive_message(self):
        try:
            # 接收消息的最大长度，可以根据实际需求调整
            max_msg_length = 1024
            message = self.s.recv(max_msg_length).decode('utf-8')
            if (message):
                return message
            else:
                return None
        except (socket.error, OSError, UnicodeDecodeError) as e:
            print(f"Error receiving message: {e}")
            return None
