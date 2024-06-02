import database as db
import datetime

current_date = datetime.datetime.now().date()
#print(db.get_notifications_users())

users = db.get_notifications_users()
    
for user_id, two_days_before, one_day_before in users:
    if current_date == two_days_before.date():
        print(123)
    elif current_date == one_day_before.date():
        print(321)

# 1. Уведомления
# 2. Создание файлов 
# 3. Изменение файлов
# 4. Изменения статуса