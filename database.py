import sqlite3

DB = "memory.db"


def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        role TEXT,
        prompt TEXT,
        image_path TEXT,
        output_path TEXT
    )
    """)

    conn.commit()
    conn.close()


def create_user(username, password):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("INSERT INTO users (username, password) VALUES (?,?)",
              (username, password))
    conn.commit()
    conn.close()


def get_user(username):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    user = c.fetchone()
    conn.close()
    return user


def save_message(user_id, role, prompt, image_path=None, output_path=None):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""
        INSERT INTO messages (user_id, role, prompt, image_path, output_path)
        VALUES (?,?,?,?,?)
    """, (user_id, role, prompt, image_path, output_path))
    conn.commit()
    conn.close()


def get_messages(user_id):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""
        SELECT role, prompt, image_path, output_path
        FROM messages
        WHERE user_id=?
        ORDER BY id ASC
    """, (user_id,))
    data = c.fetchall()
    conn.close()
    return data