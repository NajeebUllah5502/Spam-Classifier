import streamlit as st
import requests, time
from datetime import datetime
from pathlib import Path

# Constants
API_URL = "https://api-inference.huggingface.co/models/prompthero/openjourney"
API_TOKEN = "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"
HEADERS = {"Authorization": f"Bearer {API_TOKEN}"}

# Streamlit UI
st.title("🎨 AI Image Generator with Download")
prompt = st.text_input("Enter your image prompt:")

if st.button("Generate Image") and prompt:
    payload = {"inputs": prompt, "options": {"wait_for_model": True}}

    retries = 3
    for attempt in range(retries):
        with st.spinner(f"🧠 Attempt {attempt + 1} to generate image..."):
            try:
                response = requests.post(API_URL, headers=HEADERS, json=payload, timeout=60)
                if response.status_code == 200:
                    # Save image
                    image_bytes = response.content
                    filename = f"image_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"

                    # Show image
                    st.success("✅ Image generated successfully!")
                    st.image(image_bytes, caption="Generated Image", use_column_width=True)

                    # Download button
                    st.download_button(
                        label="⬇️ Download Image",
                        data=image_bytes,
                        file_name=filename,
                        mime="image/png"
                    )
                    break
                else:
                    st.warning(f"⚠️ Status {response.status_code}: Retrying...")
            except Exception as e:
                st.error(f"❌ Error: {e}")
            time.sleep(5)
    else:
        st.error("❌ All attempts failed. Try again later.")
