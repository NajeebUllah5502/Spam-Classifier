import streamlit as st
import requests
import time
from datetime import datetime

# ===== Hugging Face API (Image Generation) =====
HF_API_URL = "https://api-inference.huggingface.co/models/prompthero/openjourney"
HF_API_TOKEN = "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"
HF_HEADERS = {"Authorization": f"Bearer {HF_API_TOKEN}"}

# ===== Gemini API (Text Response in Dutch) =====
GEMINI_API_KEY = "AIzaSyBEXfh1wUUdCFEsT_yZ_DUyov-49mk-MDw"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
GEMINI_HEADERS = {"Content-Type": "application/json"}

# ===== Facebook API =====
USER_ACCESS_TOKEN = 'EAAQ1ZAgHKnkEBOZCMqeeQ5ty4ZAAOCPgIw9yMaHXfMmDZCBZBSxXPrChkfTWqmdpXB9yL00Vj1ljxv6fsmAZA0u7x966CzzGuf48PKmzpLjqvZCIXE3Y39XJSe4vm0HGplSxZAlaaUXqlXOAPmMHvAhEPgVdrjDNz3OgVnABgZCcmncjZCrrSgVhYEEGHnUHsdyraf4HeC1ZAdEzNbiAohPS5S4H5RZCiRKze0ZB8m1ZCFSZCy9FQkZD'
PAGE_ID = '599271760084973'

# Functions
def get_page_access_token(user_token, page_id):
    url = f'https://graph.facebook.com/v22.0/{page_id}?fields=access_token&access_token={user_token}'
    response = requests.get(url)
    return response.json().get('access_token') if response.status_code == 200 else None

def post_to_facebook(page_access_token, page_id, message, image_data):
    url = f'https://graph.facebook.com/{page_id}/photos'
    files = {'file': image_data}
    params = {'message': message, 'access_token': page_access_token}
    response = requests.post(url, params=params, files=files)
    return response.status_code == 200

def generate_image(image_prompt):
    payload = {"inputs": image_prompt, "options": {"wait_for_model": True}}
    retries = 3
    for attempt in range(retries):
        try:
            response = requests.post(HF_API_URL, headers=HF_HEADERS, json=payload, timeout=60)
            if response.status_code == 200:
                return response.content
        except Exception as e:
            st.warning(f"Attempt {attempt + 1} failed: {e}")
        time.sleep(5)
    return None

def generate_gemini_response(question):
    body = {
        "contents": [{
            "parts": [{"text": f"Beantwoord dit in het Nederlands: {question}"}]
        }]
    }
    try:
        response = requests.post(GEMINI_URL, headers=GEMINI_HEADERS, json=body)
        if response.status_code == 200:
            return response.json().get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "Geen inhoud.")
    except Exception as e:
        st.error(f"Gemini API error: {e}")
    return None

# ===== Streamlit App =====
st.set_page_config(page_title="Image + Dutch Text Generator", layout="centered")
st.title("🖼️ Image Generator + Gemini Dutch Response")
st.write("Enter a prompt for an image and a topic/question for Gemini to answer in Dutch.")

image_prompt = st.text_input("🎨 Image Prompt")
gemini_question = st.text_input("🧠 Gemini Question (Dutch Response)")

if st.button("🚀 Generate and Show Results"):
    if image_prompt.strip() == "" and gemini_question.strip() == "":
        st.warning("⚠️ Please enter at least one prompt.")
    else:
        if image_prompt.strip():
            st.info("🔄 Generating image...")
            image_bytes = generate_image(image_prompt)
            if image_bytes:
                st.image(image_bytes, caption="Generated Image", use_column_width=True)
            else:
                st.error("❌ Failed to generate image.")
        
        if gemini_question.strip():
            st.info("🔄 Generating Dutch response from Gemini...")
            gemini_response = generate_gemini_response(gemini_question)
            if gemini_response:
                st.success("📝 Gemini Dutch Response:")
                st.write(gemini_response)
            else:
                st.error("❌ Failed to get response from Gemini.")

        # Facebook posting
        if image_prompt.strip() and gemini_question.strip() and image_bytes:
            if st.checkbox("📤 Post to Facebook"):
                st.info("Getting Facebook Page Token...")
                page_token = get_page_access_token(USER_ACCESS_TOKEN, PAGE_ID)
                if page_token:
                    st.info("Posting to Facebook...")
                    success = post_to_facebook(page_token, PAGE_ID, gemini_response, image_bytes)
                    if success:
                        st.success("✅ Posted to Facebook successfully!")
                    else:
                        st.error("❌ Failed to post to Facebook.")
                else:
                    st.error("❌ Couldn't retrieve Facebook Page Access Token.")
