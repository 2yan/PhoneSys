import sqlite3
import pandas as pd
import time

database_name = 'database.db'


def do_sql(sql):
    with sqlite3.connect(database_name) as con:
        cur = con.cursor()
        cur.execute(sql)
        con.commit()

def read_sql(sql):
    with sqlite3.connect(database_name) as con:
        data = pd.read_sql(sql, con)
    return data

def create_ip_table():
    sql = '''
    create table IF NOT EXISTS ip_address (
    ip TEXT primary key not null,
    login_attempts INTEGER not null,
    last_attempt_time INTEGER not null
    )
    '''
    do_sql(sql)
    return 


def create_account_table():
    sql = '''
    create table IF NOT EXISTS account (
    username TEXT primary key not null,
    password INTEGER not null
    )
    '''
    do_sql(sql)
    
    sql = '''replace into account (username, password) values('admin', '383b39a5c9a275ae22c0ec1ba427716b5826fbf15ad1e168b2886fc6')'''
    do_sql(sql)
    return 


def record_login_attempt(ip_address):
    now = time.time()
    
    create_ip_table()
    get_attempts_sql = 'select * from ip_address where ip = \'{}\''''.format(ip_address)
    data = read_sql(get_attempts_sql)
    
    if len(data) == 0:
        new_record_sql = "insert into ip_address (ip, login_attempts, last_attempt_time) values ( '{}' , '0', '{}')".format(ip_address, now)
        do_sql(new_record_sql)
    
    if len(data) == 1:
        data.set_index('ip', inplace = True)
        
        last_time = int(data.loc[ip_address, 'last_attempt_time'])
        current = data.loc[ip_address, 'login_attempts'] + 1
        increment_sql = ' UPDATE ip_address SET login_attempts = {}, last_attempt_time = {} WHERE ip = \'{}\''.format(current,now, ip_address)
        do_sql(increment_sql)
        return current, now -  last_time
    
    return 0, 9999




def clear_login_attempts(ip_address):
    create_ip_table()
    sql = 'update ip_address set login_attempts = 0 where ip = \'{}\''.format(ip_address)
    do_sql(sql)
    return True


def password_check(username, password):
    create_account_table()
    sql = 'select username, password from account where username = \'{}\' '.format(username) 
    data = read_sql(sql)
    if len(data) == 0:
        raise ValueError('No Such User')
    data.set_index('username', inplace = True)
    
    if data.loc[username, 'password'] != password:
        raise ValueError('Wrong Password')
        
def make_user(username, password):
    create_account_table()
    sql = "insert into account (username, password) values ('{}', '{}')".format(username, password)
    do_sql(sql)
    return 