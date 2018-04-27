import pandas as pd
import random
from flask import Flask, request, render_template
import flask as f
import os 
from flask_sslify import SSLify
import time

import login_tools



app = Flask(__name__)
sslify = SSLify(app)




@app.route('/logout', methods=['POST'])
def logout():
    del f.session['username']
    return home()

@app.route('/login', methods=['POST'])
def login():
    attempts = login_tools.get_login_attempts(request)
        
    user_name = request.form['user_name'].lower()
    password = request.form['password']
    
    #result = login_tools.login(user_name, password)
    creds = pd.read_csv('/home/2yan/creds.csv', index_col='users')['passwords']
    if user_name not in creds.index:
        return "NO SUCH USER Attempts: {}".format(attempts)
    if user_name in creds.index:
        tru_pass = creds[user_name]
        if login_tools.hash(password) != tru_pass:
            return 'WRONG PASSWORD Attempts: {}'.format(attempts)
    f.session['username'] = user_name
    login_tools.reset_attempts(request)
    return home()


@app.route('/')
def home():
    username = login_tools.get_username(f.session)
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