# app.py

import streamlit as st
import tempfile
from helper import detect_violence
from email_alert import send_email_alert  # Make sure this function exists and works

st.set_page_config(page_title="Violence Detection", layout="centered")
st.title("🛡️ Violence Detection System")
st.write("Upload a video to detect violent scenes. You'll receive timestamps and an email alert.")

uploaded_file = st.file_uploader("📤 Upload a video file", type=["mp4", "avi"])
email = st.text_input("📧 Enter your email to receive alerts:")

if uploaded_file and email:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    st.video(tmp_path)

    with st.spinner("🔍 Detecting violence in the video..."):
        timestamps = detect_violence(tmp_path)

    if timestamps:
        st.success("⚠️ Violence detected at the following timestamps:")
        for t in timestamps:
            st.write(f"- {t:.2f} seconds")
        send_email_alert(email, timestamps)
        st.info(f"📨 Alert email sent to: **{email}**")
    else:
        st.success("✅ No violence detected in the video.")
