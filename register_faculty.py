# register_faculty.py

import cv2
import os

# Input faculty details
faculty_id = input("Enter Faculty ID: ").strip()
faculty_name = input("Enter Faculty Name: ").strip().replace(" ", "_")
folder_name = f"{faculty_id}_{faculty_name}"
save_path = os.path.join("train_images", folder_name)

# Create folder if not exists
os.makedirs(save_path, exist_ok=True)

# Open webcam
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
print("\n📸 Capturing 5 face images... Press 'c' to capture each.")

count = 0
while True:
    success, frame = cap.read()
    if not success:
        print("Camera error.")
        break

    # Show frame
    cv2.imshow("Register Faculty - Press 'c' to capture, 'q' to quit", frame)
    key = cv2.waitKey(1)

    # Press 'c' to capture image
    if key == ord('c'):
        count += 1
        img_path = os.path.join(save_path, f"{count}.jpg")
        cv2.imwrite(img_path, frame)
        print(f"✅ Saved: {img_path}")
        if count == 5:
            print("\n✅ Registration complete.")
            break

    # Press 'q' to quit early
    if key == ord('q'):
        print("\n❌ Registration aborted.")
        break

cap.release()
cv2.destroyAllWindows()
