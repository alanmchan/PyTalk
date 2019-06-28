"""
服务端 逻辑处理层

1. 建立套接字链接
2. 逻辑处理: 处理客户端请求和调用模型层
"""
from multiprocessing import Process
from socket import *
from threading import Thread

from server.models import DBManager

HOST = '0.0.0.0'
POST = 10000
ADDR = (HOST, POST)


class Server:
	def __init__(self):
		self.address = ADDR
		self.users = {}
		self.create_socket()
		self.db_manager = DBManager()
	
	def create_socket(self):
		'''创建套接字，并绑定地址'''
		self.sockfd = socket(AF_INET, SOCK_DGRAM)
		self.sockfd.bind(self.address)
	
	def start_server(self):
		# print('child')

		client = Thread(target=self.handle, args=())
		client.setDaemon(True)
		# client.daemon = True
		client.start()

		while True:
			msg = input("公告:\n")
			msg = "M 公告 " + msg
			self.sockfd.sendto(msg.encode(), ('127.0.0.1', 10000))

	def handle(self):
		while True:
			data, addr = self.sockfd.recvfrom(1024)
			print(data.decode())
			data = data.decode().split(' ')
			# 区分请求
			if data[0] == 'L':
				name = data[1]
				pwd = data[2]
				self.do_login(name, pwd, addr)
			elif data[0] == 'R':
				name = data[1]
				pwd = data[2]
				self.do_register(name, pwd, addr)
			elif data[0] == 'Q':
				name = data[1]
				self.do_quit(name)
			elif data[0] == 'M':
				name = data[1]
				msg = ' '.join(data[2:])
				# self.users[name] = addr
				# print(msg)
				self.do_chat(name, msg)

	def do_login(self, name, pwd, addr):
		result = self.db_manager.do_login(name, pwd)
		if result == 'OK':
			self.sockfd.sendto(b'OK', addr)
			# 通知其他用户有人加入聊天室
			msg = '欢迎%s进入聊天室' % name
			for user in self.users:
				self.sockfd.sendto(msg.encode(), self.users[user])
			# 将新用户加入在线用户列表
			self.users[name] = addr
			print(self.users)
		else:  # 登录失败，返回消息
			self.sockfd.sendto(result.encode(), addr)

	def do_register(self, name, pwd, addr):
		result = self.db_manager.do_register(name, pwd)
		self.sockfd.sendto(result.encode(), addr)

	def do_quit(self, name):
		msg = "%s 退出聊天室" % name
		for user in self.users:
			if user != name:
				self.sockfd.sendto(msg.encode(), self.users[user])

	def do_chat(self, name, msg):
		msg = name + ' ' + msg
		for user in self.users:
			if user != name:
				self.sockfd.sendto(msg.encode(), self.users[user])


if __name__ == "__main__":
	server = Server()
	server.start_server()
	# server.handle()