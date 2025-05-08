
import time
from flask import Blueprint, request, jsonify, Response
from module.state import StateMethods, state, graph, graphVisual

query_bp=Blueprint("query", __name__)
final_state=None

@query_bp.route("/query-input", methods=["POST"])
def setQuery():    
    '''
    The processes from getting the input to generating the visualziation
    '''

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
    try:
        return jsonify(
            {
                "question": state["question"],
                "query": state["query"],
                "result": state["result"],
                "data": state["data"],
                "analysis": state["analysis"],
                "visualization": str(state["visualization"]) if state["visualization"] is not None else None,""
                "routerCount": state["routerCount"],
            }
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
                "llm": str(state["llm"]),
                "prompt": str(state["prompt"]),
                "tools": str(state["tools"]),
                
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

    