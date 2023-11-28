from typing import Union
from fastapi import FastAPI, Request
import sqlite3
from datetime import datetime

app = FastAPI()

@app.post("/add_user/")
async def add_user(request: Request):
    data = await request.json()
    username = data["username"]
    password = data["password"]
    
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()

    try:
        cursor.execute('INSERT INTO user (name, password) VALUES (?, ?)', (username, password))
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
        cursor.execute('SELECT * FROM message WHERE receiver = ?', (receiver_id,))
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
    
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()

    timestamp = datetime.now()

    try:
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

