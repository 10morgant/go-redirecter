# db_handler.py
from abc import ABC, abstractmethod


class DBHandler(ABC):
    @abstractmethod
    def init_db(self):
        pass

    @abstractmethod
    def get_url(self, term):
        pass

    @abstractmethod
    def add_term(self, term, url):
        pass
