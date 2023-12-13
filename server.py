#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 文件名：server.py
import os.path
import socket  # 导入 socket 模块
import sys
import struct
import time

path = "../../Dataset/IRpic"


class Server:
    def __init__(self, port):
        try:
            server = socket.socket()  # 创建 socket 对象
            server.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            server.bind(('', port))  # 绑定端口
            server.listen(5)  # 等待客户端连接
            clientsocket, addr = server.accept()  # 建立客户端连接
            self.clientsocket = clientsocket
            self.addr = addr
        except socket.error as msg:
            print(msg)
            sys.exit(1)

    def deal_image(self):
        sock = self.clientsocket
        try:
            print("Accept connection from {0}".format(self.addr))  # 查看发送端的ip和端口
            while True:
                fileinfo_size = struct.calcsize('128sq')
                buf = sock.recv(fileinfo_size)  # 接收图片名
                if buf:
                    filename, filesize = struct.unpack('128sq', buf)
                    try:
                        filename = filename.decode()
                        fn = filename.strip('\x00') + '.jpg'
                    except UnicodeDecodeError as e:
                        print(f"Error decoding data: {e}")
                        return
                    fn = os.path.join(path, 'work', fn)
                    fp = open(fn, 'wb')
                    recvd_size = 0
                    while not recvd_size == filesize:
                        if filesize - recvd_size > 1024:
                            data = sock.recv(1024)
                            recvd_size += len(data)
                        else:
                            data = sock.recv(1024)
                            recvd_size = filesize
                        fp.write(data)  # 写入图片数据
                    fp.close()
                    print("Success!")

        except Exception as e:
            print(f"Error: {e}")
            print("Connection lost. Reconnecting...")
            # sock.close()
            self.reconnect_server()

    def reconnect_server(self):
        time.sleep(2)  # Wait for a while before reconnecting
        print("Attempting to reconnect...")
        self.deal_image()

    def send_message(self, message):
        try:
            print("Accept connection from {0}".format(self.addr))  # 查看发送端的ip和端口
            self.clientsocket.send(message.encode('utf-8'))
            print(f"Message sent to client: {message}")
        except (socket.error, OSError) as e:
            print(f"Error sending message: {e}")


def socket_service_image():
    s = Server(port=6123)
    while True:
        s.deal_image()
