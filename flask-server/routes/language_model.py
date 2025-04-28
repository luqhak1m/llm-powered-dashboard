
from flask import Blueprint, request, jsonify
from module.state import state
import json

data_source_bp=Blueprint('language-model', __name__)

@data_source_bp.route("llm-details", methods=["GET"])
def getLLMDetails():

    model_name=state.llm.model_name
    prompt=state.prompt

    try:
        return jsonify(
            {
                "model_name": model_name,
                "system_prompt": prompt
            }
        ), 200
    except:
        return jsonify(
            {
                "error": "No model loaded"
            }
        ), 400
    