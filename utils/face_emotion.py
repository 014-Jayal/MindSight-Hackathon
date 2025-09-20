import cv2
from fer import FER
import time
from collections import Counter

detector = FER(mtcnn=True)

def analyze_video_stream(duration=5):
    """
    Analyzes webcam video for a set duration and finds the dominant emotion.
    """
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        return "Error: Could not access webcam.", None

    start_time = time.time()
    detected_emotions = []

    while (time.time() - start_time) < duration:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Analyze the frame
        result = detector.detect_emotions(frame)
        if result:
            # Get the top emotion for the first face found
            top_emotion = max(result[0]["emotions"], key=result[0]["emotions"].get)
            detected_emotions.append(top_emotion)

    cap.release()

    if not detected_emotions:
        return "No face detected during the scan.", None

    # Find the most common (dominant) emotion
    dominant_emotion = Counter(detected_emotions).most_common(1)[0][0]
    
    return dominant_emotion.capitalize(), None