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
        return username
    except KeyError:
        return False
    
    
    
def get_login_attempts(request):
    ip_address = get_ip_address(request)
    return sql.record_login_attempt(ip_address)


def reset_attempts(request):
    ip_address = get_ip_address(request)
    return sql.clear_login_attempts(ip_address)