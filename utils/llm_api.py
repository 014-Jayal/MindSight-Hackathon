# import os
# import google.generativeai as genai

# genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
import streamlit as st # Import Streamlit
import google.generativeai as genai

# This line reads from Streamlit's secure Secrets manager
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# The base system prompt remains the same
BASE_SYSTEM_PROMPT = """
You are MindSight, a caring and supportive AI wellness companion. 
Your goal is to listen, provide a safe space for reflection, and offer gentle encouragement.
- Be empathetic, kind, and patient.
- Never give medical advice, diagnoses, or treatment plans.
- If the user expresses thoughts of self-harm or crisis, do not offer solutions. 
  Instead, gently and immediately guide them to seek professional help...
- Keep your responses thoughtful but not excessively long.
"""

def get_ai_response(conversation_history):
    """
    Initializes the model with the conversation history (which includes the proactive insight) 
    and gets the next response.
    """
    try:
        # The system prompt is the first message in the history
        system_instruction = conversation_history[0]['content']
        
        # The actual chat history starts from the second message
        history_for_api = [
            {"role": "user" if msg["role"] == "user" else "model", "parts": [msg["content"]]}
            for msg in conversation_history if msg["role"] in ["user", "assistant"]
        ]
        
        # Initialize the model with the potentially updated system prompt
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=system_instruction
        )
        
        # Pop the last user message to send it
        last_user_message = history_for_api.pop()['parts'][0]
        
        # Start the chat with the preceding history
        chat = model.start_chat(history=history_for_api)
        response = chat.send_message(last_user_message)
        
        return response.text
    except Exception as e:
        return f"Sorry, I'm having trouble connecting. Error: {e}"