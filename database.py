import sqlite3

DB = "memory.db"


def init_db():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        role TEXT,
        message TEXT,
        image_path TEXT,
        output_path TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


# ---------------- USERS ----------------
def create_user(username, password):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        (username, password)
    )

    conn.commit()
    conn.close()


def get_user(username):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("SELECT * FROM users WHERE username=?", (username,))
    user = cur.fetchone()

    conn.close()
    return user


# ---------------- CHAT ----------------
def save_message(user_id, role, message, image_path=None, output_path=None):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO messages (user_id, role, message, image_path, output_path)
    VALUES (?, ?, ?, ?, ?)
    """, (user_id, role, message, image_path, output_path))

    conn.commit()
    conn.close()


def get_chat(user_id):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""
    SELECT role, message, image_path, output_path
    FROM messages
    WHERE user_id=?
    ORDER BY id ASC
    """, (user_id,))

    data = cur.fetchall()
    conn.close()
    return data