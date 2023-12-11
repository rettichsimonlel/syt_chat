from typing import Union
from fastapi import FastAPI, Request, File, UploadFile, Form, Response
import sqlite3
from datetime import datetime
from secrets import token_hex
import os
import bcrypt

app = FastAPI()

global tokens
tokens = {}

async def add_user(data: dict):
    username = data["username"]
    password = data["password"]

    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()

    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)

    try:
        cursor.execute('INSERT INTO user (name, password) VALUES (?, ?)', (username, hashed))
    except:
        pass


    conn.commit()
    conn.close()

@app.post("/add_msg/")
async def add_msg(request: Request):
    data = await request.json()
    sender_id = data["sender_id"]
    receiver_id = data["receiver_id"]
    msg = data["msg"]
    
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()

    timestamp = datetime.now()

    try:
        cursor.execute('INSERT INTO message (sender, receiver, msg, timestamp) VALUES (?, ?, ?, ?)', (sender_id, receiver_id, msg, timestamp))
    except Exception as e:
        if hasattr(e, "message"):
            print(e.messages)
        else:
            print(e)

    conn.commit()
    conn.close()

@app.get("/get_msg_usr/")
async def get_messages_by_user(request: Request):
    data = await request.json()
    receiver_id = data["user_id"]
    
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()

    timestamp = datetime.now()

    try:
        cursor.execute('SELECT * FROM message WHERE sender = ? OR receiver = ?', (receiver_id,receiver_id))
        message = cursor.fetchall()

        return {"messages": message}
    except:
        return {"error": "receiver not found"}
    finally:
        conn.close()


@app.get("/get_usr_id/")
async def get_usr_id(request: Request):
    data = await request.json()
    username = data["username"]
    token = data["token"]
    
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()

    timestamp = datetime.now()

    try:
        if token in tokens:
            cursor.execute('SELECT id FROM user WHERE name = ?', (username,))
            message = cursor.fetchall()

        return {"messages": message}
    except:
        return {"error": "receiver not found"}
    finally:
        conn.close()

@app.get("/get_usrs/")
def get_usrs():
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()

    try:
        cursor.execute('SELECT id, name FROM user')
        message = cursor.fetchall()

        return {"messages": message}
    except:
        return {"error": "receiver not found"}
    finally:
        conn.close()

@app.post("/post_file/")
def post_file(token: str = Form(...), receiver_id: int = Form(...), file: UploadFile = File(...)):
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    
    if token not in tokens:
        return {"error": "Bad things happen to you"}
    
    user_name = tokens[token]
    
    if not os.path.exists('./static'):
        os.mkdir('./static')

    user_directory = os.path.join(".", "static", user_name)
    if not os.path.exists(user_directory):
        os.mkdir(user_directory)

    kek = user_directory + '/' + file.filename.split('/')[-1]
    try:
        sender = cursor.execute('SELECT id FROM user WHERE name = ?', (user_name,)).fetchall()
        cursor.execute('INSERT INTO file (receiver, sender, filepath) VALUES (?, ?, ?)', (receiver_id, sender[0][0], kek))
    except Exception as e:
        print(f"nothing in db: {e}")

    try:
        contents = file.file.read()
        with open(user_directory + "/" + file.filename.split('/')[-1], 'wb') as f:
            f.write(contents)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()

    conn.commit()
    conn.close()

    return {"message": f"Successfully uploaded {file.filename}"}

@app.post("/get_file_list/")
async def get_file_list(request: Request):
    data = await request.json()

    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()

    token = data["token"]
    receiver = data["receiver"]

    user_name = tokens[token]
    sender = ""

    try:
        sender = cursor.execute('SELECT id FROM user WHERE name = ?', (user_name,)).fetchall()[0][0]
    except Exception as e:
        print("Error getting sender: " + e)

    message = []

    try:
        cursor.execute('SELECT filepath FROM file WHERE sender = ? AND receiver = ?', (sender, receiver))
        message.extend(cursor.fetchall())
    except Exception as e:
        print("Error loading: " + e)

    try:
        cursor.execute('SELECT filepath FROM file WHERE sender = ? AND receiver = ?', (receiver, sender))
        message.extend(cursor.fetchall())
    except Exception as e:
        print("Error loading: " + e)

    conn.close()

    print(message)
    new_msg = []
    for file in message:
        split_msg = file[0].split('/')
        new_msg.append(split_msg[-2] + '/' + split_msg[-1])
    
    return {"messages": new_msg}

@app.post("/get_file/")
async def get_file(request: Request):
    data = await request.json()

    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    
    
    token = data["token"]

    filename = data["filename"]

    sender = ""

    message = ""

    try:
        with open(f'./static/{filename}', 'rb') as file:
            message = file.read()
    except Exception as e:
        print(f"Error loading: {e}")

    try:
        return Response(content=message, media_type="text")
    except:
        return Response(content=message, media_type="image/png")

@app.get("/get_token/")
async def get_token(request: Request):
    data = await request.json()

    username = data["username"]
    password = data["password"]
    
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()

    message = None

    try:
        cursor.execute('SELECT id FROM user WHERE name = ?', (username,))
        message = cursor.fetchall()
        if message is None or message == []:
            await add_user({ "username": username, "password": password })
    except:
        return {"error": "receiver not found"}
    try:
        cursor.execute('SELECT id, password FROM user WHERE name = ?', (username,))
        message = cursor.fetchall()
    except:
        return {"error": "receiver not found"}
    finally:
        if message is not None and message != []:
            tmp_keys = []
            if not bcrypt.checkpw(password.encode('utf-8'), message[0][1]):
                return { "error": "no token you cheeky bastard" }
            for key in tokens:
                if tokens[key] == username:
                    tmp_keys.append(key)
            for key in tmp_keys:
                del tokens[key]

            token = token_hex()
            tokens[token]= username
            print(tokens)
            conn.close()
            return { "messages": token }
        conn.close()
        return { "error": "no token you cheeky bastard" } 

