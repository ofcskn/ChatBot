from flask import Blueprint, request, jsonify
from app.nlp.processing import process_user_input

bp = Blueprint('api', __name__)

@bp.route('/chat', methods=['POST'])
def chat():
    try:
        # Get the user input from the POST request
        user_input = request.json.get('message', '')
        if not user_input:
            return jsonify({"error": "No input provided"}), 400

        # Process the input
        response = process_user_input(user_input)
        return jsonify({"response": response}), 200
    except Exception as e:
        # Handle errors and return a helpful response
        return jsonify({"error": str(e)}), 500
