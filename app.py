from flask import Flask, redirect, request, render_template

from storage.db_factory import get_db_handler

app = Flask(__name__)


class MyApp:
    def __init__(self, host, port, debug, db_type, db_path):
        self.db_handler = get_db_handler(db_type, db_path)
        self.host = host
        self.port = port
        self.debug = debug
        self.db_type = db_type
        self.db_path = db_path

        app.add_url_rule('/', 'show_terms', self.show_terms)
        app.add_url_rule('/go/', 'show_terms', self.show_terms)
        app.add_url_rule('/go/<string:term>', 'redirect_to_term', self.redirect_to_term)
        app.add_url_rule('/new', 'new_entry', self.new_entry)
        app.add_url_rule('/add', 'add_term', self.add_term, methods=['POST'])
        app.add_url_rule('/edit/<string:term>', 'edit_entry', self.edit_entry)
        app.add_url_rule('/update', 'update_term', self.update_term, methods=['POST'])
        app.add_url_rule('/delete/<string:term>', 'delete_entry', self.delete_entry)
        app.add_url_rule('/del', 'delete_term', self.delete_term, methods=['POST'])

    @app.errorhandler(404)
    def page_not_found(self):
        return render_template('404.j2.html'), 404

    def get_db(self):
        return get_db_handler(self.db_type, self.db_path)

    def delete_entry(self, term):
        url = self.get_db().get_url(term)
        return render_template("delete_entry.j2.html", term=term, url=url)

    def delete_term(self):
        term = request.form['term']
        url = request.form['url']
        print(term, url)
        self.get_db().delete_term(term)
        return redirect('/go')

    def edit_entry(self, term):
        url = self.get_db().get_url(term)
        if url:
            return render_template("edit_entry.j2.html", term=term, url=url)
        else:
            return redirect('/go')

    def update_term(self):
        old_term = request.form['old_term']
        new_term = request.form['term']
        url = request.form['url']
        print(old_term, new_term, url)
        self.get_db().update_term(old_term, new_term, url)
        return redirect('/go/{}'.format(new_term))

    def redirect_to_term(self, term):
        if term in ['go', 'home']:
            return redirect('/go')
        url = self.get_db().get_url(term)
        if url:
            return redirect(url)
        else:
            return self.new_entry(term)

    def new_entry(self, term=None):
        return render_template("new_entry.j2.html", term=term)

    def add_term(self):
        term = request.form['term']
        url = request.form['url']
        self.get_db().add_term(term, url)
        return redirect('/go/{}'.format(term))

    def show_terms(self):
        newly_added_terms = [
            (term, created_at)
            for term, created_at in self.get_db().get_newly_added_terms(5)
            if term
        ]
        most_commonly_used_terms = [
            (term, usage_count)
            for term, usage_count in self.get_db().get_most_commonly_used_terms(5)
            if term
        ]
        return render_template("terms.j2.html", newly_added_terms=newly_added_terms,
                               most_commonly_used_terms=most_commonly_used_terms)

    def run(self):
        app.run(host=self.host, port=self.port, debug=self.debug)


if __name__ == '__main__':
    import argparse
    import os

    parser = argparse.ArgumentParser(description='Run the Flask app.')
    parser.add_argument('--host', type=str, default=os.getenv('FLASK_HOST', '0.0.0.0'), help='Host to run the app on')
    parser.add_argument('--port', type=int, default=os.getenv('FLASK_PORT', 5000), help='Port to run the app on')
    parser.add_argument('--debug', action='store_true', default=os.getenv('FLASK_DEBUG', 'false').lower() == 'true',
                        help='Run the app in debug mode')
    parser.add_argument('--db-type', type=str, choices=['sqlite', 'json', 'redis'],
                        default=os.getenv('DB_TYPE', 'sqlite'), help='Database type to use')
    parser.add_argument('--db-path', type=str, default=os.getenv('DB_PATH', 'terms.db'), help='Path to the database file')

    args = parser.parse_args()

    my_app = MyApp(args.host, args.port, args.debug, args.db_type, args.db_path)
    my_app.run()
