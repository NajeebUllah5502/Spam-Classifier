pip install stripe 
import stripe
import streamlit as st

# Stripe secret key (replace with your actual secret key)
stripe.api_key = 'your_stripe_secret_key'

# Function to create a Stripe checkout session
def create_checkout_session():
    try:
        # Creating a checkout session
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',  # Change to your preferred currency
                        'product_data': {
                            'name': 'AI-Powered SMS Spam Detection Subscription',
                        },
                        'unit_amount': 1000,  # Amount in cents (1000 = $10)
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=f'{st.get_option("server.baseUrl")}/success',
            cancel_url=f'{st.get_option("server.baseUrl")}/cancel',
        )
        return checkout_session.url
    except Exception as e:
        st.error(f"Error creating checkout session: {e}")
        return None

# Pay Page
def pay_page():
    st.title("Subscribe to Access AI-Powered SMS Spam Detection Tool")
    st.markdown("""
    To access the full features of the SMS Spam Detection Tool, you need to subscribe to a plan. 
    Payment will give you access to all the functionalities.
    """)

    # Button to redirect to Stripe checkout page
    if st.button("Pay Now"):
        checkout_url = create_checkout_session()
        if checkout_url:
            st.markdown(f"### [Proceed to Payment](checkout_url)")
        else:
            st.error("Something went wrong while processing your payment. Please try again.")

# Main function to control the page flow
def main():
    if 'page' not in st.session_state:
        st.session_state.page = "pay"  # Start with the pay page

    if st.session_state.page == "pay":
        pay_page()

if __name__ == '__main__':
    main()
