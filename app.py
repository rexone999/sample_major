import streamlit as st
import tempfile, os
from helper import extract_frames, detect_violence
from email_alert import send_email_alert

st.title("Violence Detection System")
st.write("Upload a video to detect violence. Timestamps with violence will be shown and alerts will be sent.")

uploaded_file = st.file_uploader("Upload Video", type=["mp4", "avi"])
email = st.text_input("Enter your email to receive alerts:")

if uploaded_file and email:
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
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
        st.info(f"Alert email sent to: {email}")
    else:
        st.success("No violence detected in the video.")
