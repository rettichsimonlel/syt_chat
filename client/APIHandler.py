import requests
import os
import multipart

from typing import List

class APIHandler:
    def __init__(self, host) -> None:
        self.host = host
        self.Token = None

    def getPost(self, link, json, files=None):
        if files is None:
            return requests.post(self.host+link, json=json)
        return requests.post(self.host+link, json=json, files=files)

    def login(self, credentials: List[str]):
        self.username = credentials[0]
        self.password = credentials[1]

    def setReceiver(self, receiver):
        self.receiver = receiver

    def getToken(self):
        request = {
            "username": self.username,
            "password": self.password,
        }

        response = requests.get(self.host+"/get_token/", json=request).json()

        if "error" in response:
            return False
        if type(response["messages"]) != str:
            return False
        
        self.token = response["messages"]
        return True

    def postFile(self, filepath):
        if not os.path.exists(filepath):
            return
        request = {
            "token": self.token,
            "receiver_id": self.receiver,
            }
        f = open(filepath, "rb")
        files = {"file": (f.name, f, 'multipart/form-data') }

        response = requests.post(self.host+"/post_file/", request, files=files)
        
        
    def getUserId(self, username=None):
        setUserId = False
        if username is None:
            setUserId = True
            username = self.username

        request = {
                "username": username,
                "token": self.token,
                }

        data = requests.get(self.host+"/get_usr_id/", json=request).json()

        data = data["messages"]

        if data != []:
            data = data[0][0]
        else:
            return None

        if setUserId:
            self.userid = data

        return data

    def addMessage(self, message: str, receiver_id=None):
        if receiver_id is None:
            receiver_id = self.receiver
        request = {
                "token": self.token,
                "sender_id": self.userid,
                "receiver_id": receiver_id,
                "msg": message
                }

        return requests.post(self.host+"/add_msg/", json=request)

    def getMessages(self):
        request = {
                "token": self.token,
                "user_id": self.userid
                }

        data = requests.get(self.host+"/get_msg_usr/", json=request).json()
        return data["messages"]

    def addUser(self):
        request = {
            "token": self.token,
            "username": self.username,
            "password": self.password,
        }

        return requests.post(self.host+"/add_user/", json=request)


    def getUsers(self):
        response = requests.get(self.host+"/get_usrs/").json()["messages"]

        return response

    def getFileList(self):
        request = {
            "token": self.token,
            "receiver": self.receiver
        }

        response = self.getPost("/get_file_list/", request).json()["messages"]
        return(response)

    def getFile(self, args, filepath):
        if args == "":
            return self.getFileList()
        request = {
            "token": self.token,
            "filename": args,
        }

        response = requests.post(self.host+"/get_file/", json=request).content

        if not os.path.exists("static"):
            os.mkdir("static")
        path = os.path.split(args)
        if not os.path.exists(f"static/{path[-2]}"):
            os.mkdir(f"static/{path[-2]}")

        with open(f"static/{args}", "wb") as f:
           f.write(response) 

