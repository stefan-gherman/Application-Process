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


@app.route('/get-mentors-nicks-city')
def get_mentor_nicks():
    mentor_nicks = data_manager.get_mentor_nicknames_city('Miskolc')

    return render_template('mentor_nicks.html', mentor_nicks=mentor_nicks)


@app.route('/get-info-by-name')
def get_name_info():
    info = data_manager.get_info_by_name('Carol')
    print(info)
    return render_template('carols_hat.html', info=info)


@app.route('/get-info-mail')
def get_mail_info():
    info = data_manager.get_info_mailprovider('@adipiscingenimmi.edu')
    print(info)
    return render_template('carols_hat.html', info=info)


@app.route('/add-applicant')
def add_applicant():
    applicant = data_manager.insert_applicant(' Markus', 'Schaffarzyk', '003620 / 725 - 2666',
                                              'djnovus@groovecoverage.com', 54823)
    print(applicant)
    return render_template('new_applicant.html', applicant=applicant)


@app.route('/update-applicant')
def update_applicant():
    applicant = data_manager.update_applicant('Jemima', 'Foreman', '003670/223-7459')
    return render_template('new_applicant.html', applicant=applicant)


@app.route('/delete_applicant')
def delete_applicant():
    data_manager.delete_applicant('mauriseu.net')
    return redirect(url_for('index'))


@app.errorhandler(404)
def process_404(e):
    return render_template('404.html')



if __name__ == '__main__':
    app.run(debug=True)
