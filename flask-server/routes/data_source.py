
from flask import Blueprint, request, jsonify
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from urllib.parse import quote_plus


data_source_bp=Blueprint('data-source', __name__)

@data_source_bp.route("/db-connection", methods=["POST"])
def ValidateConnection():

    data=request.get_json()

    username=data.get("username")
    host=data.get("host")
    database=data.get("database")
    password=quote_plus(data.get("password"))

    db_uri = f"mysql+mysqlconnector://{username}:{password}@{host}/{database}"
    print(db_uri)

    try:
        engine = create_engine(db_uri)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return jsonify({"message": "Connection successful"}), 200
    except OperationalError as e:
        return jsonify({"error": "Connection failed", "details": str(e)}), 500