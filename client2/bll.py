"""
客户端 逻辑处理层

1. 建立套接字与服务端连接
2. 接收界面层指令和逻辑处理
"""
import os

ADDR = ('127.0.0.1', 10000)

from socket import *
from threading import Thread


class Client:
    def __init__(self):
        self.sockfd = socket(AF_INET, SOCK_DGRAM)

    def login(self, name, pwd):
        msg = "L " + name + ' ' + pwd
        self.sockfd.sendto(msg.encode(), ADDR)
        # 等待回复
        data, addr = self.sockfd.recvfrom(1024)
        return data.decode()

    def register(self, name, pwd):
        msg = "R " + name + ' ' + pwd
        self.sockfd.sendto(msg.encode(), ADDR)
        # 等待回复
        data, addr = self.sockfd.recvfrom(1024)
        return data.decode()

    def send(self, name, msg):
        msg = 'M ' + name + ' ' + msg
        self.sockfd.sendto(msg.encode(), ADDR)

    def recv(self):
        data, addr = self.sockfd.recvfrom(2048)
        print(data.decode())
        return data.decode()

    def quit(self, name):
        msg = 'Q ' + name
        self.sockfd.sendto(msg.encode(), ADDR)

    def chat(self):
        t = Thread(target=self.recv, args=())
        t.setDaemon(True)
        t.start()