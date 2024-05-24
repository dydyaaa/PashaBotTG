import sqlite3 

connection = sqlite3.connect('databse.db', check_same_thread=False)
cursor = connection.cursor()

cursor.execute("SELECT * FROM users_payment WHERE id = ?", (637222569,))
print(dict(cursor.fetchall()))