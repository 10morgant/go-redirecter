# json_handler.py
import json
import os
from datetime import datetime

from storage.db_handler import DBHandler


class JSONHandler(DBHandler):
    def __init__(self, db_path):
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        if not os.path.exists(self.db_path):
            with open(self.db_path, 'w') as f:
                json.dump({}, f)

    def get_url(self, term):
        with open(self.db_path, 'r') as f:
            data = json.load(f)
        if term in data:
            data[term]['usage_count'] += 1
            with open(self.db_path, 'w') as f:
                json.dump(data, f)
            return data[term]['url']
        return None

    def add_term(self, term, url):
        with open(self.db_path, 'r') as f:
            data = json.load(f)
        data[term] = {
            'url': url,
            'created_at': datetime.now().isoformat(),
            'usage_count': 0
        }
        with open(self.db_path, 'w') as f:
            json.dump(data, f)
