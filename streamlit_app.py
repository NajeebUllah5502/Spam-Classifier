import streamlit as st
import random
import time
from faker import Faker

fake = Faker()

# Realistic domains
real_domains = ['gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com', 'live.com', 'icloud.com', 'aol.com']

def generate_realistic_emails(target):
    # Extended name lists
    english_names = [
        'James', 'John', 'Robert', 'Michael', 'David', 'William', 'Richard', 'Joseph', 'Charles', 'Thomas',
        'Christopher', 'Daniel', 'Matthew', 'Andrew', 'Joshua', 'Ethan', 'Samuel', 'Benjamin', 'Alexander', 'Jack',
        'Ryan', 'Lucas', 'Henry', 'Max', 'Leo', 'Isaac', 'Nathan', 'Aaron', 'Owen', 'Adam', 'Mason', 'Elijah',
        'Logan', 'Aiden', 'Luke', 'Dylan', 'Caleb', 'Tyler', 'Carter', 'Isaiah', 'Gavin', 'Julian', 'Zachary',
        'Hunter', 'Christian', 'Jaxon', 'Austin', 'Cole', 'Miles', 'Jacob', 'Seth', 'Grayson', 'Sebastian',
        'Maverick', 'Lincoln', 'Brayden', 'Cooper', 'Kai', 'Hudson', 'Asher', 'Wyatt', 'Connor', 'Oliver', 'Evan',
        'Landon', 'Bentley', 'Levi', 'Jameson', 'Sawyer', 'Jordan', 'Caden', 'Carson', 'Chase', 'Blake', 'Eli',
        'Tristan', 'Brody', 'Jude', 'Paxton', 'Ryder', 'Nathaniel', 'Brooks', 'Maxwell', 'Nolan', 'Brandon',
        'Gage', 'Weston', 'Graham', 'Ezra', 'Damian', 'Brady', 'Riley', 'Finn', 'Emmett', 'Bennett', 'Bryce',
        'Dominic', 'Parker', 'Declan', 'Kaden', 'Jonah', 'Dawson', 'Charlie', 'Jasper', 'Theo', 'Jace', 'Milo'
    ]
    spanish_names = [
        'Juan', 'Pedro', 'Luis', 'Javier', 'Carlos', 'Andrés', 'Antonio', 'Francisco', 'José', 'Manuel',
        'Fernando', 'Miguel', 'Santiago', 'Pablo', 'Alberto', 'Rafael', 'Ricardo', 'Enrique', 'Jorge', 'Raúl',
        'Víctor', 'Álvaro', 'Emilio', 'Marco', 'Ángel', 'Gabriel', 'Joaquín', 'Esteban', 'Domingo', 'Felipe'
    ]
    
    emails = set()
    while len(emails) < target:
        if random.random() < 0.7:
            name = random.choice(english_names)
        else:
            name = random.choice(spanish_names)
        
        last_name = fake.last_name().lower().replace(" ", "")
        number = random.randint(1000, 9999)
        domain = random.choice(real_domains)
        
        # Create realistic email
        email = f"{name.lower()}{last_name}{number}@{domain}"
        emails.add(email)
    
    # If target is 1000, show only 15–30%
    if target == 1000:
        limit_percent = random.randint(15, 30)
        limited_count = (target * limit_percent) // 100
        emails = list(emails)[:limited_count]
    
    return list(emails)

# Store previous generation
def load_previous_data():
    if 'generated_data' not in st.session_state:
        st.session_state.generated_data = {}

# UI
st.title("Email Generator")

load_previous_data()

instagram_account = st.text_input("Enter your Instagram account:")
target_users = st.number_input("How many target users?", min_value=1, max_value=5000, step=1)

if instagram_account in st.session_state.generated_data:
    st.subheader(f"Previously generated emails for **{instagram_account}**:")
    st.write(st.session_state.generated_data[instagram_account])
else:
    if st.button("Generate Emails"):
        if instagram_account and target_users > 0:
            st.info("emails... Please wait 10 seconds.")
            time.sleep(10)
            emails = generate_realistic_emails(target_users)
            st.session_state.generated_data[instagram_account] = emails
            st.success(f"Generated {len(emails)} emails:")
            st.write(emails)
        else:
            st.error("Please enter a valid Instagram and number.")
