import streamlit as st
import requests
import time

# ===== API Config =====
GEMINI_API_KEY = "AIzaSyBEXfh1wUUdCFEsT_yZ_DUyov-49mk-MDw"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
GEMINI_HEADERS = {"Content-Type": "application/json"}

USER_ACCESS_TOKEN = 'EAAQ1ZAgHKnkEBO0GPD9tThWGYI46ucucdwP1lHUwTWc8SN0g3beibIydhoQlWtTyw0mJajBs3mVrlxBrZCXUC6vVQbldULsiyypyx9zKa2R9ZBYHaENDdgGeAE6jZAZCOXOsMFjBZATxAvAILVIvbcwYMv784WtHkZCeOo7WvMlCf7tb8mprqtXjYzmtrMcWA6dunfmkxqRFZAV3NI5GN7YCPC1PZA33DD9vjOgMIcVv3O1gZD'

PAGE_ID = '599271760084973'

# ===== Functions =====
def get_page_access_token(user_token, page_id):
    url = f'https://graph.facebook.com/v22.0/{page_id}?fields=access_token&access_token={user_token}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('access_token')
    return None

def post_to_facebook(page_access_token, page_id, message):
    url = f'https://graph.facebook.com/{page_id}/feed'
    params = {'message': message, 'access_token': page_access_token}
    response = requests.post(url, params=params)
    return response.status_code == 200

def generate_gemini_response(question):
    body = {
        "contents": [ {
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
gemini_question = st.text_input("Gemini Topic (Dutch) ✍️")

if st.button("Generate & Post"):
    if not gemini_question:
        st.warning("Please fill the Gemini question.")
    else:
        with st.spinner("Generating Dutch response..."):
            response_text = generate_gemini_response(gemini_question)
        if response_text:
            st.success("Response generated:")
            st.markdown(f"**{response_text}**")
            with st.spinner("Posting to Facebook..."):
                token = get_page_access_token(USER_ACCESS_TOKEN, PAGE_ID)
                if token and post_to_facebook(token, PAGE_ID, response_text):
                    st.success("✅ Successfully posted to Facebook!")
                else:
                    st.error("❌ Failed to post to Facebook.")
        else:
            st.error("❌ Failed to get Gemini response.")
