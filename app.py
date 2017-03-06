from flask import Flask, render_template, request, redirect, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from logging import Formatter, FileHandler
from database import db_session, init_db
from models import User, Job
from forms import *
from scheduler import scheduler, load_jobs
import logging

app = Flask(__name__)
app.config.from_object('config')
init_db()
scheduler()

# Automatically tear down SQLAlchemy.

@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()

# Login required decorator.

def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
#@login_required
def home():
    inject_jobs = db_session.query(Job)
    return render_template('pages/dashboard.html', inject_jobs=inject_jobs)


@app.route('/about')
def about():
    return render_template('pages/placeholder.about.html')


@app.route('/job', methods=['GET', 'POST'])
#@login_required
def add_job():
    form = JobForm(request.form)
    if form.validate_on_submit():
        new_job = Job(form.title.data,
            form.database.data,
            form.host.data,
            form.username.data,
            form.password.data,
            form.spreadsheet.data,
            form.sheet.data,
            form.query.data,
            form.schedule.data)
        db_session.add(new_job)
        db_session.commit()
        return redirect(url_for('home'))
    else:
        print form.errors
    return render_template('pages/job.html', form=form)


@app.route('/login')
def login():
    form = LoginForm(request.form)
    return render_template('forms/login.html', form=form)


@app.route('/register')
def register():
    form = RegisterForm(request.form)
    return render_template('forms/register.html', form=form)


@app.route('/forgot')
def forgot():
    form = ForgotForm(request.form)
    return render_template('forms/forgot.html', form=form)

# Error handlers.


@app.errorhandler(500)
def internal_error(error):
    #db_session.rollback()
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
