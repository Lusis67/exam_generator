from dotenv import load_dotenv
import os

load_dotenv()  # Loads variables from .env

openai_api_key = os.getenv("OPENAI_API_KEY")

import streamlit as st
import streamlit_authenticator as stauth
import yaml
from ui.sidebar import course_sidebar

# Load credentials from YAML
with open("users.yaml") as file:
    config = yaml.safe_load(file)
st.write("DEBUG: Loaded YAML config")

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)
st.write("DEBUG: Authenticator initialized")

login_result = authenticator.login('main')
st.write("DEBUG: login_result =", login_result)
# Defensive unpacking
if isinstance(login_result, tuple) and len(login_result) == 3:
    name, authentication_status, username = login_result
else:
    name = username = None
    authentication_status = login_result
st.write("DEBUG: authentication_status =", authentication_status)
st.write("DEBUG: authentication_status type =", type(authentication_status)) 
st.write("DEBUG: name =", name)
st.write("DEBUG: username =", username)



if authentication_status is True:
    st.success(f"Welcome, {name}!")
elif authentication_status is False:
    st.error("Username/password is incorrect")
elif authentication_status is None:
    st.warning("Please enter your username and password")