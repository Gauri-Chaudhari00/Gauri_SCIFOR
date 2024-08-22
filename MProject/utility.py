import os
from io import BytesIO
import speech_recognition as sr
from gtts import gTTS
import streamlit as st

def speech_to_text(audio_path):
    """
    Convert speech in an audio file to text using Google Web Speech API.

    Args:
        audio_path (str): Path to the audio file.

    Returns:
        str: Transcribed text or an error message.
    """
    r = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio_data = r.record(source)
        try:
            return r.recognize_google(audio_data)
        except sr.UnknownValueError:
            return "Sorry, I did not understand that."
        except sr.RequestError:
            return "Sorry, the service is unavailable at the moment."

def convert_history(history):
    """
    Convert conversation history to a format compatible with the AI model.

    Args:
        history (list of tuples): Conversation history.

    Returns:
        list of dicts: Formatted conversation history.
    """
    converted = []
    for role, text in history:
        if role == "user":
            converted.append({"parts": [{"text": text}], "role": "user"})
        elif role == "model":
            converted.append({"parts": [{"text": text}], "role": "model"})
    return converted

def generate_welcome_message():
    """
    Generate a welcome message for the chatbot.

    Returns:
        str: Welcome message.
    """
    return "Hello! Welcome to Gemini Chatbot! How may I help you today?"

def process_audio_data(audio_data, model):
    """
    Process audio data: Convert speech to text, interact with AI model, and generate TTS response.

    Args:
        audio_data (bytes): Recorded audio data.
        model: AI model for generating responses.

    Returns:
        dict: Response text and audio.
    """
    with BytesIO(audio_data) as audio_file:
        temp_audio_path = "temp_audio.wav"
        with open(temp_audio_path, "wb") as f:
            f.write(audio_file.read())
        
        user_prompt = speech_to_text(temp_audio_path)
        conversation_history = convert_history(st.session_state.conversation)
        
        try:
            chat_session = model.start_chat(history=conversation_history)
            gemini_answer = chat_session.send_message(user_prompt)
            
            response_text = gemini_answer.text
            response_audio = BytesIO()
            gTTS(text=response_text, lang='en').write_to_fp(response_audio)
            response_audio.seek(0)
            
            return {"text": response_text, "audio": response_audio}
        except Exception as e:
            st.error(f"An error occurred: {e}")
            return {"text": "An error occurred.", "audio": BytesIO()}
        finally:
            os.remove(temp_audio_path)
