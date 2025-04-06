import streamlit as st
import random
import time
from faker import Faker
import json

# Initialize the Faker instance
fake = Faker()

# Function to generate emails without the word "fake" and with unique names, adding random numbers
def generate_fake_emails(target):
    # Expanded list of English and Spanish names
    english_names = [
        'James', 'John', 'Robert', 'Michael', 'David', 'William', 'Richard', 'Joseph', 'Charles', 'Thomas',
        'Christopher', 'Daniel', 'Matthew', 'Andrew', 'Joshua', 'Ethan', 'Samuel', 'Benjamin', 'Alexander', 'Jack',
        'Ryan', 'Lucas', 'Henry', 'Max', 'Leo', 'Isaac', 'Nathan', 'Aaron', 'Owen', 'Adam', 'Mason', 'Elijah',
        'Logan', 'Jack', 'Aiden', 'Luke', 'Dylan', 'Caleb', 'Jack', 'Tyler', 'Carter', 'Isaiah', 'Gavin', 'Julian',
        'Zachary', 'Hunter', 'Christian', 'Jaxon', 'Austin', 'Leo', 'Cole', 'Miles', 'Thomas', 'Jacob', 'Seth',
        'Grayson', 'Joshua', 'Sebastian', 'Caleb', 'Maverick', 'Lincoln', 'Brayden', 'Cooper', 'Kai', 'Hudson',
        'Asher', 'Ryan', 'Wyatt', 'Connor', 'Oliver', 'Evan', 'Isaiah', 'Landon', 'Bentley', 'Levi', 'Adam',
        'Jameson', 'Sawyer', 'Jordan', 'Caden', 'Carson', 'Chase', 'Hudson', 'Wyatt', 'Blake', 'Eli', 'Tristan',
        'Brody', 'Jude', 'Paxton', 'Ryder', 'Nathaniel', 'Austin', 'Brooks', 'Maxwell', 'Nolan', 'Brandon', 'Gage',
        'Weston', 'Graham', 'Ezra', 'Damian', 'Brady', 'Riley', 'Finn', 'Emmett', 'Bennett', 'Bryce', 'Levi',
        'Dominic', 'Parker', 'Declan', 'Kaden', 'Jonah', 'Eli', 'Dawson', 'Graham', 'Riley', 'Charlie', 'Finn',
        'Jasper', 'Theo', 'Avery', 'Jace', 'Gage', 'Austin', 'Milo', 'Griffin', 'Maddox', 'Simon', 'Kai',
        'Paxton', 'Xander', 'Elian', 'Luka', 'Wesley', 'Silas', 'Kendall', 'Brock', 'Reed', 'Owen'
    ]
    
    spanish_names = [
        'Juan', 'Pedro', 'Luis', 'Javier', 'Carlos', 'Andrés', 'Antonio', 'Francisco', 'José', 'Manuel',
        'Fernando', 'Miguel', 'Santiago', 'Pablo', 'Alberto', 'Rafael', 'Ricardo', 'Enrique', 'Jorge', 'David',
        'Raúl', 'Víctor', 'Álvaro', 'Juan Carlos', 'Emilio', 'Marco', 'Ángel', 'Gabriel', 'Antonio Javier', 'Joaquín'
    ]
    
    emails = set()  # Using a set to ensure unique emails
    
    # Generate emails
    while len(emails) < target:
        if random.random() < 0.7:  # 70% English names
            name = random.choice(english_names)
        else:  # 30% Spanish names
            name = random.choice(spanish_names)
        
        email = fake.email()
        email = email.replace(fake.first_name(), name)  # Replace the name part with the generated one
        
        # Ensure no "fake" word in the email
        email = email.replace("fake", "")  # Remove the word "fake"
        
        # Add random numbers at the end of the email to make it look more realistic
        random_number = random.randint(1000, 9999)
        email = email.split('@')[0] + str(random_number) + "@" + email.split('@')[1]  # Adding number before the '@' part
        
        emails.add(email)
    
    # If target is 1000, filter to show only 15-30% emails
    if target == 1000:
        limit = random.randint(15, 30)
        emails = list(emails)[:(len(emails) * limit) // 100]
    
    return list(emails)

# Function to load and store data in session state
def load_previous_data():
    if 'generated_data' not in st.session_state:
        st.session_state.generated_data = {}

# Streamlit UI
st.title(" Email Instagram Scraper")

# Load previous data from session state
load_previous_data()

# Ask user for Instagram account and target number of users
instagram_account = st.text_input("Enter your Instagram account:")
target_users = st.number_input("How many target users?", min_value=1, max_value=5000, step=1)

# Check if the Instagram account has already been used and fetch previous data
if instagram_account in st.session_state.generated_data:
    st.write(f"Previously generated emails for {instagram_account}:")
    st.write(st.session_state.generated_data[instagram_account])
else:
    # Generate emails when button is clicked
    if st.button("Get Emails"):
        if instagram_account and target_users > 0:
            st.write("Scraping emails... Please wait.")
            time.sleep(10)  # Simulate a delay of 10 seconds
            fake_emails = generate_fake_emails(target_users)
            st.write(f"Generated {len(fake_emails)} fake emails:")

            # Store the generated emails for this Instagram account
            st.session_state.generated_data[instagram_account] = fake_emails
            st.write(fake_emails)
        else:
            st.error("Please provide a valid Instagram account and target number of users.")
