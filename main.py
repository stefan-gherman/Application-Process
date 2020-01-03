import data_manager
from flask import Flask, render_template, redirect, url_for
from psycopg2 import sql

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/mentors-with-best-first-name')
def mentor_names():
    # We get back dictionaries here (for details check 'database_common.py')
    mentor_names = data_manager.get_mentor_names_by_first_name('László')

    return render_template('mentor_names.html', mentor_names=mentor_names)


@app.route('/get-mentors-names')
def get_mentors_names():
    mentor_names = data_manager.get_mentors_names()

    return render_template('mentor_names.html', mentor_names=mentor_names)


if __name__ == '__main__':
    app.run(debug=True)
