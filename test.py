import sqlite3
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

connection = sqlite3.connect('databse.db', check_same_thread=False)
cursor = connection.cursor()

cursor.execute("SELECT payment_day FROM users_payment WHERE id = ?", (637222569,))
payment_day = datetime.strptime(cursor.fetchone()[0], '%Y-%m-%d')
payment_day = (payment_day + timedelta()).strftime('%Y-%m-%d')
print(payment_day)