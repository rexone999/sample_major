import cv2
import numpy as np
import tensorflow as tf
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

def detect_violence(video_path):
    frames, timestamps = extract_frames(video_path)
    preds = model.predict(frames, verbose=0)
    violence_times = [timestamps[i] for i, pred in enumerate(preds) if pred[0] > 0.5]
    return violence_times
