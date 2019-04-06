import os

from flask import Flask
from flask import flash, render_template, request, session
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

from table import *

engine = create_engine('sqlite:///stock.db', echo=True)
app = Flask(__name__)


@app.route('/')
@app.route('/index')
def home():
    if not session.get('logged_in'):
        return render_template('base.html')
    else:
        return render_template('login.html')


@app.route('/logout')
def logout():
    session['logged_in'] = False
    return home()


@app.route('/login', methods=['POST'])
def login():
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])

    Session = sessionmaker(bind=engine)
    s = Session()

    query = s.query(User).filter(User.username.in_(POST_USERNAME),
                                 User.password.in_(POST_PASSWORD))
    try:
        if query.first():
            session['logged_in'] = True
    except OperationalError:
        flash('User does not exist')
    return home()


if __name__ == '__main__':
    app.secret_key = os.urandom(100)
    app.run(debug=True)
