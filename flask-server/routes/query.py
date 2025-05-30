
import time
from flask import Blueprint, request, jsonify, Response
from module.state import StateMethods, state, graph, graphVisual
import jwt
import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

query_bp=Blueprint("query", __name__)
final_state=None

@query_bp.route("/query-input", methods=["POST"])
def setQuery():    
    '''
    The processes from getting the input to generating the visualziation
    '''

    global final_state


    try:

        data=request.get_json()
        question=data.get("question")

        StateMethods.clearState(state)
        state["question"]=question
        print(f"state.question set! {type(state['question'])}")

        final_state = graph.invoke(state)
        state["visualization"] = final_state.get("visualization")
        state["analysis"] = final_state.get("analysis")
        print(final_state)

        return jsonify(
            {
                "status": "success"
            }
        ), 200
    
    except Exception as e:
        return jsonify(
            {
                "error": f"{e}"
            }
        ), 400

@query_bp.route("/state-details", methods=["GET"])
def getStateDetails():

    global final_state

    try:
        toBeSent={
                "question": final_state["question"],
                "query": final_state["query"],
                "result": final_state["result"],
                "data": final_state["data"],
                "analysis": final_state["analysis"],
                "visualization": str(final_state["visualization"]) if final_state["visualization"] is not None else None,
                "routerCount": final_state["routerCount"],
                "retry": final_state["retry"],
                "SQLValidity": final_state["SQLValidity"]
            }
        
        print(f"tobesent: {toBeSent}")
        return jsonify(
            toBeSent
        )
    except Exception as e:
        return jsonify(
            {
                "error": f"{e}"
            }
        ), 500
    
@query_bp.route("/llm-details", methods=["GET"])
def getLLMDetails():
    try:
        return jsonify(
            {
                "model": str(state["model"]),                
            }
        )
    except Exception as e:
        return jsonify(
            {
                "error": f"{e}"
            }
        ), 500
    
@query_bp.route("/db-details", methods=["GET"])
def getDBDetails():
    try:
        return jsonify(
            {
                "db": str(state["db"]),
                "schema": str(state["schema"]),                
            }
        )
    except Exception as e:
        return jsonify(
            {
                "error": f"{e}"
            }
        ), 500
    
@query_bp.route("/generated-visual")
def getVisual():
    print("Returning visualization:", state["visualization"])
    return state["visualization"], 200, {"Content-Type": "text/html"}

@query_bp.route("/generated-analysis")
def getAnalysis():
    print("Returning analysis:", (state["analysis"]))
    return state["analysis"], 200,

@query_bp.route("/generated-graph")
def get_graph():
    return Response(graphVisual, mimetype="image/png")

@query_bp.route("/save-visual", methods=["POST"])
def save_visual():
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id = decoded["id"]
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401
    
    if not state["visualization"] or not state["analysis"] or not state["question"]:
        print("No visualization, analysis, or prompt to save")
        return jsonify({"error": "No visualization, analysis, or prompt to save"}), 400
    
    prompt=state["question"]
    visualization = str(state["visualization"])
    analysis = str(state["analysis"])

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO saved_visuals (user_id, prompt, visualization, analysis) VALUES (?, ?, ?, ?)",
        (user_id, prompt, visualization, analysis)
    )
    conn.commit()
    conn.close()

    return jsonify({"message": "Saved successfully"}), 200


@query_bp.route("/saved-visuals", methods=["GET"])
def get_saved_visuals():
	token = request.headers.get("Authorization", "").replace("Bearer ", "")
	try:
		decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
		user_id = decoded["id"]
	except jwt.InvalidTokenError:
		return jsonify({"error": "Invalid token"}), 401

	conn = sqlite3.connect("users.db")
	cursor = conn.cursor()
	cursor.execute(
		"SELECT id, prompt, visualization, analysis, timestamp FROM saved_visuals WHERE user_id = ? ORDER BY timestamp DESC",
		(user_id,)
	)
	rows = cursor.fetchall()
	conn.close()

	data = [
		{
			"id": row[0],
			"prompt": row[1],
			"visualization": row[2],
			"analysis": row[3],
			"timestamp": row[4]
		}
		for row in rows
	]

	return jsonify(data), 200

@query_bp.route("/saved-visuals/<int:visual_id>", methods=["GET"])
def get_saved_visual_by_id(visual_id):
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id = decoded["id"]
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, prompt, visualization, analysis, timestamp FROM saved_visuals WHERE id = ? AND user_id = ?",
        (visual_id, user_id)
    )
    row = cursor.fetchone()
    conn.close()

    if not row:
        return jsonify({"error": "Not found"}), 404

    data = {
        "id": row[0],
        "prompt": row[1],
        "visualization": row[2],
        "analysis": row[3],
        "timestamp": row[4]
    }
    print("Returning saved visual:", data)
    return jsonify(data), 200