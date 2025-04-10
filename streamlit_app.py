import streamlit as st
import requests
import time

# ===== API Config =====
GEMINI_API_KEY = "AIzaSyBEXfh1wUUdCFEsT_yZ_DUyov-49mk-MDw"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
GEMINI_HEADERS = {"Content-Type": "application/json"}

USER_ACCESS_TOKEN = 'EAAQ1ZAgHKnkEBO0GPD9tThWGYI46ucucdwP1lHUwTWc8SN0g3beibIydhoQlWtTyw0mJajBs3mVrlxBrZCXUC6vVQbldULsiyypyx9zKa2R9ZBYHaENDdgGeAE6jZAZCOXOsMFjBZATxAvAILVIvbcwYMv784WtHkZCeOo7WvMlCf7tb8mprqtXjYzmtrMcWA6dunfmkxqRFZAV3NI5GN7YCPC1PZA33DD9vjOgMIcVv3O1gZD'

PAGE_ID = '599271760084973'

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

# ===== Functions =====
def get_page_access_token(user_token, page_id):
    url = f'https://graph.facebook.com/v22.0/{page_id}?fields=access_token&access_token={user_token}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('access_token')
    return None

def post_to_facebook(page_access_token, page_id, message):
    url = f'https://graph.facebook.com/{page_id}/feed'
    params = {'message': message, 'access_token': page_access_token}
    response = requests.post(url, params=params)
    return response.status_code == 200

def generate_gemini_response(question):
    body = {
        "contents": [ {
            "parts": [{"text": prompt}]
        }]
    }
    try:
        r = requests.post(GEMINI_URL, headers=GEMINI_HEADERS, json=body)
        if r.status_code == 200:
            return r.json().get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "Geen inhoud beschikbaar.")
    except Exception:
        pass
    return None

# ===== Streamlit UI =====
st.title("AutoPoster to Facebook 🌍")
gemini_question = st.text_input("Gemini Topic (Dutch) ✍️")

if st.button("Generate & Post"):
    if not gemini_question:
        st.warning("Please fill the Gemini question.")
    else:
        with st.spinner("Generating Dutch response..."):
            response_text = generate_gemini_response(gemini_question)
        if response_text:
            st.success("Response generated:")
            st.markdown(f"**{response_text}**")
            with st.spinner("Posting to Facebook..."):
                token = get_page_access_token(USER_ACCESS_TOKEN, PAGE_ID)
                if token and post_to_facebook(token, PAGE_ID, response_text):
                    st.success("✅ Successfully posted to Facebook!")
                else:
                    st.error("❌ Failed to post to Facebook.")
        else:
            st.error("❌ Failed to get Gemini response.")
