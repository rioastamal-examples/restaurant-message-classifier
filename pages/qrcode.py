import streamlit as st
import os

QRCODE_URL = os.getenv("QRCODE_URL")

st.title("bit.ly/restodinamika")
st.image(QRCODE_URL)
