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

# Step 1: Get Page Access Token
def get_page_access_token(user_token, page_id):
    url = f'https://graph.facebook.com/v22.0/{page_id}?fields=access_token&access_token={user_token}'
    response = requests.get(url)
    
    if response.status_code == 200:
        page_data = response.json()
        return page_data.get('access_token')
    else:
        st.error("Error in getting page access token: " + response.json())
        return None

# Step 2: Post the image and message to Facebook
def post_to_facebook(page_access_token, page_id, message, image_data):
    url = f'https://graph.facebook.com/{page_id}/photos'
    files = {'file': image_data}
    params = {
        'message': message,
        'access_token': page_access_token
    }
    response = requests.post(url, params=params, files=files)
    
    if response.status_code == 200:
        st.success("Post successful!")
    else:
        st.error(f"Error in posting: {response.json()}")

# Step 3: Generate image using Hugging Face API
def generate_image(image_prompt):
    payload = {"inputs": image_prompt, "options": {"wait_for_model": True}}
    retries = 3
    for attempt in range(retries):
        try:
            st.write(f"Attempt {attempt + 1}: Generating Image...")
            img_response = requests.post(HF_API_URL, headers=HF_HEADERS, json=payload, timeout=60)
            if img_response.status_code == 200:
                return img_response.content
            else:
                st.warning(f"⚠️ Status {img_response.status_code}: Retrying...")
        except Exception as e:
            st.error(f"❌ Image Gen Error: {e}")
        time.sleep(5)
    st.error("❌ Image generation failed after multiple attempts.")
    return None

# Step 4: Get Gemini text response in Dutch
def generate_gemini_response(question):
    gemini_body = {
        "contents": [({
            "parts": [{"text": f"Beantwoord dit in het Nederlands: {question}"}]
        })]
    }
    try:
        gemini_response = requests.post(GEMINI_URL, headers=GEMINI_HEADERS, json=gemini_body)
        if gemini_response.status_code == 200:
            data = gemini_response.json()
            content_text = data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "Geen inhoud beschikbaar.")
            return content_text
        else:
            st.error(f"Error in Gemini API response: {gemini_response.text}")
            return None
    except Exception as e:
        st.error(f"❌ Gemini Request Error: {e}")
        return None

# Streamlit interface
def main():
    st.title("Image Generation and Text Response in Dutch")
    
    # Get user input for both image prompt and Gemini question
    image_prompt = st.text_input("Enter a prompt for image generation:")
    gemini_question = st.text_area("Enter a question/topic for Gemini (response in Dutch):")
    
    if image_prompt.strip() or gemini_question.strip():
        if image_prompt.strip():
            # Generate the image
            image_bytes = generate_image(image_prompt)
            if image_bytes:
                filename = f"image_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                with open(filename, 'wb') as img_file:
                    img_file.write(image_bytes)
                st.image(image_bytes, caption="Generated Image", use_column_width=True)
                st.download_button(label="Download Image", data=image_bytes, file_name=filename)
            else:
                st.error("Failed to generate the image.")
        
        if gemini_question.strip():
            gemini_response = generate_gemini_response(gemini_question)
            if gemini_response:
                st.subheader("Gemini Response (in Dutch):")
                st.write(gemini_response)

                # Get the Facebook page access token
                page_access_token = get_page_access_token(USER_ACCESS_TOKEN, PAGE_ID)
                if page_access_token:
                    post_to_facebook(page_access_token, PAGE_ID, gemini_response, image_bytes)

if __name__ == "__main__":
    main()
