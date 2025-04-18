# helper.py

import cv2
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.inception_v3 import InceptionV3, preprocess_input
from tensorflow.keras.applications.inception_v3 import decode_predictions

MODEL_PATH = "best_violence_model.h5"
model = load_model(MODEL_PATH)

# Load InceptionV3 without top layer for feature extraction
feature_extractor = InceptionV3(weights='imagenet', include_top=False, pooling='avg')

def extract_frames(video_path, step=1):
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
            frames.append(rgb)
            timestamps.append(cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0)
        i += 1
    cap.release()
    return np.array(frames), timestamps

def get_feature_vectors(frames):
    preprocessed = preprocess_input(frames.astype(np.float32))
    features = feature_extractor.predict(preprocessed, verbose=0)
    return features  # shape: (N, 2048)

def create_sequences(features, timestamps, seq_length=30):
    sequences = []
    seq_timestamps = []

    for i in range(len(features) - seq_length + 1):
        seq = features[i:i + seq_length]
        sequences.append(seq)
        seq_timestamps.append(timestamps[i + seq_length // 2])  # middle frame timestamp

    return np.array(sequences), seq_timestamps

def detect_violence(video_path, threshold=0.5):
    frames, timestamps = extract_frames(video_path, step=1)
    if frames.shape[0] < 30:
        return []

    features = get_feature_vectors(frames)
    sequences, seq_timestamps = create_sequences(features, timestamps)

    preds = model.predict(sequences, verbose=0)

    if preds.ndim == 1:
        preds = np.expand_dims(preds, axis=-1)

    violence_times = [seq_timestamps[i] for i, pred in enumerate(preds) if pred[0] > threshold]
    return violence_times
