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
    st.title("SMS Spam Detection with AI Suggestions")

    st.markdown(""" 
    This is a spam detection tool for SMS messages. 
    Enter a message, and the tool will predict if it's spam or not using Gemini AI.
    Additionally, Gemini AI will provide suggestions on improving or modifying the text.
    """)
    
    # User input
    message = st.text_area("Enter SMS message:", "Type here...")

    if st.button("Check if Spam"):
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
            
            # Display results
            st.success(f'The message is: {result}')
            st.markdown(f"Overall score: {score}")
            st.write(f"Words: {words}")
            st.write(f"Read time: {read_time} seconds")

            # Display AI suggestion
            st.markdown("**AI Suggestion for Improving the Message:**")
            st.write(ai_suggestion)

        else:
            st.warning("Please enter a message.")

if __name__ == '__main__':
    main()
