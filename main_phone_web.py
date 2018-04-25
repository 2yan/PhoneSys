import pandas as pd
import random
from flask import Flask, request, render_template
import flask as f
import hashlib
import os 

app = Flask(__name__)

def hash(text):
    text = bytes(text, 'utf-8')
    return hashlib.sha224(text).hexdigest()


def get_username():
    try:
        username = f.session['username']
        return username
    except KeyError:
        return False

@app.route('/logout', methods=['POST'])
def logout():
    del f.session['username']
    return home()

@app.route('/login', methods=['POST'])
def login():
    user_name = request.form['user_name'].lower()
    password = request.form['password']
    
    creds = pd.read_csv('/home/2yan/creds.csv', index_col='users')['passwords']
    if user_name not in creds.index:
        return "NO SUCH USER"
    if user_name in creds.index:
        tru_pass = creds[user_name]
        if hash(password) != tru_pass:
            return 'WRONG PASSWORD'
    f.session['username'] = user_name
    return home()


@app.route('/')
def home():
    username = get_username()
    if not username:
        return render_template('login.html')
    return render_template('home.html', user_name = username)

@app.route('/test')
def test():
    x = os.getcwd()
    return str(x)  

app.secret_key = str(random.random() + random.random())

if __name__ == "__main__":
    app.run()