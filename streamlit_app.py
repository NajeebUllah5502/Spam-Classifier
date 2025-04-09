import streamlit as st
import requests
import time
from datetime import datetime

# ===== API Config =====
HF_API_URL = "https://api-inference.huggingface.co/models/prompthero/openjourney"
HF_API_TOKEN = "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"
HF_HEADERS = {"Authorization": f"Bearer {HF_API_TOKEN}"}

GEMINI_API_KEY = "AIzaSyBEXfh1wUUdCFEsT_yZ_DUyov-49mk-MDw"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
GEMINI_HEADERS = {"Content-Type": "application/json"}

USER_ACCESS_TOKEN = 'EAAQ1ZAgHKnkEBOZCMqeeQ5ty4ZAAOCPgIw9yMaHXfMmDZCBZBSxXPrChkfTWqmdpXB9yL00Vj1ljxv6fsmAZA0u7x966CzzGuf48PKmzpLjqvZCIXE3Y39XJSe4vm0HGplSxZAlaaUXqlXOAPmMHvAhEPgVdrjDNz3OgVnABgZCcmncjZCrrSgVhYEEGHnUHsdyraf4HeC1ZAdEzNbiAohPS5S4H5RZCiRKze0ZB8m1ZCFSZCy9FQkZD'
PAGE_ID = '599271760084973'

# ===== Functions =====
def get_page_access_token(user_token, page_id):
    url = f'https://graph.facebook.com/v22.0/{page_id}?fields=access_token&access_token={user_token}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('access_token')
    return None

def post_to_facebook(page_access_token, page_id, message, image_data):
    url = f'https://graph.facebook.com/{page_id}/photos'
    files = {'file': ('image.png', image_data, 'image/png')}
    params = {'message': message, 'access_token': page_access_token}
    response = requests.post(url, params=params, files=files)
    return response.status_code == 200

def generate_image(prompt):
    payload = {"inputs": prompt, "options": {"wait_for_model": True}}
    for _ in range(3):
        try:
            r = requests.post(HF_API_URL, headers=HF_HEADERS, json=payload, timeout=60)
            if r.status_code == 200:
                return r.content
        except Exception:
            time.sleep(5)
    return None

def generate_gemini_response(question):
    body = {
        "contents": [{
            "parts": [{"text": f"Beantwoord dit in het Nederlands: {question}"}]
        }]
    }
    try:
        r = requests.post(GEMINI_URL, headers=GEMINI_HEADERS, json=body)
        if r.status_code == 200:
            return r.json().get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "Geen inhoud beschikbaar.")
    except Exception:
        pass
    return None

# ===== Streamlit UI =====
st.title("AutoPoster to Facebook 🌍")
image_prompt = st.text_input("Image Prompt 🎨")
gemini_question = st.text_input("Gemini Topic (Dutch) ✍️")

if st.button("Generate & Post"):
    if not image_prompt or not gemini_question:
        st.warning("Please fill both fields.")
    else:
        with st.spinner("Generating image..."):
            image_data = generate_image(image_prompt)
        if image_data:
            st.image(image_data, caption="Generated Image", use_column_width=True)
            with st.spinner("Generating Dutch response..."):
                response_text = generate_gemini_response(gemini_question)
            if response_text:
                st.success("Response generated:")
                st.markdown(f"**{response_text}**")
                with st.spinner("Posting to Facebook..."):
                    token = get_page_access_token(USER_ACCESS_TOKEN, PAGE_ID)
                    if token and post_to_facebook(token, PAGE_ID, response_text, image_data):
                        st.success("✅ Successfully posted to Facebook!")
                    else:
                        st.error("❌ Failed to post to Facebook.")
            else:
                st.error("❌ Failed to get Gemini response.")
        else:
            st.error("❌ Failed to generate image.")
