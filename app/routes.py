from flask import Blueprint, request, jsonify
from app.config.admin_config import AdminConfig
from app.nlp.processing import process_user_input

bp = Blueprint('api', __name__)

chat_histories = {}

@bp.route('/chat', methods=['POST'])
def chat():
    """
    Chatbot route to process user input.
    """
    try:
        data = request.json
        user_id = data.get("user_id", "0") # get the user_id (default = 0)
        print("user_id:", user_id)

        user_input = data.get('message', '')

        if not user_input:
            return jsonify({"error": "No input provided"}), 400
        
        # Retrieve or initialize chat history
        chat_history_ids = chat_histories.get(user_id, None)
        
        # Fetch admin-configured chatbot details
        chatbot_name = AdminConfig.CHATBOT_NAME

        # Process the user input and get the normalized response
        response, chat_history_ids = process_user_input(user_input, chat_history_ids)
        
        # Save chat_history_ids to the memory for a while
        chat_histories[user_id] = chat_history_ids  # Save updated history

        # Formulate the chatbot's full response
        response = {
            "chatbot_name": chatbot_name,
            "response": response
        }
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500