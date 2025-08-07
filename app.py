import streamlit as st
from google import genai
import gspread
from google.oauth2.service_account import Credentials
import datetime
import json

# Google Sheets credentials
GOOGLE_CREDENTIALS = {
    "type": "service_account",
    "project_id": "gen-lang-client-0819640616",
    "private_key_id": "96c9b8f981b9503b3653f4daf4a3d67ba3440c47",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDp8MUlZwnKApd7\nzKnrJUEDa+hONiB7hYGWhW2KuvkwbPKn8PoIn4XKtvs4pcd19hNCOVdjqh8PQiB1\nW2PgxqJJalW0WREKgIxcl39Ji6w51y9QPxgzqq2UNIE/uxUNWLuZx6lN+NOOW4tw\nCeYitAz6D9mWFT5smOG9eqX6nCgbz5QCHJTVuc5TRwCY6W6ftzaMFNrndLQfaj0S\nNP/YbtjQU1okh7hmucSiGS/kdncjw7NsXieITfAFKlXZiN9RKPRJOwC2fEEvcKd3\nNwtlTUk7/+SyJg+3sgUMqZpmVh4b6v/pxUopH2EdK3wtYT2qrTNOxXxFVL5/pty/\nHNRo9xmnAgMBAAECggEAZPg0PuZwBS6FLzuwgvs7SjzCsS8PagC/Y7YHB3+Xmd0M\nBowtfpdLaaj8WQDETBd/TG/vVebRLQa/d6eQPi29Ua6BeyuN/VhqPHRuzdFo7jYA\nB8STr4kVDghzWIxok7AemEriufKRbLn6Pssm9wd7Klq48NwOa1S46c0L4lSPwyBL\nScpH4eSwL9yPHp0Mttc95i+r+jyKZdmRFaOXlcxpdi3gU0ON8VzGWxEXJ+jQgovN\nYXXytFU2fQx8gXqWT/HJ8LYonpAvMb/Nt9UqP/14bhF9MKbi2kJSn3s9YAlJGSnu\nDNOlZqSnhFNKccPS1zDPDILjGUpTUi3xszbD2LnGoQKBgQD8bLliodvnGnkExYS/\nFmFfUM/SNqbRbNoFTT6c0pR547nSeTcPiPyFiDuy53EAcJpG2yXHbqmVdG3GtNZ+\nmJ0Elmt6OU9wR8fhWyKWyWVoEOlR5EhU5i64T4CsKhxHgU/14FCpGbyPQwtjO/CS\nhmo1Uz8q67MdUgGvn7pZZTkeDwKBgQDtQQX/duOWDYTPr3GLGbnb9gUQa6eGLj8i\nwvJ3SIASjS2btu/Ycef3jMY1Y/qnV7IMv4c4mgOJ4OoWNkfpH7ht3/QFzbwM0brq\nbFldVsgADXCT1aq54oj+WJMoF5DWtV4Qi9/yZxDgNxoeAHYchBvWfh9rCJljYKRT\nnNG39vdi6QKBgHpPCCi1esLo/diFCEQ6yOWRV5Fo772r+5v0CLGeC1lgMWq9VyOM\n4aamEx8lq4hmByrsBssyYLNNHd/ZQdFHi1VsuRkY6dfiwAP+z6y2Ww9omlUWwsF4\nYwzlYNiK8vbmvmLJ1OuKz+Wuu7bSlUe6H35FHudiG4DKeoypXXbxaBKbAoGBAOVH\nX2qAFHRgYCbs34eTtv+RA1fZEa4kZzNKvlL0J4DGGntPEP5VJd0fmDTkh8jMgO68\n8QqMHDtUtiP9FQV/eBYGxaYOKlshG8eMKdiAEwup8U+Mv06gU8+o/Z1TGM/Fuj+3\nTRbO74oe9ghkXcA1E0n33JjtWH6nWGbNOAbWjkBxAoGADj63326iUfFxSOl07sOw\nY4mYcs7K+lx2MTeerwkXOnOsK37+94dJwIZS17O7xMwVEzTHz6q1MNg3H8wqhrTu\nbGNsCU1qoHRB97lHTUB6rjaMBqxk2l2EZsv/+wMJYbwEWRY5brDLuShcRqcCtbxw\nZQ128zPNh746O9MXK3oy9z0=\n-----END PRIVATE KEY-----\n",
    "client_email": "gainzz@gen-lang-client-0819640616.iam.gserviceaccount.com",
    "client_id": "115231198127691029159",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/gainzz%40gen-lang-client-0819640616.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com"
}

GOOGLE_API_KEY = 'AIzaSyCIXuzDiGIAMC1SrHbFtRMSfJHtd8F2k9E'
SHEET_ID = '1wpPFWmDUNuFmXra91Fxr9oFad8xJflvy7XeXTlGszeA'

# === Helper Functions ===

def init_google_sheets():
    """Initialize Google Sheets connection"""
    try:
        scopes = ["https://www.googleapis.com/auth/spreadsheets"]
        creds = Credentials.from_service_account_info(GOOGLE_CREDENTIALS, scopes=scopes)
        gc = gspread.authorize(creds)
        sheet = gc.open_by_key(SHEET_ID)
        return sheet
    except Exception as e:
        st.error(f"Error connecting to Google Sheets: {str(e)}")
        return None


def get_or_create_worksheets(sheet):
    try:
        try:
            profiles_ws = sheet.worksheet("profiles")
        except:
            profiles_ws = sheet.add_worksheet(title="profiles", rows="1000", cols="10")
            profiles_ws.append_row([
                "email", "name", "age", "height", "weight", "fitness_goal",
                "medical_conditions", "injuries", "medications", "activity_level", "diet_preferences"
            ])
        try:
            messages_ws = sheet.worksheet("messages")
        except:
            messages_ws = sheet.add_worksheet(title="messages", rows="1000", cols="4")
            messages_ws.append_row(["email", "role", "content", "timestamp"])
        return profiles_ws, messages_ws
    except Exception as e:
        st.error(f"Error setting up worksheets: {str(e)}")
        return None, None

def get_user_profile(profiles_ws, email):
    try:
        records = profiles_ws.get_all_records()
        for record in records:
            if record['email'] == email:
                return record
        return None
    except Exception as e:
        st.error(f"Error getting user profile: {str(e)}")
        return None

def save_user_profile(profiles_ws, profile_data):
    try:
        profiles_ws.append_row([
            profile_data['email'], profile_data['name'], profile_data['age'],
            profile_data['height'], profile_data['weight'], profile_data['fitness_goal'],
            profile_data['medical_conditions'], profile_data['injuries'], profile_data['medications'],
            profile_data['activity_level'], profile_data['diet_preferences']
        ])
        return True
    except Exception as e:
        st.error(f"Error saving profile: {str(e)}")
        return False

def get_user_messages(messages_ws, email, limit=15):
    try:
        records = messages_ws.get_all_records()
        user_messages = [record for record in records if record['email'] == email]
        return user_messages[-limit:] if len(user_messages) > limit else user_messages
    except Exception as e:
        st.error(f"Error getting messages: {str(e)}")
        return []

def save_message(messages_ws, email, role, content):
    try:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        messages_ws.append_row([email, role, content, timestamp])
        return True
    except Exception as e:
        st.error(f"Error saving message: {str(e)}")
        return False

def collect_user_metadata():
    st.subheader("🏋️‍♂️ Welcome to GAINZ! Let's get you started with Coach Chad")
    st.write("Please fill out your profile so Coach Chad can create the perfect plan for you:")

    with st.form("user_profile"):
        col1, col2 = st.columns(2)
        with col1:
            age = st.number_input("Age", min_value=13, max_value=100, value=25)
            height = st.text_input("Height (e.g., 5'10\" or 178cm)")
            weight = st.text_input("Weight (e.g., 150lbs or 68kg)")
        with col2:
            fitness_goal = st.selectbox("Fitness Goal", [
                "Lose weight", "Gain muscle", "Get stronger", "Improve endurance", 
                "General fitness", "Athletic performance", "Other"
            ])
            activity_level = st.selectbox("Current Activity Level", [
                "Sedentary", "Lightly active", "Moderately active", "Very active", "Extremely active"
            ])
            diet_preferences = st.selectbox("Diet Preferences", [
                "No restrictions", "Vegetarian", "Vegan", "Keto", "Paleo", 
                "Mediterranean", "Low carb", "Other"
            ])

        medical_conditions = st.text_area("Medical Conditions (if any)", placeholder="e.g., diabetes, high blood pressure, etc.")
        injuries = st.text_area("Current/Past Injuries", placeholder="e.g., knee injury, back problems, etc.")
        medications = st.text_area("Current Medications", placeholder="List any medications you're taking")

        submitted = st.form_submit_button("Start Training with Coach Chad! 💪")
        if submitted:
            return {
                'email': st.session_state.user_email,
                'name': st.session_state.user_name,
                'age': age,
                'height': height,
                'weight': weight,
                'fitness_goal': fitness_goal,
                'medical_conditions': medical_conditions,
                'injuries': injuries,
                'medications': medications,
                'activity_level': activity_level,
                'diet_preferences': diet_preferences
            }
    return None

def create_coach_context(profile, recent_messages):
    context = f"""You are Coach Chad, a motivational and knowledgeable fitness coach for the GAINZ app.

User Profile:
- Name: {profile['name']}
- Age: {profile['age']}
- Height: {profile['height']}
- Weight: {profile['weight']}
- Fitness Goal: {profile['fitness_goal']}
- Activity Level: {profile['activity_level']}
- Diet Preferences: {profile['diet_preferences']}
- Medical Conditions: {profile['medical_conditions']}
- Injuries: {profile['injuries']}
- Medications: {profile['medications']}

Recent conversation context:
"""
    for msg in recent_messages[-5:]:
        context += f"{msg['role']}: {msg['content']}\n"

    context += "\nAs Coach Chad, be motivational, personalized, and always consider their health conditions and goals. Keep responses conversational and encouraging!"
    return context

# === Main App ===

def main():
    st.title("💪 GAINZ - Your Personal Fitness Coach")

    sheet = init_google_sheets()
    if not sheet:
        st.error("Unable to connect to database. Please try again later.")
        return

    profiles_ws, messages_ws = get_or_create_worksheets(sheet)
    if not profiles_ws or not messages_ws:
        st.error("Unable to set up database. Please try again later.")
        return

    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        st.subheader("🔐 Login to GAINZ")
        with st.form("login_form"):
            email = st.text_input("Email Address")
            name = st.text_input("Full Name")
            login_submitted = st.form_submit_button("Enter GAINZ")
            if login_submitted and email and name:
                st.session_state.user_email = email
                st.session_state.user_name = name
                st.session_state.authenticated = True
                st.rerun()
        return

    user_profile = get_user_profile(profiles_ws, st.session_state.user_email)
    if not user_profile:
        profile_data = collect_user_metadata()
        if profile_data:
            if save_user_profile(profiles_ws, profile_data):
                st.success("Profile saved! Welcome to GAINZ! 🎉")
                st.rerun()
        return

    st.subheader("💬 Chat with Coach Chad")
    st.write(f"Welcome back, {user_profile['name']}! Ready to crush your {user_profile['fitness_goal'].lower()} goals? 💪")

    try:
        client = genai.Client(api_key=GOOGLE_API_KEY)
    except Exception as e:
        st.error(f"Error initializing AI: {str(e)}")
        return

    if "messages" not in st.session_state:
        user_messages = get_user_messages(messages_ws, st.session_state.user_email)
        st.session_state.messages = [{"role": msg["role"], "content": msg["content"]} for msg in user_messages]

    if "chat" not in st.session_state:
        context = create_coach_context(user_profile, st.session_state.messages)
        st.session_state.chat = client.chats.create(model="gemini-2.0-flash-exp")
        if context:
            st.session_state.chat.send_message(context)

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            if message["role"] == "assistant":
                st.write(f"**Coach Chad:** {message['content']}")
            else:
                st.write(message["content"])

    if prompt := st.chat_input("Ask Coach Chad anything about fitness, nutrition, or your goals..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        save_message(messages_ws, st.session_state.user_email, "user", prompt)

        with st.chat_message("user"):
            st.write(prompt)

        try:
            context_prompt = f"""
            Remember you're Coach Chad talking to {user_profile['name']}.
            Their goal: {user_profile['fitness_goal']}
            Their question: {prompt}

            Respond as Coach Chad - motivational, knowledgeable, and personalized.
            """
            response = st.session_state.chat.send_message(context_prompt)
            ai_response = response.text

            st.session_state.messages.append({"role": "assistant", "content": ai_response})
            save_message(messages_ws, st.session_state.user_email, "assistant", ai_response)

            with st.chat_message("assistant"):
                st.write(f"**Coach Chad:** {ai_response}")
        except Exception as e:
            st.error(f"Coach Chad is taking a quick break: {str(e)}")

    with st.sidebar:
        st.header("🏋️‍♂️ Your GAINZ Profile")
        st.write(f"**Name:** {user_profile['name']}")
        st.write(f"**Goal:** {user_profile['fitness_goal']}")
        st.write(f"**Activity Level:** {user_profile['activity_level']}")
        st.divider()

        st.header("💬 Chat Stats")
        st.write(f"Messages: {len(st.session_state.messages)}")

        if st.button("🔄 New Chat Session"):
            st.session_state.messages = []
            context = create_coach_context(user_profile, [])
            st.session_state.chat = client.chats.create(model="gemini-2.0-flash-exp")
            st.session_state.chat.send_message(context)
            st.rerun()

        if st.button("🚪 Logout"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

if __name__ == "__main__":
    main()
