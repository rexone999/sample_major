# helper.py
import cv2
import numpy as np
from keras.models import load_model
from keras.applications.inception_v3 import InceptionV3, preprocess_input
from keras.applications.inception_v3 import decode_predictions
from keras.preprocessing import image

# Load your trained LSTM model
model = load_model("vlstm_92.h5")

# Load CNN feature extractor (InceptionV3 without top)
cnn_model = InceptionV3(include_top=False, pooling='avg', input_shape=(299, 299, 3))

def extract_frames(video_path, max_frames=30):
    cap = cv2.VideoCapture(video_path)
    frames = []
    timestamps = []

    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_interval = max(1, total_frames // max_frames)

    count = 0
    while cap.isOpened() and len(frames) < max_frames:
        ret, frame = cap.read()
        if not ret:
            break
        if count % frame_interval == 0:
            frame = cv2.resize(frame, (299, 299))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frames.append(frame)
            timestamps.append(count / fps)
        count += 1

    cap.release()
    return np.array(frames), timestamps

def extract_features(frames):
    preprocessed = preprocess_input(frames.astype(np.float32))
    features = cnn_model.predict(preprocessed, verbose=0)  # shape: (n_frames, 2048)
    if features.shape[0] < 30:
        # Pad with zeros to maintain (30, 2048)
        padding = np.zeros((30 - features.shape[0], 2048))
        features = np.vstack((features, padding))
    return np.expand_dims(features[:30], axis=0)  # shape: (1, 30, 2048)

def detect_violence(video_path):
    frames, timestamps = extract_frames(video_path)
    if len(frames) == 0:
        return []

    features = extract_features(frames)  # shape: (1, 30, 2048)
    preds = model.predict(features, verbose=0)

    # Assume binary classification with sigmoid output
    if preds[0][0] > 0.5:
        return timestamps  # violent
    else:
        return []  # non-violent
