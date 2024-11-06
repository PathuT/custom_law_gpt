import os
from dotenv import load_dotenv  # Ensure this line is included
import streamlit as st
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

# Configure the Gemini API
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Create the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
    system_instruction=(
        "You are an expert in laws and your role is to assist junior counsels and law students. "
        "Your task is to engage in conversations about law, answer legal questions, and provide "
        "real-time information on case law based on user input queries. Ensure that your explanations are clear "
        "and precise, using legal terminology in a way that is understandable for your audience. Provide accurate, "
        "fast, and user-friendly responses using the Gemini API. Aim to help users strengthen their legal knowledge "
        "by offering relevant case law examples and practical applications. Also provide some real example cases "
        "related to the questions asked remember that strictly no other topics if I ask you other out of the topic "
        "questions do not respond."
    ),
)

# Streamlit app layout
st.set_page_config(page_title="Criminal Law Assistant", layout="centered")
st.title("Criminal Law Assistant")
st.write("Welcome! Ask any question related to criminal law and view the conversation history below.")

# Initialize session state for conversation history
if "history" not in st.session_state:
    st.session_state.history = []

# Define a callback function to clear user input
def clear_input():
    st.session_state.user_input = ""

# Input box for user query with session state
user_input = st.text_input("Your Question:", placeholder="Type your question here...", key="user_input")

# Display conversation history
st.subheader("Conversation History")
if st.session_state.history:
    for i, (question, answer) in enumerate(st.session_state.history):
        st.markdown(f"**You**: {question}")
        st.markdown(f"**Assistant**: {answer}")
        st.markdown("---")

# Submit button interaction with a callback to clear input
if st.button("Submit", on_click=clear_input):
    if user_input:
        # Start a chat session
        chat_session = model.start_chat(history=[])
        response = chat_session.send_message(user_input)

        # Display the response
        st.write("Response:")
        st.write(response.text)

        # Save to conversation history
        st.session_state.history.append((user_input, response.text))
    else:
        st.warning("Please enter a question before submitting.")

# Add some custom styles for better UI
st.markdown(
    """
    <style>
    div[data-testid="stTextInput"] > div:first-child {
        border-radius: 10px;
        border: 1px solid #D3D3D3;
        padding: 10px;
    }
    div[data-testid="stButton"] > button {
        background-color: #4CAF50;
        color: white;
        border-radius: 5px;
        padding: 10px 20px;
    }
    .stMarkdown { margin-top: 10px; }
    </style>
    """,
    unsafe_allow_html=True
)
