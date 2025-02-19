import smtplib
import streamlit as st
from email.mime.text import MIMEText

# Streamlit UI
st.title("📩 Email-to-SMS Gateway")
st.write("Send SMS via Email-to-SMS Gateway.")

# User Inputs
email_address = st.text_input("📧 Your Email:")
email_password = st.text_input("🔑 Email Password (App Password for Gmail):", type="password")
phone_number = st.text_input("📱 Recipient's Phone Number:")
carrier_gateway = st.selectbox(
    "📡 Select Carrier Gateway:",
    ["@vtext.com (Verizon)", "@tmomail.net (T-Mobile)", "@txt.att.net (AT&T)", "@messaging.sprintpcs.com (Sprint)", "@vodafone.net (Vodafone UK)"]
)

message = st.text_area("💬 Enter your message:")

# Send Button
if st.button("📤 Send SMS"):
    if email_address and email_password and phone_number and carrier_gateway and message:
        st.info("Sending SMS... Please wait.")

        # Create recipient address
        sms_recipient = phone_number + carrier_gateway.split()[0]  # Extract domain from selectbox

        # Email Configuration
        SMTP_SERVER = "smtp.gmail.com"
        SMTP_PORT = 587

        # Create Email
        msg = MIMEText(message)
        msg["From"] = email_address
        msg["To"] = sms_recipient
        msg["Subject"] = "SMS Notification"

        try:
            # Connect to SMTP Server
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            server.starttls()
            server.login(email_address, email_password)
            server.sendmail(email_address, sms_recipient, msg.as_string())
            server.quit()
            
            st.success("✅ SMS Sent Successfully!")
        except Exception as e:
            st.error(f"❌ Failed to send SMS: {e}")

    else:
        st.warning("⚠️ Please fill all fields before sending.")

