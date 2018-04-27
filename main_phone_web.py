import random
from flask import Flask, request, render_template
import flask as f

from flask_sslify import SSLify


import login_tools



app = Flask(__name__)
sslify = SSLify(app)



def alert(error_text):
    return '''
        <script>
        alert("{}");
        window.history.back();
        </script>
        '''.format(error_text)

@app.route('/logout', methods=['POST'])
def logout():
    try:
        del f.session['username']
    except KeyError:
        pass
    return home()

@app.route('/login', methods=['POST'])
def login():
    
        
    user_name = request.form['user_name']
    password = request.form['password']
    
    attempts, last_time = login_tools.get_login_attempts(request)
    if last_time > 60  * 3:
        login_tools.reset_attempts(request)
    try:
        if (attempts > 5) and (last_time < 30):
            return(render_template('wait_page.html', wait_time = 30))
        
        user_name = login_tools.clean_username(user_name)
        login_tools.login(user_name, password)
    except ValueError as v:
        return alert(str(v) + ' ATTEMPTS: {}'.format(attempts))

    
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
   return render_template('test.html')

app.secret_key = str(random.random() + random.random())

if __name__ == "__main__":
    app.run()