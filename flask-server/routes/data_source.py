
from flask import Blueprint, request, jsonify
from sqlalchemy import create_engine, text, inspect, func, select
from sqlalchemy.exc import OperationalError, SQLAlchemyError
from urllib.parse import quote_plus

connection_status={
    "status":False,
    "database_name": None,
    "engine": None
}

data_source_bp=Blueprint('data-source', __name__)

@data_source_bp.route("/db-connection", methods=["POST"])
def ValidateConnection():

    data=request.get_json()

    username=data.get("username")
    host=data.get("host")
    database=data.get("database")
    password=quote_plus(data.get("password"))

    db_uri = f"mysql+mysqlconnector://{username}:{password}@{host}/{database}"
    try:
        engine = create_engine(db_uri)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))

        connection_status["status"]=True
        connection_status["database_name"]=database
        connection_status["engine"]=engine
        
        return jsonify({"message": "Connection successful"}), 200
    except OperationalError as e:
        return jsonify({"error": "Connection failed", "details": str(e)}), 500
    
@data_source_bp.route("/db-status", methods=["GET"])
def CheckConnectionStatus():

    if connection_status["status"]:
        return jsonify(
            {
                "status": "connected",
                "databaseName": connection_status["database_name"]
            }
        ), 200
    else:
        return jsonify(
            {
                "status": "not connected",
                "databaseName": connection_status["database_name"]
            }
        ), 200


@data_source_bp.route("/db-tables", methods=["GET"])
def GetTables():
    if connection_status["status"]:
        engine=connection_status["engine"]

        inspector=inspect(engine)
        tables=inspector.get_table_names()

        return jsonify(
            {
                "databaseName": connection_status["database_name"],
                "tables": tables,
                "tablesCount": len(tables)
            }
        ), 200
    else:
        return jsonify(
            {
                "error": "No Connection"
            }
        ), 400
    
@data_source_bp.route("/db-table-preview/<table_name>", methods=["GET"])
def PreviewTable(table_name):
    if connection_status["status"]:
        engine=connection_status["engine"]

        try:

            inspector=inspect(engine)
            columns_info = inspector.get_columns(table_name)

            with engine.connect() as conn:
                preview_query = text(f"SELECT * FROM `{table_name}` LIMIT 5")
                result = conn.execute(preview_query)
                rows = [dict(row) for row in result.mappings()]
                count_query = text(f"SELECT COUNT(*) as total FROM `{table_name}`")
                total_rows = conn.execute(count_query).scalar()
            
            column_schema=[
                {
                    "name": col["name"],
                    "type": str(col["type"])
                } for col in columns_info
            ] 

            return jsonify(
                {
                    "tableName": table_name,
                    "columns": column_schema,
                    "preview": rows,
                    "rowCount": total_rows
                }
            ), 200
        
        except SQLAlchemyError as e:
            print(f"SQLAlchemyError: {str(e)}")
            return jsonify(
                {
                        "error": "Error querying table", "details": str(e)
                }
            ), 500

    else:
        return jsonify(
            {
                "error": "No Connection"
            }
        ), 400