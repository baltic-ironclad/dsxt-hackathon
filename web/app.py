import os
import json

from flask import Flask
from flask import flash, render_template, request, session

with open('database.json', 'r') as database:
    data = json.load(database)

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def home():
    if session.get('logged_in'):
        return render_template('base.html')
    else:
        return render_template('login.html')


@app.route('/send')
def send():
    return render_template('send.html')


@app.route('/register', methods=['GET'])
def register():
    user = {
        'username': str(request.form['username']),
        'password': str(request.form['password'])
    }
    data.append(user)
    with open('database.json', 'a') as database:
        json.dump(data, database)
    return home()


@app.route('/logout')
def logout():
    session['logged_in'] = False
    return home()


@app.route('/login', methods=['POST'])
def login():
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])

    for user in data:
        if user['username'] == POST_USERNAME and user['password'] == POST_PASSWORD:
            session['logged_in'] = True
    if not session['logged_in']:
        flash('Wrong password')

    return home()


if __name__ == '__main__':
    app.secret_key = os.urandom(100)
    app.run(debug=True)
