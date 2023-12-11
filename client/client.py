from APIHandler import APIHandler
from getpass import getpass
from time import sleep
from ChatApp import ChatApp

import os
import threading

class Client:
    def __init__(self, apihandler):
        self.toggleUpdate = True 
        self.apihandler = apihandler
        self.app = None
        self.running = False

    def login(self):
        auth = False
        while not auth:
            username = input("username: ")
            password = getpass("password: ")
            self.apihandler.login([username, password])
            auth = self.apihandler.getToken()

    def handleClear(self, args):
        self.toggleUpdate = True

    def update(self):
        sleep(1)
        sender = self.apihandler.userid
        receiver = self.apihandler.receiver
        while self.running:
            messages = self.apihandler.getMessages()
            filtered = []

            for i in messages:
                if(str(i[1]) == str(receiver)) or str(i[2]) == str(receiver):
                    filtered.append(i)

            text = []
            for i in filtered:
                for msg in i[3].split("\n"):
                    if str(i[2]) == str(receiver) and str(sender) == str(i[1]):
                        text.append(f"You   : {msg}")
                    elif str(i[1]) == str(receiver) and str(sender) == str(i[2]):
                        text.append(f"Other : {msg}")

            text = text[-35:]
            text = "\n".join(text)

            if self.running and self.toggleUpdate:
                self.app.set_read_box(text)
            sleep(1)

    def handleGet(self, args):
        if args == "":
            self.toggleUpdate = False
            response = self.apihandler.getFileList()

            self.app.set_read_box("\n".join(response))
        else:
            response = self.apihandler.getFile(args, f"static/{args}")

    def run_app(self, appname):
        ACTIONS = {
            "put": self.apihandler.postFile,
            "get": self.handleGet,
            "clear": self.handleClear,
        }

        self.app = ChatApp(appname, self.apihandler.addMessage, ACTIONS)

        update_thread = threading.Thread(target=self.update)
        update_thread.start()

        self.running = True

#        self.toggleUpdate = False
        self.app.run()

        self.running = False
