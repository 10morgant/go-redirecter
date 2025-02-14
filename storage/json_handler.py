# json_handler.py
import json
from datetime import datetime

from storage.db_handler import DBHandler


class JSONHandler(DBHandler):
    def __init__(self, db_path):
        self.db_path = db_path
        self.load_db()

    def load_db(self):
        try:
            with open(self.db_path, 'r') as f:
                self.db = json.load(f)
        except FileNotFoundError:
            self.db = {}

    def save_db(self):
        with open(self.db_path, 'w') as f:
            json.dump(self.db, f)

    def init_db(self):
        pass

    def get_url(self, term):
        if term in self.db:
            self.db[term]['usage_count'] += 1
            self.save_db()
            return self.db[term]['url']
        return None

    def add_term(self, term, url):
        self.db[term] = {
            'url': url,
            'created_at': datetime.now().isoformat(),
            'usage_count': 0
        }
        self.save_db()

    def get_newly_added_terms(self, limit=10):
        terms = [(term, data['created_at']) for term, data in self.db.items()]
        terms.sort(key=lambda x: x[1], reverse=True)
        return terms[:limit]

    def get_most_commonly_used_terms(self, limit=10):
        terms = [(term, data['usage_count']) for term, data in self.db.items()]
        terms.sort(key=lambda x: x[1], reverse=True)
        return terms[:limit]
