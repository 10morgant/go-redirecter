import argparse

from flask import Flask, redirect, request, render_template

from storage.db_factory import get_db_handler


class MyApp:
    def __init__(self, host, port, debug, db_type, db_path):
        self.app = Flask(__name__)
        self.db_handler = get_db_handler(db_type, db_path)
        self.host = host
        self.port = port
        self.debug = debug

        self.app.add_url_rule('/go/', 'show_terms', self.show_terms)
        self.app.add_url_rule('/go/<string:term>', 'redirect_to_term', self.redirect_to_term)
        self.app.add_url_rule('/new', 'new_entry', self.new_entry)
        self.app.add_url_rule('/add', 'add_term', self.add_term, methods=['POST'])
        self.app.add_url_rule('/edit/<string:term>', 'edit_entry', self.edit_entry)
        self.app.add_url_rule('/update', 'update_term', self.update_term, methods=['POST'])
        self.app.add_url_rule('/delete/<string:term>', 'delete_entry', self.delete_entry)
        self.app.add_url_rule('/del', 'delete_term', self.delete_term, methods=['POST'])

    def delete_entry(self, term):
        url = self.db_handler.get_url(term)
        return render_template("delete_entry.j2.html", term=term, url=url)

    def delete_term(self):
        term = request.form['term']
        url = request.form['url']
        print(term, url)
        self.db_handler.delete_term(term)
        return redirect('/go')

    def edit_entry(self, term):
        url = self.db_handler.get_url(term)
        if url:
            return render_template("edit_entry.j2.html", term=term, url=url)
        else:
            return redirect('/go')

    def update_term(self):
        old_term = request.form['old_term']
        new_term = request.form['term']
        url = request.form['url']
        print(old_term, new_term, url)
        self.db_handler.update_term(old_term, new_term, url)
        return redirect('/go/{}'.format(new_term))

    def redirect_to_term(self, term):
        url = self.db_handler.get_url(term)
        if url:
            return redirect(url)
        else:
            return self.new_entry(term)

    def new_entry(self, term=None):
        return render_template("new_entry.j2.html", term=term)

    def add_term(self):
        term = request.form['term']
        url = request.form['url']
        self.db_handler.add_term(term, url)
        return redirect('/go/{}'.format(term))

    def show_terms(self):
        newly_added_terms = [
            (term, created_at)
            for term, created_at in self.db_handler.get_newly_added_terms()
            if term
        ]
        most_commonly_used_terms = [
            (term, usage_count)
            for term, usage_count in self.db_handler.get_most_commonly_used_terms()
            if term
        ]
        return render_template("terms.j2.html", newly_added_terms=newly_added_terms,
                               most_commonly_used_terms=most_commonly_used_terms)

    def run(self):
        self.app.run(host=self.host, port=self.port, debug=self.debug)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run the Flask app.')
    parser.add_argument('--host', type=str, default='127.0.0.1', help='Host to run the app on')
    parser.add_argument('--port', type=int, default=5000, help='Port to run the app on')
    parser.add_argument('--debug', action='store_true', help='Run the app in debug mode')
    parser.add_argument('--db-type', type=str, choices=['sqlite', 'json', 'redis'], default='redis',
                        help='Database type to use')
    default_db = '/home/tim/Github/personal/url_redirect/terms.json'
    parser.add_argument('--db-path', type=str, default="redis://localhost:6379/0",
                        help='Path to the database file')

    args = parser.parse_args()

    my_app = MyApp(args.host, args.port, args.debug, args.db_type, args.db_path)
    my_app.run()
