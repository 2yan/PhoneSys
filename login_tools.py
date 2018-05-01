import hashlib
import sql

def hash(text):
    text = bytes(text, 'utf-8')
    return hashlib.sha224(text).hexdigest()


def get_ip_address(request):
    return request.environ.get('HTTP_X_REAL_IP', request.remote_addr)


def get_username(session):
    try:
        username = session['username']
        username = clean_username(username)
        return username
    except KeyError:
        return False
    
def get_login_attempts(request):
    ip_address = get_ip_address(request)
    attempt_count, last_time = sql.record_login_attempt(ip_address)
    return attempt_count, last_time


def reset_attempts(request):
    ip_address = get_ip_address(request)
    return sql.clear_login_attempts(ip_address)


def login(username, password):
    password = hash(password)
    sql.password_check(username, password)
    return 
     
    
def clean_username(username):
    username = username.lower()
    allowed_letters = 'qwertyuiopasdafghjklzxcvbnm1234567890@'
    for character in username: 
        if character not in allowed_letters:
            raise ValueError('Only text and numbers for usernames please')
    return username

def get_role(username):
    username = sql.get_role(username)
    return username



    