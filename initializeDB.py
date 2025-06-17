# delete_db.py
import os

db_path = "db/attendance.db"

if os.path.exists(db_path):
    os.remove(db_path)
    print("🗑️ attendance.db deleted.")
else:
    print("⚠️ attendance.db not found.")

