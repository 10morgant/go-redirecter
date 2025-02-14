# sqlite_handler.py
import sqlite3
from datetime import datetime

from storage.db_handler import DBHandler


class SQLiteHandler(DBHandler):
    def __init__(self, db_path):
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS terms (
                term TEXT PRIMARY KEY,
                url TEXT,
                created_at TEXT,
                usage_count INTEGER
            )
        ''')
        conn.commit()
        conn.close()

    def get_url(self, term):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('SELECT url, usage_count FROM terms WHERE term = ?', (term,))
        result = c.fetchone()
        if result:
            url, usage_count = result
            c.execute('UPDATE terms SET usage_count = ? WHERE term = ?', (usage_count + 1, term))
            conn.commit()
            conn.close()
            return url
        conn.close()
        return None

    def add_term(self, term, url):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        created_at = datetime.now().isoformat()
        c.execute('INSERT INTO terms (term, url, created_at, usage_count) VALUES (?, ?, ?, ?)',
                  (term, url, created_at, 0))
        conn.commit()
        conn.close()
