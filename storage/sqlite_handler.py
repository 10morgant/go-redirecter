# sqlite_handler.py
import sqlite3
from datetime import datetime

from storage.db_handler import DBHandler


class SQLiteHandler(DBHandler):
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def init_db(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS terms
                               (term TEXT PRIMARY KEY, url TEXT, created_at TEXT, usage_count INTEGER)''')
        self.conn.commit()

    def get_url(self, term):
        self.cursor.execute('SELECT url, usage_count FROM terms WHERE term=?', (term,))
        row = self.cursor.fetchone()
        if row:
            url, usage_count = row
            self.cursor.execute('UPDATE terms SET usage_count=? WHERE term=?', (usage_count + 1, term))
            self.conn.commit()
            return url
        return None

    def add_term(self, term, url):
        created_at = datetime.now().isoformat()
        self.cursor.execute('INSERT OR REPLACE INTO terms (term, url, created_at, usage_count) VALUES (?, ?, ?, ?)',
                            (term, url, created_at, 0))
        self.conn.commit()

    def get_newly_added_terms(self, limit=10):
        self.cursor.execute('SELECT term, created_at FROM terms ORDER BY created_at DESC LIMIT ?', (limit,))
        return self.cursor.fetchall()

    def get_most_commonly_used_terms(self, limit=10):
        self.cursor.execute('SELECT term, usage_count FROM terms ORDER BY usage_count DESC LIMIT ?', (limit,))
        return self.cursor.fetchall()

    def update_term(self, old_term, new_term, url):
        self.cursor.execute('UPDATE terms SET term=?, url=? WHERE term=?', (new_term, url, old_term))
        self.conn.commit()

    def delete_term(self, term):
        self.cursor.execute('DELETE FROM terms WHERE term=?', (term,))
        self.conn.commit()
