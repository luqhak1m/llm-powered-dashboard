
from flask import Blueprint, request, jsonify
import sqlite3

auth_bp=Blueprint('auth', __name__)

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
    conn.commit()
    conn.close()

init_db()

# testuser1@mmu.com
# testUser
# 123123


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
        return jsonify(
            {
                "message": "Login successful!",
                "username": username,
                "email": user[2]
            }
        ), 200
    else:
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
    except sqlite3.IntegrityError:
        return jsonify(
            {
                "ERROR": "E-mail already exists"
            }
        ), 409
    finally:
        conn.close()

    return jsonify({'message': 'User registered successfully'}), 201