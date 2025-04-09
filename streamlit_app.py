import streamlit as st
import requests
import time
from datetime import datetime
from pathlib import Path
import json

# ===== Hugging Face API (Image Generation) =====
HF_API_URL = "https://api-inference.huggingface.co/models/prompthero/openjourney"
HF_API_TOKEN = "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"
HF_HEADERS = {"Authorization": f"Bearer {HF_API_TOKEN}"}

# ===== Gemini API (Text Response in Dutch) =====
GEMINI_API_KEY = "AIzaSyBEXfh1wUUdCFEsT_yZ_DUyov-49mk-MDw"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
GEMINI_HEADERS = {"Content-Type": "application/json"}

# ===== Streamlit UI =====
st.set_page_config(page_title="🎨 AI Image & Dutch Gemini Bot", layout="centered")
st.title("🤖 Dual AI Generator")
st.markdown("Generate images using a prompt and get a Gemini answer in Dutch.")

# ---- Separate Inputs ----
image_prompt = st.text_input("🎨 Enter prompt for image generation:")
gemini_question = st.text_input("🧠 Enter question/topic (response in Dutch):")

if st.button("🚀 Generate Both"):
    if not image_prompt.strip() and not gemini_question.strip():
        st.warning("Please enter at least one prompt.")
    else:
        # ---------- Image Generation ----------
        if image_prompt.strip():
            st.subheader("🎨 AI Image Output")
            payload = {"inputs": image_prompt, "options": {"wait_for_model": True}}
            retries = 3
            for attempt in range(retries):
                with st.spinner(f"Attempt {attempt + 1}: Generating Image..."):
                    try:
                        img_response = requests.post(HF_API_URL, headers=HF_HEADERS, json=payload, timeout=60)
                        if img_response.status_code == 200:
                            image_bytes = img_response.content
                            filename = f"image_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                            st.image(image_bytes, caption="Generated Image", use_column_width=True)
                            st.download_button("⬇️ Download Image", data=image_bytes, file_name=filename, mime="image/png")
                            break
                        else:
                            st.warning(f"⚠️ Status {img_response.status_code}: Retrying...")
                    except Exception as e:
                        st.error(f"❌ Image Gen Error: {e}")
                    time.sleep(5)
            else:
                st.error("❌ Image generation failed after multiple attempts.")

        # ---------- Gemini Response in Dutch ----------
        if gemini_question.strip():
            st.subheader("🧠 Gemini Antwoord (in Dutch)")
            gemini_body = {
                "contents": [{
                    "parts": [{"text": f"Beantwoord dit in het Nederlands: {gemini_question}"}]
                }]
            }

            try:
                gemini_response = requests.post(GEMINI_URL, headers=GEMINI_HEADERS, json=gemini_body)
                if gemini_response.status_code == 200:
                    data = gemini_response.json()
                    content_text = data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "Geen inhoud beschikbaar.")
                    st.success("✅ Gemini antwoord ontvangen:")
                    st.write(content_text)
                else:
                    st.error(f"❌ Gemini API fout {gemini_response.status_code}: {gemini_response.text}")
            except Exception as e:
                st.error(f"❌ Gemini Request Error: {e}")
