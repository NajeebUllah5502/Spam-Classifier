import sqlite3
import hashlib
import streamlit as st
import google.generativeai as genai
import stripe
from datetime import datetime

# Configure the Gemini API
def genAI(user_prompt):
    genai.configure(api_key="AIzaSyBEXfh1wUUdCFEsT_yZ_DUyov-49mk-MDw")
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(user_prompt)
    return response.text

# Configure Stripe
stripe.api_key = "sk_test_XXXXXXXXXXXXXXXXXXXX"  # Replace with your Stripe secret key

# Database setup function to create the user table
def create_user_table():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        email TEXT PRIMARY KEY,
                        password TEXT,
                        stripe_customer_id TEXT,
                        subscription_status TEXT)''')
    conn.commit()
    conn.close()

# Function to register a new user
def register_user(email, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    cursor.execute('''INSERT INTO users (email, password, stripe_customer_id, subscription_status) 
                      VALUES (?, ?, ?, ?)''', (email, hashed_password, "", "inactive"))
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

# Function to create a Stripe customer and subscription
def create_stripe_subscription(email):
    try:
        # Create Stripe customer
        customer = stripe.Customer.create(
            email=email,
            description="Customer for SMS Spam Detection Tool"
        )

        # Create a checkout session
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': 'SMS Spam Detection Tool Subscription',
                        },
                        'unit_amount': 500,  # Amount in cents (e.g., $5.00)
                    },
                    'quantity': 1,
                },
            ],
            mode='subscription',
            success_url="http://localhost:8501/success",  # Redirect URL after success
            cancel_url="http://localhost:8501/cancel",  # Redirect URL if canceled
        )

        # Update the user with Stripe customer ID
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('''UPDATE users SET stripe_customer_id = ?, subscription_status = ? WHERE email = ?''',
                       (customer.id, "inactive", email))
        conn.commit()
        conn.close()

        return session.url

    except Exception as e:
        st.error(f"Error creating Stripe subscription: {e}")

# Page to handle Stripe subscription
def subscribe_page():
    st.title("Subscribe to SMS Spam Detection Tool")
    st.markdown("""
    Subscribe to gain full access to the SMS Spam Detection Tool for an enhanced experience.
    """)

    # Check if user is logged in
    if 'email' in st.session_state:
        email = st.session_state.email
        session_url = create_stripe_subscription(email)

        st.markdown(f"To complete your subscription, click the button below:")
        if st.button("Subscribe Now", use_container_width=True):
            st.write(f"Redirecting to Stripe Checkout...")
            st.markdown(f'<a href="{session_url}" target="_blank">Proceed with Subscription</a>', unsafe_allow_html=True)
    else:
        st.warning("You must log in to subscribe. Please log in to proceed.")

# Program Page (after successful sign-in)
def program_page():
    # Check subscription status before showing content
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT subscription_status FROM users WHERE email = ?''', (st.session_state.email,))
    user = cursor.fetchone()
    conn.close()

    if user and user[0] == 'inactive':
        st.warning("Please subscribe to gain full access.")
        subscribe_page()
        return
    
    st.title("SMS Spam Detection")
    st.markdown("""Enter the SMS message you want to check for spam detection. The AI will tell you whether it's spam or not and provide suggestions for improvement.""")

    message = st.text_area("Enter SMS Message:", placeholder="Type your SMS here...", height=150)
    
    if st.button("Check if Spam", use_container_width=True):
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
    
    if st.button("Log Out", use_container_width=True):
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
