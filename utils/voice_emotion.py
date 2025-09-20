import torch
import numpy as np
import soundfile as sf
from transformers import Wav2Vec2FeatureExtractor, Wav2Vec2ForSequenceClassification

MODEL_NAME = "superb/wav2vec2-base-superb-er"

# Load feature extractor + model
extractor = Wav2Vec2FeatureExtractor.from_pretrained(MODEL_NAME)
model = Wav2Vec2ForSequenceClassification.from_pretrained(MODEL_NAME)

# SER labels from HuggingFace config
id2label = model.config.id2label

def get_voice_emotion(audio_path):
    # Load audio
    speech, rate = sf.read(audio_path)
    if len(speech.shape) > 1:
        speech = np.mean(speech, axis=1)  # convert stereo → mono

    # Preprocess audio
    inputs = extractor(speech, sampling_rate=rate, return_tensors="pt", padding=True)

    # Get logits
    with torch.no_grad():
        logits = model(**inputs).logits

    # Prediction
    predicted_id = torch.argmax(logits, dim=-1).item()
    emotion = id2label[predicted_id]
    score = torch.softmax(logits, dim=-1)[0][predicted_id].item()

    return emotion, round(score * 100, 2)
