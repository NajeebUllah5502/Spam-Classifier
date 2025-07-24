# simple_qa_app.py

import streamlit as st
import requests
from bs4 import BeautifulSoup
import fitz  # PyMuPDF
from openai import OpenAI
import os
from dotenv import load_dotenv

# ================== LOAD ENV ==================
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    st.error("❌ OpenAI API key not found. Please set it in your .env file or environment variables.")
    st.stop()

client = OpenAI(api_key=OPENAI_API_KEY)

# ================== CONFIG ==================
PDF_PATH = "reading_material.pdf"
DEFAULT_URL = "https://accsc.com.au/"

# ================== SCRAPE WEBSITE ==================
def scrape_website_text(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        return soup.get_text(separator="\n", strip=True)
    except Exception as e:
        return f"❌ Error scraping website: {e}"

# ================== EXTRACT PDF TEXT ==================
def extract_text_from_pdf(path):
    try:
        doc = fitz.open(path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        return f"❌ Error reading PDF: {e}"

# ================== GET RELEVANT CONTEXT ==================
def get_relevant_context(text, query, window=500):
    query_lower = query.lower()
    index = text.lower().find(query_lower)
    if index == -1:
        return text[:1000]  # fallback: first 1000 chars
    start = max(0, index - window)
    end = min(len(text), index + window)
    return text[start:end]

# ================== ASK OPENAI GPT ==================
def ask_gpt(question, context):
    prompt = (
        "You are an assistant. Use the context below to answer the user's question.\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {question}\nAnswer:"
    )
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=500
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ OpenAI API error: {e}"

# ================== STREAMLIT UI ==================
st.set_page_config(page_title="Simple Q&A | PDF + Website", layout="wide")
st.title("📘 Simple AI Q&A from Website + PDF")

with st.sidebar:
    st.header("📄 Upload & Settings")
    uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")
    website_url = st.text_input("Website URL", value=DEFAULT_URL)

    if uploaded_file:
        with open("temp_uploaded.pdf", "wb") as f:
            f.write(uploaded_file.read())
        PDF_PATH = "temp_uploaded.pdf"

# Load and combine content
with st.spinner("📥 Loading website and PDF content..."):
    website_text = scrape_website_text(website_url)
    pdf_text = extract_text_from_pdf(PDF_PATH)

combined_text = website_text + "\n" + pdf_text
st.success("✅ Loaded. Ask your question below.")

# ================== ASK QUESTION ==================
user_question = st.text_input("💬 Ask a question:")
if user_question:
    with st.spinner("🤖 Thinking..."):
        context = get_relevant_context(combined_text, user_question)
        answer = ask_gpt(user_question, context)

        st.markdown("### ✅ Answer")
        st.write(answer)

        with st.expander("📄 Context Used for Answer"):
            st.code(context)
