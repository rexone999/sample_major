# helper.py

import cv2
import numpy as np
from tensorflow.keras.models import load_model

MODEL_PATH = "best_violence_model.h5"
model = load_model(MODEL_PATH)

def extract_frames(video_path, step=30):
    cap = cv2.VideoCapture(video_path)
    frames = []
    timestamps = []
    frame_rate = cap.get(cv2.CAP_PROP_FPS)

    i = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if i % step == 0:
            resized = cv2.resize(frame, (299, 299))
            rgb = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
            frames.append(rgb / 255.0)
            timestamps.append(cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0)
        i += 1
    cap.release()
    return np.array(frames), timestamps

def detect_violence(video_path, threshold=0.5):
    frames, timestamps = extract_frames(video_path)
    if frames.size == 0:
        return []

    preds = model.predict(frames, verbose=0)  # shape: (N, 1)

    if preds.ndim == 1:
        preds = np.expand_dims(preds, axis=-1)

    violence_times = [timestamps[i] for i, pred in enumerate(preds) if pred[0] > threshold]
    return violence_times
