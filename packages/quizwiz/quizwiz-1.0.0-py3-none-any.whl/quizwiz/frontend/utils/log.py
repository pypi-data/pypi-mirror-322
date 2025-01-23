import streamlit as st

from config import Config


class Log:
    @staticmethod
    def ui_debug(message, force=False):
        if Config.DEBUG_PRINT or force:
            st.write(message)
