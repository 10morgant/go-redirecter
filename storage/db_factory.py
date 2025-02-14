from storage.json_handler import JSONHandler
from storage.redis_handler import RedisHandler
from storage.sqlite_handler import SQLiteHandler


def get_db_handler(db_type, db_path):
    if db_type == 'sqlite':
        return SQLiteHandler(db_path)
    elif db_type == 'json':
        return JSONHandler(db_path)
    elif db_type == 'redis':
        return RedisHandler(db_path)
    else:
        raise ValueError(f"Unsupported database type: {db_type}")
