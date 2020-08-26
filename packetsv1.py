import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
import socket

HEADER = 64
PORT = 5050
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "/disconnect"
SERVER = "192.168.56.1"
ADDR = (SERVER, PORT)
CONNECTED = True

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def send(msg):

    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b" " * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    if message == " /disconnect":
        global CONNECTED
        CONNECTED = False
    else:
        print(client.recv(2048).decode(FORMAT))


class MyGrid(GridLayout):
    def __init__(self, **kwargs):
        super(MyGrid, self).__init__(**kwargs)

        self.cols = 1

        self.inside = GridLayout()
        self.inside.cols = 2

        self.inside.add_widget(Label(text="Message: "))
        self.message = TextInput(multiline=False)
        self.inside.add_widget(self.message)

        self.add_widget(self.inside)

        self.send = Button(text="Send", font_size=20)

        self.send.bind(on_press=self.clicked)
        self.add_widget(self.send)

    def clicked(self, instance):
        message = self.message.text
        # print(message)
        send(message)
        self.message.text = ""


class MyApp(App):
    def build(self):
        return MyGrid()


if __name__ == "__main__":
    MyApp().run()