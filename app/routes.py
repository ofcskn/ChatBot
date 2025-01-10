from flask import Blueprint, request, jsonify
from app.config.admin_config import AdminConfig
from app.nlp.processing import process_user_input

bp = Blueprint('api', __name__)

@bp.route('/chat', methods=['POST'])
def chat():
    """
    Chatbot route to process user input.
    """
    try:
        user_input = request.json.get('message', '')
        if not user_input:
            return jsonify({"error": "No input provided"}), 400
        
        # Fetch admin-configured chatbot details
        chatbot_name = AdminConfig.CHATBOT_NAME
        welcome_message = AdminConfig.WELCOME_MESSAGE

        # Process the user input and get the normalized response
        response, chat_history_ids = process_user_input(user_input)

        # Formulate the chatbot's full response
        response = {
            "chatbot_name": chatbot_name,
            "response": response
        }
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500