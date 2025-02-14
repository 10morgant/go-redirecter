try:
    import redis

    redis_available = True
except ImportError as e:
    print(e)
    redis_available = False

from datetime import datetime

from storage.db_handler import DBHandler

if redis_available:
    class RedisHandler(DBHandler):
        def __init__(self, db_path):
            self.db = redis.StrictRedis.from_url(db_path, decode_responses=True)
            self.prefix = "go:"

        def init_db(self):
            pass

        def get_url(self, term):
            key = self.prefix + term
            url = self.db.hget(key, 'url')
            if url:
                self.db.hincrby(key, 'usage_count', 1)
                return url
            return None

        def add_term(self, term, url):
            key = self.prefix + term
            self.db.hmset(key, {
                'url': url,
                'created_at': datetime.now().isoformat(),
                'usage_count': 0
            })

        def get_newly_added_terms(self, limit=10):
            keys = self.db.keys(self.prefix + '*')
            terms = []
            for key in keys:
                term_data = self.db.hgetall(key)
                terms.append((key[len(self.prefix):], term_data['created_at']))
            terms.sort(key=lambda x: x[1], reverse=True)
            return terms[:limit]

        def get_most_commonly_used_terms(self, limit=10):
            keys = self.db.keys(self.prefix + '*')
            terms = []
            for key in keys:
                term_data = self.db.hgetall(key)
                terms.append((key[len(self.prefix):], int(term_data['usage_count'])))
            terms.sort(key=lambda x: x[1], reverse=True)
            return terms[:limit]
else:
    class RedisHandler(DBHandler):
        def init_db(self):
            pass

        def get_url(self, term):
            pass

        def add_term(self, term, url):
            pass

        def __init__(self, db_path):
            raise ImportError("Redis is not installed. Please install Redis to use this database type.")
