import google.generativeai as genai
import streamlit as st

# Configure the Gemini API
def genAI(user_prompt):
    # Configure the API key for the generative AI service
    genai.configure(api_key="AIzaSyBEXfh1wUUdCFEsT_yZ_DUyov-49mk-MDw")

    # Initialize the generative model (make sure the model name is correct)
    model = genai.GenerativeModel("gemini-1.5-flash")

    # Request the AI to generate content based on the user-provided prompt
    response = model.generate_content(user_prompt)

    # Return the AI's response text
    return response.text

# Streamlit Web App
def main():
    # Custom HTML and CSS for the app's layout and animation
    st.markdown("""
    <style>
        body {
            background-color: #f7f8fa;
            font-family: 'Roboto', sans-serif;
            margin: 0;
            padding: 0;
        }
        .container {
            width: 100%;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            box-sizing: border-box;
        }
        .header {
            text-align: center;
            font-size: 3em;
            font-weight: 700;
            color: #00bfae;
            text-transform: uppercase;
            animation: fadeIn 2s ease-out;
        }
        .description {
            text-align: center;
            font-size: 1.2em;
            margin-top: 20px;
            color: #333;
            animation: fadeIn 2s ease-out;
        }
        .message-input {
            width: 100%;
            max-width: 600px;
            margin: 20px auto;
            padding: 15px;
            font-size: 1.1em;
            border-radius: 8px;
            border: 1px solid #ccc;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease-in-out;
        }
        .message-input:focus {
            outline: none;
            border-color: #00bfae;
            box-shadow: 0 0 8px rgba(0, 191, 174, 0.6);
        }
        .button {
            background-color: #00bfae;
            color: white;
            font-size: 1.2em;
            padding: 15px 30px;
            border: none;
            border-radius: 50px;
            cursor: pointer;
            margin-top: 20px;
            transition: all 0.3s ease;
            display: block;
            margin-left: auto;
            margin-right: auto;
        }
        .button:hover {
            background-color: #008e82;
        }
        .result {
            text-align: center;
            font-size: 1.5em;
            margin-top: 30px;
            color: #333;
            animation: fadeIn 1s ease-out;
        }
        .result span {
            font-weight: bold;
        }
        .suggestion {
            background-color: #f0f8f0;
            padding: 20px;
            border-radius: 8px;
            margin-top: 30px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .suggestion h3 {
            font-size: 1.5em;
            color: #00bfae;
            margin-bottom: 15px;
        }
        .suggestion p {
            font-size: 1.1em;
            color: #555;
        }
        @keyframes fadeIn {
            from {
                opacity: 0;
            }
            to {
                opacity: 1;
            }
        }
        .animation {
            animation: fadeIn 1s ease-out;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # App container
    with st.container():
        # Header with animation
        st.markdown('<div class="header">SMS Spam Detection with AI Suggestions</div>', unsafe_allow_html=True)

        # Description
        st.markdown('<div class="description">Enter an SMS message, and the tool will predict if it\'s spam or not using Gemini AI. Additionally, Gemini AI will provide suggestions for improving the message.</div>', unsafe_allow_html=True)

        # User input for message
        message = st.text_area("Enter SMS message:", "Type here...", key="input_message", height=150)

        # Check for spam button
        if st.button("Check if Spam", key="check_spam"):
            if message:
                # Send the message to Gemini AI for spam detection
                ai_prompt = f"Is the following message spam or not? Respond with 'Spam' or 'Not Spam': {message}"
                ai_response = genAI(ai_prompt)
                result = ai_response.strip()  # Extracting the response from Gemini

                # Set score based on AI response
                if result.lower() == 'spam':
                    score = "Poor"
                elif result.lower() == 'not spam':
                    score = "Good"
                else:
                    score = "Uncertain"

                # Additional Metrics
                words = len(message.split())
                read_time = round(words / 2)

                # Gemini AI: Generate improvement suggestions
                ai_suggestion = genAI(f"Provide suggestions for improving this message: '{message}'")
                
                # Display result with animation
                st.markdown(f'<div class="result">The message is: <span>{result}</span></div>', unsafe_allow_html=True)
                st.markdown(f'<div class="result">Overall score: <span>{score}</span></div>', unsafe_allow_html=True)
                st.write(f"Words: {words}")
                st.write(f"Read time: {read_time} seconds")

                # Display AI suggestion with styling
                st.markdown(f'<div class="suggestion"><h3>AI Suggestion for Improving the Message:</h3><p>{ai_suggestion}</p></div>', unsafe_allow_html=True)

            else:
                st.warning("Please enter a message.")

if __name__ == '__main__':
    main()
