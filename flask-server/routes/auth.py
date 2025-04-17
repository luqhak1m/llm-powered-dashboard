
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

@auth_bp.route("/login", methods=['POST'])
def login():

    data=request.get_json()
    email=data.get("email")
    password=data.get("password")

    print(f"Received: {email}, {password}")
    return '', 204  # no content

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