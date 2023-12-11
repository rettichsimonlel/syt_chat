from APIHandler import APIHandler
from ChatApp import ChatApp

import os

from client import Client

def main():
#    apihandler = APIHandler("http://172.31.180.136:8000")
    apihandler = APIHandler("http://localhost:8000")

    client = Client(apihandler)
    client.login()
        
    user_id = apihandler.getUserId()

    first = True

    user_input = ""
    while user_input != "q" and first:
        fancy_users = []
        users = apihandler.getUsers()
        user_ids = []
        for user in users:
            fancy_users.append(f"{user[0]}: {user[1]}")
            user_ids.append(str(user[0]))
        print("\n".join(fancy_users))

        user_input = input("Select userID or q to quit: ")

        if user_input in user_ids and user_input != "q":
            appname = ""
            receiver = user_input
            for user in users:
                if str(user[0]) == str(receiver):
                    appname = user[1]

            apihandler.setReceiver(receiver)

            client.run_app(appname)
            first = False


if __name__ == "__main__":
    main()
    pass

