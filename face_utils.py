import os
import cv2
import numpy as np
import pandas as pd
from datetime import datetime

FACE_DIR = "data/faces"
ATTENDANCE_FILE = os.path.join(FACE_DIR, "attendance.csv")

# Ensure data directory exists
os.makedirs(FACE_DIR, exist_ok=True)

# Load OpenCV face detector
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

def register_face(name):
    """Captures a face from the webcam and saves the face embedding."""
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            continue
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(100, 100))

        for (x, y, w, h) in faces:
            face = gray[y:y+h, x:x+w]
            face = cv2.resize(face, (100, 100))
            face_path = os.path.join(FACE_DIR, f"{name}.npy")
            np.save(face_path, face)
            cap.release()
            cv2.destroyAllWindows()
            return f"Face registered for {name}!"

        cv2.imshow("Register Face", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    return "No face detected. Try again."

def recognize_face():
    """Recognizes a face from the webcam and marks attendance."""
    cap = cv2.VideoCapture(0)
    known_faces = {f.split(".")[0]: np.load(os.path.join(FACE_DIR, f)) for f in os.listdir(FACE_DIR) if f.endswith(".npy")}

    while True:
        ret, frame = cap.read()
        if not ret:
            continue
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(100, 100))

        for (x, y, w, h) in faces:
            face = gray[y:y+h, x:x+w]
            face = cv2.resize(face, (100, 100))

            # Compare with registered faces
            recognized_name = "Unknown"
            min_mse = float("inf")

            for name, known_face in known_faces.items():
                mse = np.mean((face.astype("float") - known_face.astype("float")) ** 2)
                if mse < min_mse and mse < 1000:  # Threshold
                    min_mse = mse
                    recognized_name = name

            if recognized_name != "Unknown":
                mark_attendance(recognized_name)

            cap.release()
            cv2.destroyAllWindows()
            return recognized_name

        cv2.imshow("Recognizing Face", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    return "No face recognized."

def mark_attendance(name):
    """Logs attendance in a CSV file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if not os.path.exists(ATTENDANCE_FILE):
        df = pd.DataFrame(columns=["Name", "Timestamp"])
    else:
        df = pd.read_csv(ATTENDANCE_FILE)

    new_entry = pd.DataFrame({"Name": [name], "Timestamp": [timestamp]})
    df = pd.concat([df, new_entry], ignore_index=True)
    df.to_csv(ATTENDANCE_FILE, index=False)
