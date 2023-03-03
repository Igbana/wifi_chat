from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.screen import MDScreen
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivymd.uix.card import MDCard
from kivy.clock import mainthread
from kivy.properties import StringProperty
import socket
import json
import threading


class LoginPage(MDScreen):
    def __init__(self):
        super(LoginPage, self).__init__()

    def login(self, nickname):
        if nickname == "":
            self.error_msg.text = "Name cannot be empty"
        else:
            global client
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect(('127.0.0.1', 9999))
            message = client.recv(1024).decode()
            if message == "NICK":
                client.send(self.nickname_text.text.encode())
                self.manager.get_screen('home').nickname_label.text = nickname
                self.manager.transition.direction = 'left'
                self.manager.current = 'home'
                threading.Thread(target=self.manager.get_screen('home').receive).start()

class MessageBox(AnchorLayout):
    sender = StringProperty()
    message = StringProperty()

class HomePage(MDScreen):
    def receive(self):
        self.running = True
        while self.running:
            try:
                message = json.loads(f'{client.recv(1024).decode()}')
                print(message)
                self.display_chat(message)
            except Exception as e:
                self.close_connection()

    @mainthread
    def display_chat(self, message):
        self.chat_list.add_widget(MessageBox(sender = list(message.keys())[0], message = message[list(message.keys())[0]], anchor_x = 'right' if list(message.keys())[0] == self.nickname_label.text else 'left'))

    def send_message(self, message):
        if message == 'xKill':
            message = 'x-Kill'
        client.send(message.encode())
    
    def close_connection(self):
        self.running = False
        try:
            client.send('xKill'.encode())
        except:
            pass

class MainApp(MDApp):    
    def build(self):
        self.theme_cls.theme_style = 'Dark'
        sm = ScreenManager()
        sm.add_widget(LoginPage())
        sm.add_widget(HomePage())
        return sm

MainApp().run()
try:
    client.close()
except:
    pass