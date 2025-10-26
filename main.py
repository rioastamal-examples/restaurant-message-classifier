import streamlit as st

st.set_page_config(
    page_title="Restaurant Message Classifier",
    page_icon="🍽️",
    layout="wide"
)

# Define pages with custom titles
input_page = st.Page("pages/send_message.py", title="Kirim Pesan", icon="📝")
dashboard_page = st.Page("pages/dashboard.py", title="Dashboard", icon="📊")
prompt_page = st.Page("pages/prompt.py", title="System Prompt", icon="🤖")
qrcode_page = st.Page("pages/qrcode.py", title="QR Code", icon="🧑‍💻")

# Navigation
pg = st.navigation([input_page, dashboard_page, prompt_page, qrcode_page])
pg.run()
