import sqlite3

con = sqlite3.connect('users.db',  check_same_thread=False)

cur = con.cursor()

cur.execute('CREATE TABLE IF NOT EXISTS users (email TEXT, password TEXT, tel INTEGER, date DATE, address TEXT)')

def add_user(email, password, tel, date, address):
    cur = con.cursor()
    res = cur.execute('SELECT email FROM users').fetchall()
    for i in res:
        if i[0] == email:
            return False

    cur.execute('INSERT INTO users VALUES (?, ?, ?, ?, ?)', (email, password, int(tel), date, address))
    con.commit()
    return True


def login(email, password):
        cur = con.cursor()
        res = cur.execute('SELECT * FROM users').fetchall()
        for i in res:
            if i[0] == email:
                if i[1] == password:
                    return True
                else:
                    return False
        return False

def get_user_by_email(email):
    cur = con.cursor()
    res = cur.execute('SELECT * FROM users').fetchall()
    for i in res:
        if i[0] == email:
            return i
    return None

def all_users():
    cur = con.cursor()
    res = cur.execute('SELECT * FROM users').fetchall()
    print(res)

def delete_user(email):
    cur = con.cursor()
    cur.execute('DELETE FROM users WHERE email=?', (email,))
    con.commit()

def get_user_info(email):
    ...

def update_user(email, password, tel, date, address):
    cur = con.cursor()
    cur.execute('UPDATE users SET password=?, tel=?, date=?, address=? WHERE email=?', (password, tel, date, address, email))
    con.commit()

def delete_table():
    cur = con.cursor()
    cur.execute('DROP TABLE users')
    con.commit()

