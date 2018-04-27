import sqlite3
import pandas as pd




def do_sql(sql,table_name ):
    with sqlite3.connect(table_name) as con:
        cur = con.cursor()
        cur.execute(sql)
        con.commit()

def read_sql(sql, table_name):
    with sqlite3.connect(table_name) as con:
        data = pd.read_sql(sql, con)
    return data

def create_unique_ip_table():
    sql = '''
    create table IF NOT EXISTS ip_address (
    ip TEXT primary key not null,
    login_attempts INTEGER not null
    )
    '''
    do_sql(sql, 'database.db')
         
    return 


def create_unique_account_table():
    sql = '''
    create table IF NOT EXISTS account (
     TEXT primary key not null,
    login_attempts INTEGER not null
    )
    '''
    do_sql(sql, 'database.db')

def record_login_attempt(ip_address):
    create_unique_ip_table()
    get_attempts_sql = 'select * from ip_address where ip = \'{}\''''.format(ip_address)
    data = read_sql(get_attempts_sql, 'database.db')
    
    if len(data) == 0:
        new_record_sql = 'insert into ip_address (ip, login_attempts) values ( \'{}\' , \'0\')'.format(ip_address)
        do_sql(new_record_sql, 'database.db')
    
    if len(data) == 1:
        data.set_index('ip', inplace = True)
        current = data.loc[ip_address, 'login_attempts'] + 1
        increment_sql = ' UPDATE ip_address SET login_attempts = {} WHERE ip = \'{}\''.format(current, ip_address)
        do_sql(increment_sql, 'database.db')
        return current
    
    return 0


def clear_login_attempts(ip_address):
    create_unique_ip_table()
    sql = 'update up_address set login_attempts = 0 where ip = \'{}\''.format(ip_address)
    do_sql(sql, 'database.db')
    return True


#def login(username, password):
    