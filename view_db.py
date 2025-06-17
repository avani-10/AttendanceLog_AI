import sqlite3
import pandas as pd

conn = sqlite3.connect("db/attendance.db")
df = pd.read_sql_query("SELECT * FROM faculty_attendance", conn)
conn.close()

print(df)
