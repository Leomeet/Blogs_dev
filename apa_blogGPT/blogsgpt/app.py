"""main streamlit application file"""

import streamlit as st
from PIL import Image
from backend.utils import General
from frontend.streamlit_ui import UiWrappers
from configparser import ConfigParser

APP_CONFIG = ConfigParser()
APP_CONFIG.read("config.ini")

simform_img = Image.open("images/simform-logo.png")

# Setting page title and header
st.set_page_config(page_title="BlogsGpt", page_icon=simform_img)

manager = General()
ui = UiWrappers()
manager.initialize_session()
ui.sidebar()
manager()
ui.chat()

if APP_CONFIG.get("DEV", "DEV_MODE") == "Enable":
    ui.dev_stats()