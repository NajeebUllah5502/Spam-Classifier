import streamlit as st
import google.generativeai as genai

# Set your Gemini API key securely
GEMINI_API_KEY = "AIzaSyCU4iur7NQz1PGZ4DXTXCjndrsENh3IDIE"
genai.configure(api_key=GEMINI_API_KEY)

# Initialize the Gemini 1.5 Pro model
model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest")

# Function to get a response from Gemini
def ask_chatbot(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {e}"

# Streamlit UI
st.set_page_config(page_title="Drug & Alcohol Counseling Chatbot", page_icon="🎓")

st.title("🎓 Drug & Alcohol Counseling Study Chatbot")
st.write("Ask any question related to counseling studies. Type below:")

# Chat input
user_input = st.text_input("You:", "")

if user_input:
    with st.spinner("Thinking..."):
        response = ask_chatbot(user_input)
        st.markdown(f"**Chatbot:** {response}")
