import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect("techconnect.db")
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            roll_no TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            mobile TEXT NOT NULL,
            email TEXT NOT NULL,
            branch TEXT NOT NULL,
            year TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS events (
            event_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            due_date TEXT NOT NULL,
            start_time TEXT NOT NULL,
            instructions TEXT,
            is_completed INTEGER DEFAULT 0
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS participation (
            roll_no TEXT,
            event_id INTEGER,
            enrolled INTEGER DEFAULT 0,
            result TEXT,
            enrollment_time TEXT,
            FOREIGN KEY(roll_no) REFERENCES students(roll_no),
            FOREIGN KEY(event_id) REFERENCES events(event_id),
            PRIMARY KEY (roll_no, event_id)
        )
    ''')
    
    cursor.execute("PRAGMA table_info(participation)")
    columns = [column[1] for column in cursor.fetchall()]
    if "enrollment_time" not in columns:
        cursor.execute("ALTER TABLE participation ADD COLUMN enrollment_time TEXT")
        cursor.execute("UPDATE participation SET enrollment_time = datetime('now') WHERE enrollment_time IS NULL")
    
    conn.commit()
    conn.close()

def register_student(roll_no, name, mobile, email, branch, year, password):
    conn = sqlite3.connect("techconnect.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO students (roll_no, name, mobile, email, branch, year, password) VALUES (?, ?, ?, ?, ?, ?, ?)", 
                       (roll_no, name, mobile, email, branch, year, password))
        conn.commit()
    except sqlite3.IntegrityError:
        raise ValueError("Roll number already registered!")
    finally:
        conn.close()

def get_student(roll_no):
    conn = sqlite3.connect("techconnect.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE roll_no = ?", (roll_no,))
    student = cursor.fetchone()
    conn.close()
    return student

def add_event(name, due_date, start_time, instructions):
    conn = sqlite3.connect("techconnect.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO events (name, due_date, start_time, instructions) VALUES (?, ?, ?, ?)", 
                   (name, due_date, start_time, instructions))
    conn.commit()
    conn.close()

def get_events():
    conn = sqlite3.connect("techconnect.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM events WHERE is_completed = 0")
    events = cursor.fetchall()
    conn.close()
    return events

def get_completed_events():
    conn = sqlite3.connect("techconnect.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM events WHERE is_completed = 1")
    events = cursor.fetchall()
    conn.close()
    return events

def enroll_student(roll_no, event_id):
    conn = sqlite3.connect("techconnect.db")
    cursor = conn.cursor()
    enrollment_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT OR REPLACE INTO participation (roll_no, event_id, enrolled, enrollment_time) VALUES (?, ?, 1, ?)", 
                   (roll_no, event_id, enrollment_time))
    conn.commit()
    conn.close()

def get_participation_count(event_id):
    conn = sqlite3.connect("techconnect.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM participation WHERE event_id = ? AND enrolled = 1", (event_id,))
    count = cursor.fetchone()[0]
    conn.close()
    return count

def get_participants(event_id):
    conn = sqlite3.connect("techconnect.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.roll_no, s.name, s.branch, s.year, p.enrollment_time, p.result
        FROM participation p
        JOIN students s ON p.roll_no = s.roll_no
        WHERE p.event_id = ? AND p.enrolled = 1
        ORDER BY p.enrollment_time
    """, (event_id,))
    participants = cursor.fetchall()
    conn.close()
    return participants

def mark_event_completed(event_id):
    conn = sqlite3.connect("techconnect.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE events SET is_completed = 1 WHERE event_id = ?", (event_id,))
    conn.commit()
    conn.close()

def announce_result(roll_no, event_id, result):
    conn = sqlite3.connect("techconnect.db")
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO participation (roll_no, event_id, enrolled, result) VALUES (?, ?, 1, ?) "
                   "ON CONFLICT(roll_no, event_id) DO UPDATE SET result = ?", (roll_no, event_id, result, result))
    conn.commit()
    conn.close()

def delete_event(event_id):
    conn = sqlite3.connect("techconnect.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM events WHERE event_id = ?", (event_id,))
    cursor.execute("DELETE FROM participation WHERE event_id = ?", (event_id,))
    conn.commit()
    conn.close()

def get_participation(roll_no, event_id):
    conn = sqlite3.connect("techconnect.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM participation WHERE roll_no = ? AND event_id = ?", (roll_no, event_id))
    participation = cursor.fetchone()
    conn.close()
    return participation