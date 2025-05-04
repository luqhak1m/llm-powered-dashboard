
import time
from flask import Blueprint, request, jsonify, Response
from module.state import state, graph, graphVisual

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

        state["question"]=question
        print(f"state.question set! {type(state['question'])}")

        final_state = graph.invoke(state)
        state["visualization"] = final_state.get("visualization")
        print(final_state)

        # print(query)
        

        # # -- SQL generation
        # start_sql = time.time()
        # state.writeQuery()
        # end_sql = time.time()
        # print(f"state.query set! {state.query}")
        # print(f"⏱ SQL generation took {end_sql - start_sql:.2f} sec")

        # # -- Execute SQL
        # start_exec = time.time()
        # state.executeQuery()
        # end_exec = time.time()
        # print(f"state.result set! {state.result}")
        # print(f"⏱ SQL execution took {end_exec - start_exec:.2f} sec")

        # # -- Generate dict (DataFrame-like structure)
        # start_df = time.time()
        # state.generateDF()
        # end_df = time.time()
        # print(f"state.data set! {state.data}")
        # print(f"⏱ Dict (DF) generation took {end_df - start_df:.2f} sec")

        # # -- Choose visualization
        # start_vis = time.time()
        # state.chooseVisualization()
        # end_vis = time.time()
        # print(f"state.visualization set! {state.visualization}")
        # print(f"⏱ Visualization choice took {end_vis - start_vis:.2f} sec")

        # # -- Generate Analysis
        # start_vis = time.time()
        # state.generateAnalysis()
        # end_vis = time.time()
        # print(f"state.analysis set! {state.analysis}")
        # print(f"⏱ Analysis generation took {end_vis - start_vis:.2f} sec")

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

@query_bp.route("/query-output", methods=["GET"])
def getStateAttr():
    try:
        return jsonify(
            {
                "db": str(state["db"]) if state["db"] is not None else None,
                "llm": str(state["llm"].model_name) if state["llm"].model_name is not None else None,
                "schema": state["schema"],
                "prompt": str(state["prompt"]) if state["prompt"] is not None else None,
                "question": state["question"],
                "query": state["query"],
                "result": state["result"],
                "data": state["data"],
                "tools": str(state["tools"]),
                "analysis": state["analysis"],
                "visualization": str(state["visualization"]) if state["visualization"] is not None else None
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
    # print("Returning visualization:", (state.visualization))
    return state["analysis"], 200,

@query_bp.route("/generated-graph")
def get_graph():
    return Response(graphVisual, mimetype="image/png")
    