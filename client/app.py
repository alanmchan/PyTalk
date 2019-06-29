from bll import Client
from ui import *

class App:
    def __init__(self):
        self.client = Client()
        self.ui = UILogin(self.client)