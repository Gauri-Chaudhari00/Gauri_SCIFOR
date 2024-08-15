# Libraries
import streamlit as st

import google.generativeai as gen_ai
from dotenv import load_dotenv
import os


# Load environment variables
load_dotenv()



# Streamlit page configuration
st.set_page_config(
    page_title=" Gemini",
    page_icon=":gem:",
    layout="wide",  # Changed to wide for more space
    initial_sidebar_state="expanded"
)

st.title("My Chatbot App")
st.write("Hello, world!")

# Retrieve API key from environment variables
GOOGLE_API_KEY = os.getenv("GoogleAPI")


gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-pro')



# Display the image at the top
#st.image("gemini.pro", use_column_width=True)

# Streamlit app title with styling
st.markdown("<h1 style='text-align: center;'>Hello, How can I help you?</h1>", unsafe_allow_html=True)

# Set up Google Gemini-pro AI model
#gen_ai.configure(api_key=GOOGLE_API_KEY)
#model = gen_ai.GenerativeModel('gemini-pro')

# Function to translate roles between Gemini-Pro and Streamlit terminology
def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role

# Initialize chat session in Streamlit if not already present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])


# Add a new chat icon in the sidebar
st.sidebar.title(":blue[NEW CHAT]")
if st.sidebar.button("💬 Start New Chat"):
    st.session_state.chat_session = model.start_chat(history=[])

# Sidebar for session history and controls
st.sidebar.title(":blue[SESSION HISTORY]")
st.sidebar.download_button("⬇️ Download History", data=str(st.session_state.chat_session.history), file_name="chat_history.txt")

# Display chat history with styling
for message in st.session_state.chat_session.history:
    role = translate_role_for_streamlit(message.role)
    with st.chat_message(role):
        if role == "assistant":
            st.markdown(f"{message.parts[0].text}", unsafe_allow_html=True)
        else:
            st.markdown(f"{message.parts[0].text}", unsafe_allow_html=True)

# User input for chat with loading animation
user_input = st.chat_input("Ask Gemini.....")
if user_input:
    with st.spinner("Thinking..."):
        # Display user's message
        st.chat_message("user").markdown(user_input)

        # Get and display Gemini-Pro's response
        response = st.session_state.chat_session.send_message(user_input)
        with st.chat_message("assistant"):
            st.markdown(response.text)
            

# Feedback system with smiley faces
st.sidebar.title(":blue[FEEDBACK]")
feedback = st.sidebar.radio("Was the response helpful?", ("🙂 Yes", "😞 No"))
if feedback.startswith("🙂"):
    st.sidebar.success("Thank you for your feedback!")
elif feedback.startswith("😞"):
    st.sidebar.warning("Sorry to hear that. We'll try to improve.")
    