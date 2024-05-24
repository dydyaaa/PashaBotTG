import sqlite3
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


connection = sqlite3.connect('databse.db', check_same_thread=False)
cursor = connection.cursor()

# current_date = datetime.now()
# payment_day = (current_date + relativedelta(months=1)).strftime('%Y-%m-%d')
# two_days_before = (current_date + relativedelta(months=1) - timedelta(days=2)).strftime('%Y-%m-%d')
# one_day_before = (current_date + relativedelta(months=1) - timedelta(days=1)).strftime('%Y-%m-%d')
# payment_day = payment_day + relativedelta(months=1)


cursor.execute('''
        CREATE TABLE IF NOT EXISTS users_payment (
        id INTEGER PRIMARY KEY, 
        status BOOLEAN DEFAULT 0,
        sum INTEGER,
        payment_day TIMESTAMP,
        two_days_before TIMESTAMP,
        one_day_before TIMESTAMP,
        name TEXT
        )''')

def add_new(id, sum, current_date, name):
    payment_day = datetime.strptime(current_date, '%Y-%m-%d')
    two_days_before = (payment_day - timedelta(days=2)).strftime('%Y-%m-%d')
    one_day_before = (payment_day - timedelta(days=1)).strftime('%Y-%m-%d')
    payment_day = payment_day.strftime('%Y-%m-%d')
    cursor.execute('''
                INSERT INTO users_payment (id, sum, payment_day, two_days_before, one_day_before, name) 
                VALUES (?, ?, ?, ?, ?, ?)''', 
                (id, sum, payment_day, two_days_before, one_day_before, name))
    connection.commit()

def change(id, sum, current_date, name):
    payment_day = datetime.strptime(current_date, '%Y-%m-%d')
    two_days_before = (payment_day - timedelta(days=2)).strftime('%Y-%m-%d')
    one_day_before = (payment_day - timedelta(days=1)).strftime('%Y-%m-%d')
    payment_day = payment_day.strftime('%Y-%m-%d')
    cursor.execute('''
                    UPDATE users_payment 
                    SET sum = ?,
                        payment_day = ?,
                        two_days_before = ?,
                        one_day_before = ?,
                        name = ?
                    WHERE id = ?''',
                        (sum, payment_day, two_days_before, one_day_before, name, id))
    connection.commit()

def stat():
    cursor.execute('SELECT * FROM users_payment WHERE status = 0')

def check_time_to_pay(id):
    cursor.execute("SELECT payment_day FROM users_payment WHERE id = ?", (id,))
    return f'{cursor.fetchone()}'