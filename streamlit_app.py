import requests
import json
import streamlit as st

# Your API details
GEMINI_API_KEY = "AIzaSyBEXfh1wUUdCFEsT_yZ_DUyov-49mk-MDw"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
GEMINI_HEADERS = {"Content-Type": "application/json"}

# Facebook API details
USER_ACCESS_TOKEN = 'EAAQ1ZAgHKnkEBOZC05Mh4dHZACqd0VEeXVfle4Q2GvqZAqrO9GxJFO6JBoMr90djbUWrOBVqCR45Hp6hywqGJ16mKpDRfRbWW1rW3qz3k5n3ZCdEN2aryd94qQkXxdnktFFfQPHcTPNg0jiejYWMOyZCWwulUE6KtVk36ZBqZBCJ0eTlwi0IfmLy5Vy3CQyrkvCIi1S7IfkQLbE0124xD20gaXjIrtjnUaiUKQZDZD'
PAGE_ID = '599271760084973'

# Define your topic
topic = "Waarom het gebruik van originele telefoononderdelen belangrijk is voor de kwaliteit van uw reparatie"

# Craft the prompt
prompt = f"""
Je bent een AI-inhoudsassistente voor de officiële beheerder van Fixst — een top-rated telefoon-, tablet- en laptopreparatieservice
in Hoogvliet, Spijkenisse, Rhoon, Poortugaal, Pernis en de omliggende gebieden.

De beheerder maakt een informatieve post over het onderwerp: {topic}.

Op basis van de autoritaire rol van de beheerder, genereer een behulpzame, professionele en duidelijke uitleg of aankondiging
voor de klanten en websitebezoekers.

Voeg een oproep tot actie toe die mensen aanmoedigt om contact met ons op te nemen voor snelle, hoogwaardige reparaties.

Voeg aan het einde altijd het volgende toe:

"Ik heb deze promo om te verzenden met het onderwerp en Gemini gaf mij een reactie overeenkomstig."

📞 Telefoon: 06 1755 71365
📧 E-mail: info@fixstspijkenisse.nl
🛠️ Van de beheerder van Fixst

En vergeet niet onze prijzen:

Fixst Paramaribo – iPhone Scherm Reparatie met Europese Kwaliteit! 🔧💥
Is je iPhone scherm gebroken? Kom naar Fixst Paramaribo voor snel en vakkundig repareren! We gebruiken Europese kwaliteit onderdelen en je krijgt 3 maanden garantie! 🔒
Onze scherpe prijzen (met koers 36):
iPhone X, XR, XS, XS Max, 11: 1100 SRD
iPhone 11 Pro: 1300 SRD
iPhone 11 Pro Max: 1400 SRD
iPhone 12, 12 Pro: 1400 SRD
iPhone 12 Pro Max: 1600 SRD
iPhone 13: 1440 SRD
iPhone 13 Pro: 1620 SRD
iPhone 13 Pro Max: 1980 SRD
Waarom Fixst?
✅ Europese kwaliteit voor een Surinaamse prijs
✅ Snel geholpen – geen gedoe!
✅ 3 maanden garantie op elke reparatie
📍 Locatie: Langatabiki Straat, Paramaribo
⏰ Open van 10:00 tot 22:00
📲 Kom langs of stuur een DM voor meer info!
#FixstParamaribo #iPhoneReparatie #TelefoonFix #Suriname #iPhoneScherm #TelefoonReparatie #TechFix
"""

# Prepare the request payload for Gemini
data = {
    "contents": [
        {
            "parts": [{"text": prompt}]
        }
    ]
}

# Streamlit UI setup
st.title("AI Content Generation and Facebook Post Automation")
st.subheader("Generated Content:")

# Function to post content on Facebook
def post_to_facebook(content):
    # Facebook API request to post the generated content
    url = f'https://graph.facebook.com/{PAGE_ID}/feed'
    payload = {
        'message': content,
        'access_token': USER_ACCESS_TOKEN
    }
    
    # Send the POST request to Facebook
    fb_response = requests.post(url, data=payload)

    # Check if the post was successful
    if fb_response.status_code == 200:
        st.success("Post successfully created on Facebook!")
    else:
        fb_error_message = fb_response.json().get('error', {}).get('message', 'Unknown error')
        st.error(f"Error posting to Facebook: {fb_response.status_code}, {fb_error_message}")
        print(f"Error posting to Facebook: {fb_response.status_code}, {fb_error_message}")

# Send the API request to Gemini
response = requests.post(GEMINI_URL, headers=GEMINI_HEADERS, data=json.dumps(data))

# Check if the request was successful
if response.status_code == 200:
    gemini_response = response.json()
    generated_content = gemini_response.get("predictions", [{}])[0].get("content", "")
    
    if generated_content:
        st.write(generated_content)  # Display the content in the Streamlit app
        post_to_facebook(generated_content)  # Post to Facebook
    else:
        st.error("No content generated. Please try again.")
else:
    error_message = response.json().get('error', {}).get('message', 'Unknown error')
    st.error(f"Error with Gemini API: {response.status_code}, {error_message}")
    print(f"Error with Gemini API: {response.status_code}, {error_message}")
