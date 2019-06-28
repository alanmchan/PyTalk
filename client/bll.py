"""
客户端 逻辑处理层

1. 建立套接字与服务端连接
2. 接收界面层指令和逻辑处理
"""
import os

ADDR = ('127.0.0.1', 10000)

from socket import *
from threading import Thread
# from ui import App

class Client:
	def __init__(self):
		self.sockfd = socket(AF_INET, SOCK_DGRAM)
		# self.app = App(self)

	def login(self, name, pwd):
		msg = "L " + name + ' ' + pwd
		print(msg)
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
		while True:
			data, addr = self.sockfd.recvfrom(2048)
			# return data.decode()
			print(data.decode())

	def quit(self, name):
		msg = 'Q ' + name
		self.sockfd.sendto(msg.encode(), ADDR)

	def chat(self):
		self.t_list = []
		# 创建分支线程发送消息
		t = Thread(target=self.send, args=('zhangsan','nihao ya'))
		self.t_list.append(t)
		t.start()
		# 创建分支线程接收消息
		t = Thread(target=self.recv, args=())
		self.t_list.append(t)
		t.start()

		# 回收进程
		for t in self.t_list:
			t.join()



if __name__ == '__main__':
	client = Client()
	# re = client.login('zhangsan', '123')
	# print(re)
	# re = client.register('zhaoliu', '123456')
	# print(re)
	# client.send('zhangsan','dajiahao ya')
	client.chat()