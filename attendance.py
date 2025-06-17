import cv2
import numpy as np
import face_recognition
import os
import pickle
from datetime import datetime
import sqlite3

# Load face encodings
with open("encodings/faculty_encodings.pkl", "rb") as f:
    known_encodings, known_metadata = pickle.load(f)

print(f"✅ Loaded {len(known_encodings)} face encodings.")

# Setup SQLite database
os.makedirs("db", exist_ok=True)
conn = sqlite3.connect("db/attendance.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS faculty_attendance (
    id TEXT,
    name TEXT,
    login_time TEXT,
    logout_time TEXT,
    date TEXT
)
""")
conn.commit()

# Function to mark and return status
def mark_attendance(faculty_id, name):
    now = datetime.now()
    date_today = now.strftime("%Y-%m-%d")
    current_time = now.strftime("%H:%M:%S")

    cursor.execute("""
        SELECT login_time, logout_time FROM faculty_attendance
        WHERE id = ? AND date = ?
    """, (faculty_id, date_today))
    record = cursor.fetchone()

    if not record:
        # First time today → mark login
        cursor.execute("""
            INSERT INTO faculty_attendance (id, name, login_time, logout_time, date)
            VALUES (?, ?, ?, NULL, ?)
        """, (faculty_id, name, current_time, date_today))
        conn.commit()
        return "Login Marked"

    elif record[0] and not record[1]:
        # Mark logout
        cursor.execute("""
            UPDATE faculty_attendance
            SET logout_time = ?
            WHERE id = ? AND date = ?
        """, (current_time, faculty_id, date_today))
        conn.commit()
        return "Logout Marked"

    else:
        return "Already Marked"

# Start webcam
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

while True:
    success, img = cap.read()
    if not success:
        print("Camera error.")
        break

    # Resize for faster processing
    small_img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)
    rgb_small = cv2.cvtColor(small_img, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(rgb_small)
    face_encodings = face_recognition.face_encodings(rgb_small, face_locations)

    for encodeFace, faceLoc in zip(face_encodings, face_locations):
        matches = face_recognition.compare_faces(known_encodings, encodeFace, tolerance=0.38)
        faceDis = face_recognition.face_distance(known_encodings, encodeFace)
        matchIndex = np.argmin(faceDis)

        y1, x2, y2, x1 = [v * 2 for v in faceLoc]  # Rescale back to original size

        if matches[matchIndex]:
            faculty_id = known_metadata[matchIndex]["id"]
            name = known_metadata[matchIndex]["name"]
            display_name = f"{faculty_id} - {name}"

            status = mark_attendance(faculty_id, name)

            if status == "Login Marked":
                color = (0, 255, 0)  # Green
            elif status == "Logout Marked":
                color = (255, 0, 0)  # Blue
            else:
                color = (128, 128, 128)  # Gray

            cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
            cv2.rectangle(img, (x1, y2 - 55), (x2, y2), color, cv2.FILLED)
            cv2.putText(img, display_name, (x1 + 6, y2 - 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
            cv2.putText(img, status, (x1 + 6, y2 - 8),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 1)
        else:
            # Unknown face
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 0, 255), cv2.FILLED)
            cv2.putText(img, "Unknown", (x1 + 6, y2 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

    cv2.imshow("Faculty Attendance", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
conn.close()
cv2.destroyAllWindows()
