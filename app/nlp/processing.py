import random
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

# Load the pretrained DialoGPT model and tokenizer
tokenizer = GPT2Tokenizer.from_pretrained("microsoft/DialoGPT-medium")
model = GPT2LMHeadModel.from_pretrained("microsoft/DialoGPT-medium")

tokenizer.pad_token = tokenizer.eos_token

# Set the model to evaluation mode
model.eval()

def generate_response(user_input, chat_history_ids=None):
    """
    Generate a response from the chatbot based on user input.

    :param user_input: The text input from the user.
    :param chat_history_ids: Optional conversation history for context.
    :return: A plain string response and updated chat history.
    """
    try:
        # Encode the user input with attention mask
        user_input_encoded = tokenizer(
            user_input + tokenizer.eos_token,
            return_tensors="pt",
            padding=True,
            truncation=True
        )

        new_user_input_ids = user_input_encoded["input_ids"]
        attention_mask = user_input_encoded["attention_mask"]

        # Append the new input to the chat history (for context)
        if chat_history_ids is not None:
            input_ids = torch.cat([chat_history_ids, new_user_input_ids], dim=-1)
            attention_mask = torch.cat(
                [torch.ones(chat_history_ids.shape, dtype=torch.long), attention_mask], dim=-1
            )
        else:
            input_ids = new_user_input_ids

        # Generate a response using the model
        chat_history_ids = model.generate(
            input_ids,
            max_length=1000,
            pad_token_id=tokenizer.eos_token_id,
            do_sample=True,  # Enable sampling
            top_p=0.92,
            temperature=0.7,
            attention_mask=attention_mask  # Pass the attention mask
        )

        # Decode the generated response into a plain string
        chat_response = tokenizer.decode(chat_history_ids[:, input_ids.shape[-1]:][0], skip_special_tokens=True)
        
        return chat_response, chat_history_ids

    except Exception as e:
        return f"Error: {str(e)}", chat_history_ids

def process_user_input(text, chat_history_ids=None):
    """
    Process the user's input, normalize it, and generate a response.
    Uses DialoGPT for context-aware conversation generation.

    :param text: The user's input message.
    :param chat_history_ids: Optional conversation history to maintain context.
    :return: A chatbot response with optional updated chat history.
    """
    try:
        # Basic tokenization and normalization
        normalized_text = text.strip().lower()

        # Otherwise, generate a response using DialoGPT
        response, chat_history_ids = generate_response(normalized_text, chat_history_ids)

        return response, chat_history_ids

    except Exception as e:
        return f"Error processing input: {e}", chat_history_ids