# generate_model.py

import numpy as np
import os
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.utils import to_categorical

data_dir = "gesture_data"
X, y, labels = [], [], []

label_map = {}
for idx, folder in enumerate(sorted(os.listdir(data_dir))):
    label_map[folder] = idx
    labels.append(folder)
    for file in os.listdir(os.path.join(data_dir, folder)):
        if file.endswith(".npy"):
            path = os.path.join(data_dir, folder, file)
            landmarks = np.load(path)
            X.append(landmarks)
            y.append(idx)

X = np.array(X)
y = to_categorical(y)

np.save("label_classes.npy", np.array(labels))

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = Sequential([
    Dense(128, activation='relu', input_shape=(63,)),
    Dense(64, activation='relu'),
    Dense(len(label_map), activation='softmax')
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.fit(X_train, y_train, epochs=30, validation_data=(X_test, y_test))

model.save("sign_model.h5")
print("✅ Model trained and saved as sign_model.h5")
