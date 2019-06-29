"""
客户端 视图层

为用户提供图形界面,将用户指令发给逻辑处理层
"""
import sys
import tkinter as tk
import time
from threading import Thread
from tkinter import messagebox

from bll import Client


class App:
    def __init__(self, master=None):
        self.client = Client()
        self.master = master
        self.master.title('PyTalk')
        self.master.geometry('250x180')
        self.master.resizable(0, 0)
        self.init_widget()

    def init_widget(self):
        self.label1 = tk.Label(self.master, text='Welcome to PyTalk', font=('微软雅黑', 16))
        self.label1.grid(row=0, column=0, columnspan=3)
        self.label2 = tk.Label(self.master, text="用户名：")
        self.label2.grid(row=1, column=0, padx=10, pady=10)
        self.label3 = tk.Label(self.master, text="密  码：")
        self.label3.grid(row=2, column=0, padx=10, pady=10)

        self.name = tk.StringVar()  # 创建tk字符串用于绑定输入的用户名
        self.entry_name = tk.Entry(self.master, textvariable=self.name)
        self.entry_name.grid(row=1, column=1, columnspan=2, padx=10, pady=10)
        self.pwd = tk.StringVar()  # 创建tk字符串用于绑定输入的密码
        self.entry_pwd = tk.Entry(self.master, textvariable=self.pwd, show="*")
        self.entry_pwd.grid(row=2, column=1, columnspan=2, padx=10, pady=10)

        self.btn_register = tk.Button(self.master, text='Register', command=self.register)
        self.btn_register.grid(row=3, column=0, padx=10, pady=10)
        self.btn_login = tk.Button(self.master, text='Login', command=self.login)
        self.btn_login.grid(row=3, column=1, padx=10, pady=10)
        self.btn_quit = tk.Button(self.master, text='Cancel', command=self.master.quit, fg='red')
        self.btn_quit.grid(row=3, column=2, padx=10, pady=10)

    def register(self):
        reg_window = tk.Toplevel(self.master)
        reg_window.title('Register PyTalk')
        reg_window.resizable(0, 0)

        tk.Label(reg_window, text='用户名:').grid(row=0, column=0, padx=10, pady=10)
        tk.Label(reg_window, text='密码:').grid(row=1, column=0, padx=10, pady=10)
        tk.Label(reg_window, text='确认密码:').grid(row=2, column=0, padx=10, pady=10)
        self.reg_name = tk.StringVar()
        entry_name = tk.Entry(reg_window, textvariable=self.reg_name)
        entry_name.grid(row=0, column=1, padx=10, pady=10)
        self.reg_pwd = tk.StringVar()
        entry_pwd = tk.Entry(reg_window, textvariable=self.reg_pwd, show='*')
        entry_pwd.grid(row=1, column=1, padx=10, pady=10)
        self.reg_pwd2 = tk.StringVar()
        entry_pwd2 = tk.Entry(reg_window, textvariable=self.reg_pwd2, show='*')
        entry_pwd2.grid(row=2, column=1, padx=10, pady=10)
        btn_register = tk.Button(reg_window, text='Register', command=self.do_register)
        btn_register.grid(row=3, column=0, padx=10, pady=10)
        btn_quit = tk.Button(reg_window, text='Cancel', command=reg_window.quit)
        btn_quit.grid(row=3, column=1, padx=10, pady=10)

    def login(self):
        name = self.name.get()
        pwd = self.pwd.get()
        result = self.client.login(name, pwd)
        if result == 'OK':
            self.chat()
        else:
            tk.messagebox.showerror(message=result)

    def do_register(self):
        if self.reg_pwd.get() == self.reg_pwd2.get():
            result = self.client.register(self.reg_name.get(), self.reg_pwd.get())
            if result == 'OK':
                tk.messagebox.showinfo(message="注册成功")
            else:
                tk.messagebox.showerror(message=result)
        else:
            tk.messagebox.showerror(message="两次密码不同")

    def chat(self):
        print('welcome')
        self.forget_login()
        self.master.geometry('800x600')
        self.master.title(f'PyTalk {self.name.get()}')
        self.master.protocol("WM_DELETE_WINDOW", self.quit)
        self.dialog = tk.Text(self.master, font=('微软雅黑', 16, 'normal'), state='disable')  # , textvariable=self.dialog_text
        self.dialog.place(relx=0, rely=0, relwidth=1, relheight=0.7)
        self.input = tk.Text(self.master, font=('微软雅黑', 16, 'normal'))  # , textvariable=self.input_text
        self.input.place(relx=0, rely=0.7, relwidth=1, relheight=0.2)
        self.btn_send = tk.Button(self.master, command=self.send, text='发送', font=('微软雅黑', 16, 'normal'))
        self.btn_send.place(relx=0, rely=0.9, relwidth=0.5, relheight=0.1)
        self.btn_cancle = tk.Button(self.master, command=self.cancle, text='取消', font=('微软雅黑', 16, 'normal'))
        self.btn_cancle.place(relx=0.5, rely=0.9, relwidth=0.5, relheight=0.1)

        # 创建线程接收消息
        t = Thread(target=self.recv)
        t.setDaemon(True)
        t.start()
        # t.join()

    def forget_login(self):
        '''移除登录界面的控件，以便放置其他界面的控件'''
        self.label1.pack_forget()
        self.label2.pack_forget()
        self.label3.pack_forget()

        self.entry_name.pack_forget()
        self.entry_pwd.pack_forget()

        self.btn_register.pack_forget()
        self.btn_login.pack_forget()
        self.btn_quit.pack_forget()

    def send(self):
        msg = self.input.get(1.0, 'end')
        if not msg or msg == '\n':
            messagebox.showwarning('warning', '消息为空，发送失败')
        else:
            print(msg)
            # 修改消息框为可编辑状态
            self.dialog.config(state='normal')
            # 为消息框设置time——style样式，用于显示时间
            self.dialog.tag_config('send_time_style', font=('Arial', 10, 'normal'), justify='right', foreground='silver')  #
            # 为消息框设置text——style样式，用于显示用户输入消息
            self.dialog.tag_config('send_text_style', font=('微软雅黑', 16, 'normal'), justify='right')  # , background='lightgreen'
            # 在消息框插入时间, 并指定样式
            time_string = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n'
            self.dialog.insert('end', time_string, 'send_time_style')
            # 在消息框插入信息， 并制定样式
            self.dialog.insert('end', msg + '\n', 'send_text_style')
            # 修改消息框为不可编辑状态
            self.dialog.config(state='disable')
            # 清空输入框内容
            self.input.delete(1.0, 'end')
            # 发送消息
            self.client.send(self.name.get(), msg)

    def recv(self):
        print("接收消息")
        while True:
            msg = self.client.recv()
            print('client -- ui-->bll の', msg)
            if msg == 'EXIT':
                self.master.quit()
                sys.exit()
            msg_list = msg.split(' ')
            name = msg_list[0]
            msg = ' '.join(msg_list[1:])
            self.dialog.configure(state='normal')  # 修改消息框为可编辑状态
            # 为消息框设置time——style样式，用于显示时间
            self.dialog.tag_config('recv_time_style', font=('Arial', 10, 'normal'), justify='left', foreground='silver')
            # 为消息框设置text——style样式，用于显示用户输入消息
            self.dialog.tag_config('recv_text_style', font=('微软雅黑', 16, 'normal'), justify='left')
            # 在消息框插入时间, 并指定样式
            time_string = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n'
            self.dialog.insert('end', time_string, 'recv_time_style')
            # 在消息框插入信息， 并制定样式
            self.dialog.insert('end', name + ':\n', 'recv_text_style')  # 插入姓名
            self.dialog.insert('end', msg + '\n', 'recv_text_style')  # 插入消息
            self.dialog.config(state='disable')# 修改消息框为不可编辑状态

    def cancle(self):
        self.input.delete(1.0, 'end')

    def quit(self):
        self.client.quit(self.name.get())
        # if data == 'EXIT':
        #     sys.exit(f'{self.name.get()}退出聊天室')


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
