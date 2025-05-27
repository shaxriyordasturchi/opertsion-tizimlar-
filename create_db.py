import sqlite3

conn = sqlite3.connect('worktime.db')
c = conn.cursor()

c.execute('''
    CREATE TABLE IF NOT EXISTS employees (
        username TEXT PRIMARY KEY,
        firstname TEXT,
        lastname TEXT,
        chat_id TEXT
    )
''')

c.execute('''
    CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        firstname TEXT,
        lastname TEXT,
        login_time TEXT,
        logout_time TEXT
    )
''')

conn.commit()
conn.close()
print("✅ Baza yaratildi.")
