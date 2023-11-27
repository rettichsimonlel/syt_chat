import requests

from typing import List

class APIHandler:
    def __init__(self, host) -> None:
        self.host = host

    def login(self, credentials: List[str]):
        self.username = credentials[0]
        self.password = credentials[1]

    def getUserId(self, username=None):
        setUserId = False
        if username is None:
            setUserId = True
            username = self.username

        request = {
                "username": username
                }

        data = requests.get(self.host+"/get_usr_id/", json=request).json()["messages"]

        data = data[0][0]

        if setUserId:
            self.userid = data

        return data

    def addMessage(self, receiver_id, message: str):
        request = {
                "sender_id": self.userid,
                "receiver_id": receiver_id,
                "msg": message
                }

        print(request)

        return requests.post(self.host+"/add_msg/", json=request)

    def getMessages(self):
        request = {
                "user_id": self.userid
                }

        print(request)
        data = requests.get(self.host+"/get_msg_usr/", json=request).json()
        return data

    def addUser(self):
        request = {
            "username": self.username,
            "password": self.password,
        }

        return requests.post(self.host+"/add_user/", json=request)

