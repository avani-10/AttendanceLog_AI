# generate_encodings.py

import os
import cv2
import face_recognition
import pickle

image_path = 'train_images'
encoding_path = 'encodings/faculty_encodings.pkl'
os.makedirs('encodings', exist_ok=True)

encode_list = []
metadata = []

folders = os.listdir(image_path)
print(f"🔍 Found {len(folders)} faculty folders.")

for folder in folders:
    folder_path = os.path.join(image_path, folder)
    if not os.path.isdir(folder_path):
        continue

    try:
        faculty_id, faculty_name = folder.split("_", 1)
    except ValueError:
        print(f"❌ Skipping folder: {folder} (invalid name format)")
        continue

    for file in os.listdir(folder_path):
        img_path = os.path.join(folder_path, file)
        img = cv2.imread(img_path)
        if img is None:
            continue

        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encodings = face_recognition.face_encodings(rgb_img)

        if encodings:
            encode_list.append(encodings[0])
            metadata.append({
                "id": faculty_id,
                "name": faculty_name.replace("_", " ")
            })

print(f"✅ Encoded {len(encode_list)} faces. Saving...")

with open(encoding_path, 'wb') as f:
    pickle.dump((encode_list, metadata), f)

print(f"📦 Saved encodings to {encoding_path}")
