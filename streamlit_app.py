import sqlite3
import hashlib
import streamlit as st
import google.generativeai as genai

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

# Database setup function to create the user table
def create_user_table():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        email TEXT PRIMARY KEY,
                        password TEXT)''')
    conn.commit()
    conn.close()

# Function to register a new user
def register_user(email, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # Hash the password before storing it
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    
    cursor.execute('''INSERT INTO users (email, password) VALUES (?, ?)''', (email, hashed_password))
    conn.commit()
    conn.close()

# Function to check if user credentials are valid
def check_user(email, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    
    cursor.execute('''SELECT * FROM users WHERE email = ? AND password = ?''', (email, hashed_password))
    user = cursor.fetchone()
    conn.close()
    return user

# Streamlit Web App
def main():
    create_user_table()  # Ensure the database table is created
    
    st.title("SMS Spam Detection with AI Suggestions")
    
    st.markdown(""" 
    This is a spam detection tool for SMS messages. 
    Enter a message, and the tool will predict if it's spam or not using Gemini AI.
    Additionally, Gemini AI will provide suggestions on improving or modifying the text.
    """)
    
    menu = ["Sign In", "Sign Up"]
    choice = st.sidebar.selectbox("Select an option", menu)

    # Sign In Page
    if choice == "Sign In":
        st.subheader("Sign In")
        
        # User input
        email = st.text_input("Email")
        password = st.text_input("Password", type='password')
        
        if st.button("Log In"):
            if email and password:
                user = check_user(email, password)
                if user:
                    st.success("Logged In Successfully!")
                    # Call spam detection and AI suggestions here
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
                else:
                    st.error("Invalid email or password.")
            else:
                st.warning("Please enter both email and password.")

    # Sign Up Page
    if choice == "Sign Up":
        st.subheader("Sign Up")

        # User input
        email = st.text_input("Email")
        password = st.text_input("Password", type='password')
        confirm_password = st.text_input("Confirm Password", type='password')

        if st.button("Sign Up"):
            if email and password and confirm_password:
                if password == confirm_password:
                    try:
                        register_user(email, password)
                        st.success("Account created successfully! You can now log in.")
                    except sqlite3.IntegrityError:
                        st.error("This email is already registered.")
                else:
                    st.error("Passwords do not match.")
            else:
                st.warning("Please fill out all fields.")

if __name__ == '__main__':
    main()
