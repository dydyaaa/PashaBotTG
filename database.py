import sqlite3
import file_manager as fm
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


connection = sqlite3.connect('database.db', check_same_thread=False)
cursor = connection.cursor()


cursor.execute('''
        CREATE TABLE IF NOT EXISTS users_payment (
        id INTEGER PRIMARY KEY, 
        user_name TEXT,
        status BOOLEAN DEFAULT 0,
        sum INTEGER,
        payment_day TIMESTAMP,
        two_days_before TIMESTAMP,
        one_day_before TIMESTAMP,
        name TEXT
        )''')

def add_new(user_id, user_name, price, current_date, name):
    payment_day = datetime.strptime(current_date, '%Y-%m-%d')
    two_days_before = (payment_day - timedelta(days=2)).strftime('%Y-%m-%d')
    one_day_before = (payment_day - timedelta(days=1)).strftime('%Y-%m-%d')
    payment_day = payment_day.strftime('%Y-%m-%d')
    try:
        cursor.execute('''
                    INSERT INTO users_payment (id, user_name, sum, payment_day, two_days_before, one_day_before, name) 
                    VALUES (?, ?, ?, ?, ?, ?, ?)''', 
                    (user_id, user_name, price, payment_day, two_days_before, one_day_before, name))
        connection.commit()
        fm.create_files(name)
        return 'ok'
    except Exception:
        return 'error'

def change(user_id, user_name, price, current_date, name):
    
    cursor.execute('SELECT name FROM users_payment WHERE id = ?', (user_id,))
    result = cursor.fetchone()
    current_names = result[0].split(', ') if result else []
    new_names = name.split(', ')
    fm.manage_files(current_names, new_names)

    payment_day = datetime.strptime(current_date, '%Y-%m-%d')
    two_days_before = (payment_day - timedelta(days=2)).strftime('%Y-%m-%d')
    one_day_before = (payment_day - timedelta(days=1)).strftime('%Y-%m-%d')
    payment_day = payment_day.strftime('%Y-%m-%d')
    cursor.execute('''
                    UPDATE users_payment 
                    SET user_name = ?,
                        sum = ?,
                        payment_day = ?,
                        two_days_before = ?,
                        one_day_before = ?,
                        name = ?
                    WHERE id = ?''',
                        (user_name, price, payment_day, two_days_before, one_day_before, name, user_id))
    connection.commit()

def renew(user_id, months):
    
    months_str = f"+{months} month" 
    query = f'''
        UPDATE users_payment
        SET status = 1,
            payment_day = date(payment_day, '{months_str}'),
            two_days_before = date(payment_day, '{months_str}', '-2 day'),
            one_day_before = date(payment_day, '{months_str}', '-1 day')
        WHERE id = ?'''

    cursor.execute(query, (user_id,))
    cursor.execute('SELECT name FROM users_payment WHERE id = ?', (user_id, ))
    name = cursor.fetchone()[0]
    fm.update_to_one(name)
    connection.commit()

def cancel(user_id):
    cursor.execute('SELECT name FROM users_payment WHERE id = ?', (user_id, ))
    name = cursor.fetchone()[0]
    fm.delete_files(name)
    cursor.execute('DELETE FROM users_payment WHERE id = ?', (user_id,))
    connection.commit()

def check(user_id):

    cursor.execute("SELECT user_name, sum, payment_day, name FROM users_payment WHERE id = ?", (user_id,))
    result = cursor.fetchone()

    if result:
        user_name, payment_sum, payment_day, name = result
        info_text = f"Имя пользователя: {user_name}\nСумма оплаты: {payment_sum}\nДата оплаты: {payment_day}\nИмена файлов: {name}"
    else:
        info_text = "Пользователь с таким ID не найден."
    
    return info_text

def stat():
    cursor.execute('''
            SELECT * FROM users_payment 
            WHERE status = 1''')
    payers = cursor.fetchall()

    cursor.execute('''
            SELECT * FROM users_payment
            WHERE status = 0''')
    non_payers = cursor.fetchall()
    
    return payers, non_payers

def check_time_to_pay(user_id):
    cursor.execute("SELECT payment_day FROM users_payment WHERE id = ?", (user_id,))
    result = cursor.fetchone()
    if result:
        return result
    else:
        return f'Пользователь не найден'
    
def get_notifications_users():
    cursor.execute('SELECT id, two_days_before, one_day_before, payment_day FROM users_payment')
    users = cursor.fetchall()
    notification_users = []
    for user in users:
        user_id, two_days_before, one_day_before, payment_day = user
        two_days_before = datetime.strptime(two_days_before, '%Y-%m-%d')
        one_day_before = datetime.strptime(one_day_before, '%Y-%m-%d')
        payment_day = datetime.strptime(payment_day, '%Y-%m-%d')
        notification_users.append((user_id, two_days_before, one_day_before, payment_day))
    return notification_users

def update_status(user_id):
    cursor.execute("UPDATE users_payment SET status = 0 WHERE id = ?", (user_id,))
    connection.commit()
    cursor.execute('SELECT name FROM users_payment WHERE id = ?', (user_id, ))
    name = cursor.fetchone()[0]
    fm.update_to_zero(name)
