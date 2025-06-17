# export_attendance.py

import sqlite3
import pandas as pd
from datetime import datetime
import os

# Connect to the database
conn = sqlite3.connect("db/attendance.db")

# Optional: change this to export any specific date
today = datetime.now().strftime("%Y-%m-%d")

# Query today's attendance
query = """
SELECT id, name, login_time, logout_time, date
FROM faculty_attendance
WHERE date = ?
"""

df = pd.read_sql_query(query, conn, params=(today,))
conn.close()

# Export directory
os.makedirs("exports", exist_ok=True)
filename = f"exports/faculty_attendance_{today}.xlsx"

# Write to Excel
df.to_excel(filename, index=False)

print(f"📦 Attendance exported to {filename}")
