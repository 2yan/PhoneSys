

from flask import Flask, request, render_template
import flask as f


app = Flask(__name__)


@app.route('/login', methods=['POST'])
def login():
    user_name = request.form['user_name']
    password = request.form['password']
    f.session['username'] = user_name
    return  user_name + password

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/test')
def test():
    try:
        username = f.session['username']
    except KeyError:
        return 'Sorry Not Logged In'
    return username


if __name__ == "__main__":
    app.secret_key = 'POMCEINVDSLJCO12903ucneasjcp0h#lSnc834win3nasidj390'
    app.run()