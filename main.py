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
        cursor.execute('INSERT INTO msg (sender, receiver, msg, timestamp) VALUES (?, ?)', (sender_id, receiver_id, msg, timestamp))
    except:
        pass

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

