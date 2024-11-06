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
        "Your task is to engage in conversations about  law, answer legal questions, and provide "
        "real-time information on case law based on user input queries. Ensure that your explanations are clear "
        "and precise, using legal terminology in a way that is understandable for your audience. Provide accurate, "
        "fast, and user-friendly responses using the Gemini API. Aim to help users strengthen their legal knowledge "
        "by offering relevant case law examples and practical applications. Also provide some real example cases "
        "related to the questions asked remember that strictly no other topics if I ask you other out of the topic "
        "questions do not respond."
    ),
)
# Streamlit app layout
st.title("Criminal Law Assistant")
st.write("Ask any question related to criminal law:")
# Input box for user query
user_input = st.text_input("Your Question:")
if st.button("Submit"):
    if user_input:
        chat_session = model.start_chat(history=[])
        response = chat_session.send_message(user_input)
        st.write("Response:")
        st.write(response.text)
    else:
        st.warning("Please enter a question before submitting.")