# app.py
import streamlit as st
import tempfile
from helper import detect_violence
from send_email import send_email_alert

st.title("Violence Detection in Videos")

uploaded_file = st.file_uploader("Upload a video", type=["mp4", "avi", "mov"])
email = st.text_input("Enter your email (for alerts)")

if uploaded_file and email:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    st.video(tmp_path)
    st.info("Processing video for violence detection...")

    timestamps = detect_violence(tmp_path)

    if timestamps:
        st.success("Violence detected at timestamps:")
        for t in timestamps:
            st.write(f"- {t:.2f} seconds")
        send_email_alert(email, timestamps)
    else:
        st.success("No violence detected.")
