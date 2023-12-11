from APIHandler import APIHandler
from getpass import getpass
from time import sleep
from ChatApp import ChatApp

import os
import threading

global toggleUpdate
toggleUpdate = True
global apihandler
apihander = None
global app
app = None

def handleClear(args):
    global toggleUpdate
    toggleUpdate = True

def handleGet(args):
    global app
    global toggleUpdate
    global apihandler

    if args == "":
        response = apihandler.getFileList()
        toggleUpdate = False

        app.set_read_box("\n".join(response))
    else:
        response = apihandler.getFile(args, f"static/{args}")

def update(apihandler, receiver, sender, running):
    global toggleUpdate
    global app
    sleep(1)
    while running[0]:
        messages = apihandler.getMessages()
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

        if running[0] and toggleUpdate:
            app.set_read_box(text)
        sleep(1)

def main():
    global apihandler
    global app
    auth = False
    apihandler = APIHandler("http://172.31.180.136:8000")
#    apihandler = APIHandler("http://localhost:8000")

    while not auth:
        username = input("username: ")
        password = getpass("password: ")
        apihandler.login([username, password])
        auth = apihandler.getToken()
        
    first = True

    user_id = apihandler.getUserId()
    if user_id == None:
        apihandler.addUser()
        user_id = apihandler.getUserId()

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

            run_app(user_id, receiver, first, appname)
            first = False

def run_app(user_id, receiver, first, appname):
    global apihandler
    global app
    running = [False]

    ACTIONS = {
        "put": apihandler.postFile,
        "get": handleGet,
        "clear": handleClear,
    }

    app = ChatApp(appname, apihandler.addMessage, ACTIONS)


    update_thread = threading.Thread(target=update, kwargs={"apihandler": apihandler, "receiver": receiver, "sender": user_id, "running": running})
    update_thread.start()

    running[0] = True

    if first:
        app.run()
    else:
        app.main()

    running[0] = False

if __name__ == "__main__":
    main()
    pass

