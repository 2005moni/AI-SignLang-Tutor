# collect_data.py

import cv2
import numpy as np
import os
import mediapipe as mp

# ---- Setup ----
mp_hands = mp.solutions.hands
data_dir = "gesture_data"
os.makedirs(data_dir, exist_ok=True)

# ---- Ask for Label ----
label = input("Enter the phrase label (e.g., hello, thank_you, how_are_you): ").strip().lower()
if not label:
    print("❌ Label cannot be empty.")
    exit()

label_dir = os.path.join(data_dir, label)
os.makedirs(label_dir, exist_ok=True)
print(f"📂 Saving to {label_dir}")

# ---- Webcam ----
cap = cv2.VideoCapture(0)
with mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7) as hands:
    index = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb)

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                mp.solutions.drawing_utils.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                landmarks = []
                for lm in hand_landmarks.landmark:
                    landmarks.extend([lm.x, lm.y, lm.z])

                if len(landmarks) == 63:
                    cv2.putText(frame, f"{label} (Samples: {index})", (10, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                    key = cv2.waitKey(1)
                    if key == ord(' '):
                        np.save(os.path.join(label_dir, f"{index}.npy"), np.array(landmarks))
                        print(f"✅ Saved sample {index}")
                        index += 1

        cv2.imshow("Collect Gesture Data (press 'space' to save, 'q' to quit)", frame)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
print("📦 Data collection complete.")
