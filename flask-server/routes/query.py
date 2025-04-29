from flask import Blueprint, request, jsonify
from module.state import state

query_bp=Blueprint("query", __name__)

@query_bp.route("/query-input", methods=["POST"])
def getQuery():    
    '''
    The processes from getting the input to generating the visualziation
    '''

    try:
        data=request.get_json()

        query=data.get("query")
        # print(query)

        state.question=query
        print(f"state.question set! {state.question}")

        state.writeQuery()
        print(f"state.query set! {state.query}")

        state.executeQuery()
        print(f"state.result set! {state.result}")

        state.generateDF()
        print(f"state.data set! {state.data}")
        
        state.chooseVisualization()
        print(f"state.visualization set! {state.visualization}")

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

