from abc import ABC, abstractmethod


class DBHandler(ABC):
    @abstractmethod
    def get_url(self, term):
        pass

    @abstractmethod
    def add_term(self, term, url):
        pass

    @abstractmethod
    def get_newly_added_terms(self):
        pass

    @abstractmethod
    def get_most_commonly_used_terms(self):
        pass

    @abstractmethod
    def update_term(self, old_term, new_term, url):
        pass

    def delete_term(self, term):
        pass
