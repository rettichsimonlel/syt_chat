import requests

from typing import List

class APIHandler:
    def __init__(self, host) -> None:
        self.host = host

    def login(self, credentials: List[str]):
        self.username = credentials[0]
        self.password = credentials[1]

    def setReceiver(self, receiver):
        self.receiver = receiver

    def getUserId(self, username=None):
        setUserId = False
        if username is None:
            setUserId = True
            username = self.username

        request = {
                "username": username
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
                "sender_id": self.userid,
                "receiver_id": receiver_id,
                "msg": message
                }

        return requests.post(self.host+"/add_msg/", json=request)

    def getMessages(self):
        request = {
                "user_id": self.userid
                }

        data = requests.get(self.host+"/get_msg_usr/", json=request).json()
        return data["messages"]

    def addUser(self):
        request = {
            "username": self.username,
            "password": self.password,
        }

        return requests.post(self.host+"/add_user/", json=request)


    def getUsers(self):
        response = requests.get(self.host+"/get_usrs/").json()["messages"]

        return response

