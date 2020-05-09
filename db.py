import sqlite3
from config import sudos

conn = sqlite3.connect("main.db")

cur = conn.cursor()

for sudo in sudos:
    cur.execute(f"CREATE TABLE IF NOT EXISTS msgs_to_{sudo} (from_chat_id, from_message_id, to_message_id)")
