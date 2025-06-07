
from flask import Blueprint, request, jsonify
import sqlite3

import os
from dotenv import load_dotenv

import jwt
import datetime

import json

from module.state import state
from module.tools import Tool

auth_bp=Blueprint('auth', __name__)

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

print(SECRET_KEY)

def init_db():
    conn=sqlite3.connect("users.db")
    cursor=conn.cursor()
    cursor.execute('''
		CREATE TABLE IF NOT EXISTS users (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			username TEXT NOT NULL,
			email TEXT NOT NULL UNIQUE,
			password TEXT NOT NULL
		)
	''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_tools (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            tools TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS saved_visuals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            visualization TEXT,
            analysis TEXT,
            prompt TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    ''')
    conn.commit()
    conn.close()

    # print("db_init() successfully executed")

init_db()

# testuser1@mmu.com
# testUser
# 123123

@auth_bp.route("/currentUser", methods=["GET"])
def currentUser():
    auth_header=request.headers.get("Authorization")
    if not auth_header:
        return jsonify(
            {
                "error": "Missing Token"
            }
        ), 401
    
    token=auth_header.replace("Bearer ", "")
    try:
        decoded=jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return jsonify(
            {
                "username": decoded["username"],
                "email": decoded["email"]
            }
        ), 200
    except jwt.ExpiredSignatureError:
        return jsonify(
            {
                "error": "Token Expired"
            }
        ), 401
    except jwt.InvalidTokenError:
        return jsonify(
            {
                "error": "Invalid Token"
            }
        ), 401

@auth_bp.route("/login", methods=['POST'])
def login():

    data=request.get_json()
    username=data.get("username")
    password=data.get("password")

    conn=sqlite3.connect("users.db")
    cursor=conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username = ? AND password = ?", (username, password)
    )

    user=cursor.fetchone()
    conn.close()

    if user:
        print("GETTING TOOLS FROM auth.py")
        payload={
            "id": user[0],
            "username": user[1],
            "email": user[2],
            "exp": int((datetime.datetime.now() + datetime.timedelta(hours=1)).timestamp())
        }
        token=jwt.encode(payload, SECRET_KEY, algorithm="HS256")

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("SELECT tools FROM user_tools WHERE user_id = ?", (user[0],))
        row = cursor.fetchone()
        conn.close()

        selected_tool_names = json.loads(row[0]) if row else []
        original_tools = Tool().tools
        filtered_tools = [tool for tool in original_tools if tool.name in selected_tool_names]
        state["tools"] = filtered_tools

        print(f"""\nState updated with: \n
            tools: {type(state['tools'])} {len(state['tools'])}
            """)

        return jsonify({
            "message": "Login Successful",
            "token": token
        }), 200
    
    return jsonify(
        {
            "error": "Invalid credentials"
            }
    ), 401

@auth_bp.route("/register", methods=['POST'])
def register():

    data=request.get_json()
    email=data.get("email")
    username=data.get("username")
    password=data.get("password")

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
            (username, email, password)
        )
        conn.commit()

        user_id = cursor.lastrowid
        tools_json = json.dumps(Tool().get_tool_names())
        print(f"tools_json: {tools_json}")

        cursor.execute(
            "INSERT INTO user_tools (user_id, tools) VALUES (?, ?)",
            (user_id, tools_json)
        )

        conn.commit()

        tools=Tool()
        tools_list=tools.tools
        state["tools"] = tools_list

        print(f"""\nState updated with: \n
            tools: {type(state['tools'])} {len(state['tools'])}
            """)

    except sqlite3.IntegrityError:
        return jsonify(
            {
                "ERROR": "E-mail already exists"
            }
        ), 409
    finally:
        conn.close()

    payload={
            "id": cursor.lastrowid,
            "username": username,
            "email": email,
            "exp": int((datetime.datetime.now() + datetime.timedelta(hours=1)).timestamp())
        }
    token=jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    return jsonify({
        "message": "Registration Successful",
        "token": token
    }), 200