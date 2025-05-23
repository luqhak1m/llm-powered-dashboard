from flask import Blueprint, request, jsonify
import sqlite3
import json
import jwt
import os
from dotenv import load_dotenv
from module.tools import Tool
from module.state import state


tools_bp = Blueprint('tools', __name__)
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

@tools_bp.route("/tools-list", methods=["GET"])
def get_tools():
    t = Tool()
    return jsonify(t.get_tool_names())


@tools_bp.route("/save-tools", methods=["POST"])
def save_tools():
    data = request.get_json()
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    selected_tools = data.get("tools")

    if not selected_tools or not isinstance(selected_tools, list):
        return jsonify({"error": "Invalid tools list"}), 400

    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id = decoded["id"]
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM user_tools WHERE user_id = ?", (user_id,))
    existing = cursor.fetchone()

    if existing:
        cursor.execute(
            "UPDATE user_tools SET tools = ? WHERE user_id = ?",
            (json.dumps(selected_tools), user_id)
        )
    else:
        cursor.execute(
            "INSERT INTO user_tools (user_id, tools) VALUES (?, ?)",
            (user_id, json.dumps(selected_tools))
        )

    conn.commit()
    conn.close()

    original_tools = Tool().tools
    filtered_tools = [tool for tool in original_tools if tool.name in selected_tools]

    state["tools"]=filtered_tools
    print(f"""\nState updated with: \n
        tools: {type(state['tools'])} {len(state['tools'])}
        """)

    print({
        "message": "Tools saved successfully",
        "tools": original_tools,
        "filtered_tools": filtered_tools,
        "filtered_tools_type": type(filtered_tools).__name__,
        "length": len(filtered_tools),
    })

    return jsonify(
        {
            "message": "Tools saved successfully",
        }
    )

@tools_bp.route("/get-selected-tools", methods=["GET"])
def get_selected_tools():
    token = request.headers.get("Authorization", "").replace("Bearer ", "")

    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id = decoded["id"]
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT tools FROM user_tools WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()

    selected_tools = json.loads(row[0]) if row else []

    return jsonify({"tools": selected_tools})
