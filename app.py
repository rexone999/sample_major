# app.py
import streamlit as st
import tempfile
import os
import cv2
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.inception_v3 import InceptionV3, preprocess_input
from tensorflow.keras.preprocessing import image
from tensorflow.keras.utils import pad_sequences
from send_email import send_email_alert

# Load LSTM model and Inception feature extractor
model = load_model("vlstm_92.h5")
cnn_model = InceptionV3(weights="imagenet", include_top=False, pooling="avg")

def extract_features(video_path, max_frames=300, sequence_len=30):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frames = []
    timestamps = []

    count = 0
    while count < max_frames:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.resize(frame, (299, 299))
        img = image.img_to_array(frame)
        img = preprocess_input(img)
        frames.append(img)
        timestamps.append(cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0)
        count += 1
    cap.release()

    # Extract features using CNN
    frames_np = np.array(frames)
    features = cnn_model.predict(frames_np, verbose=0)

    # Chunk into sequences of 30 frames
    feature_sequences = []
    time_sequences = []
    for i in range(0, len(features) - sequence_len + 1, sequence_len):
        feature_sequences.append(features[i:i+sequence_len])
        time_sequences.append(timestamps[i + sequence_len // 2])  # middle timestamp

    feature_sequences = np.array(feature_sequences)
    return feature_sequences, time_sequences

def detect_violence(video_path):
    sequences, times = extract_features(video_path)
    if len(sequences) == 0:
        return []
    preds = model.predict(sequences, verbose=0)
    return [times[i] for i, p in enumerate(preds) if p > 0.5]

# Streamlit interface
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
