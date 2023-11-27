import curses

from APIHandler import APIHandler
from typing import List
from getpass import getpass

def login() -> [str, str]:
    username = input("username: ")
    password = getpass("password: ")
    return [username, password]

def main():
    apihandler = APIHandler("http://172.31.180.14:8000")
    apihandler2 = APIHandler("http://172.31.180.14:8000")

#    [username, password] = login()
    credentials = ["testUser", "Kennwort1"]
    credentials2 = ["testUser2", "Kennwort1"]

    apihandler.login(credentials)
    apihandler2.login(credentials2)

#    apihandler.addUser()
#    apihandler2.addUser()

#    user2id = apihandler.getUserId("testUser2")
    apihandler2.getUserId()
#    apihandler.getUserId()

#    print(apihandler.addMessage(user2id, "Hello World"))

    print(apihandler2.getMessages())


if __name__ == "__main__":
    main()
    pass

