"""
Module 8: Translation History — database layer.
Uses SQLite so no external DB server is required.
"""
import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "database", "history.db")


def get_connection():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    return conn


def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_text TEXT NOT NULL,
            translated_text TEXT NOT NULL,
            source_lang TEXT,
            target_lang TEXT,
            favorite INTEGER DEFAULT 0,
            created_at TEXT
        )
    """)
    conn.commit()
    conn.close()


def add_entry(source_text, translated_text, source_lang, target_lang):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO history (source_text, translated_text, source_lang, target_lang, created_at) "
        "VALUES (?, ?, ?, ?, ?)",
        (source_text, translated_text, source_lang, target_lang, datetime.now().isoformat(timespec="seconds")),
    )
    conn.commit()
    conn.close()


def get_all(search=None):
    conn = get_connection()
    cur = conn.cursor()
    if search:
        cur.execute(
            "SELECT * FROM history WHERE source_text LIKE ? OR translated_text LIKE ? ORDER BY id DESC",
            (f"%{search}%", f"%{search}%"),
        )
    else:
        cur.execute("SELECT * FROM history ORDER BY id DESC")
    rows = cur.fetchall()
    conn.close()
    return rows


def toggle_favorite(entry_id, favorite: bool):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE history SET favorite = ? WHERE id = ?", (int(favorite), entry_id))
    conn.commit()
    conn.close()


def delete_entry(entry_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM history WHERE id = ?", (entry_id,))
    conn.commit()
    conn.close()


def clear_all():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM history")
    conn.commit()
    conn.close()
