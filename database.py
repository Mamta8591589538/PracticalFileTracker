import sqlite3

DB_NAME = "practical_tracker.db"

def connect_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            subject TEXT,
            status TEXT
        )
    """)
    conn.commit()
    conn.close()

def add_submission(name, subject, status):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO submissions (name, subject, status) VALUES (?, ?, ?)",
                   (name, subject, status))
    conn.commit()
    conn.close()

def fetch_all():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM submissions")
    data = cursor.fetchall()
    conn.close()
    return data

def filter_by_status(status):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    if status == "All":
        cursor.execute("SELECT * FROM submissions")
    else:
        cursor.execute("SELECT * FROM submissions WHERE status=?", (status,))
    data = cursor.fetchall()
    conn.close()
    return data

def search_by_name(name):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM submissions WHERE name LIKE ?", ('%' + name + '%',))
    data = cursor.fetchall()
    conn.close()
    return data

def delete_record(record_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM submissions WHERE id=?", (record_id,))



    conn.commit()
    conn.close()