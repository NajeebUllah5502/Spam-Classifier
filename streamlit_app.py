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

# Welcome Page
def welcome_page():
    st.title("SMS Spam Detection with AI Suggestions")
    st.markdown("""
    ### Welcome to the SMS Spam Detection Tool
    This tool helps you detect whether an SMS message is spam or not using the power of AI. 
    It also provides suggestions on how to improve or modify the text.
    """)
    
    # Navigation buttons to Sign In or Sign Up
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Sign In"):
            st.session_state.page = "sign_in"
    with col2:
        if st.button("Sign Up"):
            st.session_state.page = "sign_up"

# Sign In Page
def sign_in_page():
    st.subheader("Sign In")
    
    email = st.text_input("Email Address", placeholder="Enter your email address")
    password = st.text_input("Password", type='password', placeholder="Enter your password")
    
    if st.button("Log In"):
        if email and password:
            user = check_user(email, password)
            if user:
                st.success("Logged in successfully!")
                st.session_state.page = "program"
            else:
                st.error("Invalid email or password. Please try again.")
        else:
            st.warning("Please enter both email and password to log in.")
    
    if st.button("Back to Welcome Page"):
        st.session_state.page = "welcome"

# Sign Up Page
def sign_up_page():
    st.subheader("Create a New Account")
    
    email = st.text_input("Email Address", placeholder="Enter your email address")
    password = st.text_input("Password", type='password', placeholder="Enter your password")
    confirm_password = st.text_input("Confirm Password", type='password', placeholder="Re-enter your password")
    
    if st.button("Sign Up"):
        if email and password and confirm_password:
            if password == confirm_password:
                try:
                    register_user(email, password)
                    st.success("Account created successfully! You can now log in.")
                    st.session_state.page = "sign_in"
                except sqlite3.IntegrityError:
                    st.error("This email is already registered. Please use a different email.")
            else:
                st.error("Passwords do not match. Please check and try again.")
        else:
            st.warning("Please fill out all fields to create an account.")
    
    if st.button("Back to Welcome Page"):
        st.session_state.page = "welcome"

# Program Page (after successful sign-in)
def program_page():
    st.title("SMS Spam Detection")
    st.markdown("""
    ### Message Spam Detection
    Enter the SMS message you want to check for spam detection. The AI will tell you whether it's spam or not.
    """)
    
    # Message input
    message = st.text_area("Enter SMS Message:", placeholder="Type your SMS here...")
    
    if st.button("Check if Spam"):
        if message:
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
            st.success(f"The message is classified as: {result.capitalize()}")
            st.markdown(f"**Spam Detection Score**: {score}")
            st.write(f"**Word Count**: {words}")
            st.write(f"**Estimated Read Time**: {read_time} seconds")

            # Display AI suggestion
            st.markdown("### AI Suggestion for Improving the Message:")
            st.write(ai_suggestion)

        else:
            st.warning("Please enter a message to check for spam.")
    
    if st.button("Log Out"):
        st.session_state.page = "welcome"

# Main function to control the page flow
def main():
    create_user_table()  # Ensure the database table is created
    
    # Initialize session state for page navigation
    if 'page' not in st.session_state:
        st.session_state.page = "welcome"  # Start with the welcome page
    
    if st.session_state.page == "welcome":
        welcome_page()
    elif st.session_state.page == "sign_in":
        sign_in_page()
    elif st.session_state.page == "sign_up":
        sign_up_page()
    elif st.session_state.page == "program":
        program_page()

if __name__ == '__main__':
    main()
