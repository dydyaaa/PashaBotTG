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

def add_new(user_id, price, current_date, name):
    payment_day = datetime.strptime(current_date, '%Y-%m-%d')
    two_days_before = (payment_day - timedelta(days=2)).strftime('%Y-%m-%d')
    one_day_before = (payment_day - timedelta(days=1)).strftime('%Y-%m-%d')
    payment_day = payment_day.strftime('%Y-%m-%d')
    cursor.execute('''
                INSERT INTO users_payment (id, sum, payment_day, two_days_before, one_day_before, name) 
                VALUES (?, ?, ?, ?, ?, ?)''', 
                (user_id, price, payment_day, two_days_before, one_day_before, name))
    connection.commit()

def change(user_id, price, current_date, name):
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
                        (price, payment_day, two_days_before, one_day_before, name, user_id))
    connection.commit()

def renew(user_id):
    
    cursor.execute('''
        UPDATE users_payment
        SET status = 1,
            payment_day = date(payment_day, '+1 month'),
            two_days_before = date(payment_day, '+1 month', '-2 day'),
            one_day_before = date(payment_day, '+1 month', '-1 day')
        WHERE id = ?''', (user_id,))
    
    connection.commit()

def cancel(user_id):

    cursor.execute('DELETE FROM users_payment WHERE id = ?', (user_id,))
    connection.commit()

def check(user_id):

    cursor.execute("SELECT sum, payment_day, name FROM users_payment WHERE id = ?", (user_id,))
    result = cursor.fetchone()

    if result:
        payment_sum, payment_day, name = result
        info_text = f"Сумма оплаты: {payment_sum}\nДата оплаты: {payment_day}\nИмена файлов: {name}"
    else:
        info_text = "Пользователь с таким ID не найден."
    
    return info_text

def stat():
    cursor.execute('SELECT * FROM users_payment WHERE status = 0')
    cursor.fetchall()
    cursor.execute('SELECT * FROM users_payment WHERE status = 1')
    cursor.fetchall()

def check_time_to_pay(id):
    cursor.execute("SELECT payment_day FROM users_payment WHERE id = ?", (id,))
    return f'{cursor.fetchone()}'