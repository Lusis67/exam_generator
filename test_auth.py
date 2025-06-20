import streamlit as st
import streamlit_authenticator as stauth
import yaml
from ui.sidebar import course_sidebar

# Load credentials from YAML
with open("users.yaml") as file:
    config = yaml.safe_load(file)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

login_result = authenticator.login(location="main")
