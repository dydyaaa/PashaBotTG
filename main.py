import telebot, datetime, schedule, threading, time 
import config as cfg
import buttons as btn
import database as db


bot = telebot.TeleBot(cfg.TOKEN)
user_data = {}

@bot.message_handler(commands=['start'])
def start(message):
    if message.chat.id in cfg.ADMIN:
        bot.send_message(message.chat.id, f'Добро пожаловать в панель администратора! Выберете действие:', reply_markup=btn.admin_start_btn())
    else:
        bot.send_message(message.chat.id, db.check_time_to_pay(message.chat.id))

@bot.callback_query_handler(func=lambda call: call.data in ["add_new", "change", "renew", "cancel", "check", "stat"])
def admin_panel(call):
    match call.data:
        case 'add_new':
            msg = bot.send_message(call.message.chat.id, 'Введите ID пользователя:')
            user_data[call.message.chat.id] = {} 
            user_data[call.message.chat.id]['action'] = call.data
            bot.register_next_step_handler(msg, process_id_step)
        case 'change':
            msg = bot.send_message(call.message.chat.id, 'Введите ID пользователя:')
            user_data[call.message.chat.id] = {}    
            user_data[call.message.chat.id]['action'] = call.data 
            bot.register_next_step_handler(msg, process_id_step)
        case 'renew':
            user_data[call.message.chat.id] = {}  
            msg = bot.send_message(call.message.chat.id, 'Введите ID пользователя:')
            bot.register_next_step_handler(msg, renew)
        case 'cancel':
            msg = bot.send_message(call.message.chat.id, 'Введите ID пользователя:')
            bot.register_next_step_handler(msg, cancel)
        case 'check':
            msg = bot.send_message(call.message.chat.id, 'Введите ID пользователя:')
            bot.register_next_step_handler(msg, check)
        case 'stat':
            payers, non_payers = db.stat()
            payers_message = "Пользователи, оплатившие подписку:\n" + "\n".join([f"Имя пользователя: {payer[1]}, Дата: {payer[4]}" for payer in payers])
            non_payers_message = "Пользователи, не оплатившие подписку:\n" + "\n".join([f"Имя пользователя: {non_payer[1]}" for non_payer in non_payers])
            full_message = f"{payers_message}\n\n{non_payers_message}"
            bot.send_message(call.message.chat.id, f'{full_message}')
    
def process_id_step(message):
    try:
        user_id = int(message.text)
        user_data[message.chat.id]['id'] = user_id
        msg = bot.send_message(message.chat.id, "Введите имя пользователя:")
        bot.register_next_step_handler(msg, process_user_name_step)
    except ValueError:
        msg = bot.send_message(message.chat.id, "Некорректный ввод. Введите ID пользователя:")
        bot.register_next_step_handler(msg, process_id_step)

def process_user_name_step(message):
    user_name = message.text
    user_data[message.chat.id]['user_name'] = user_name
    msg = bot.send_message(message.chat.id, "Введите сумму:")
    bot.register_next_step_handler(msg, process_sum_step)

def process_sum_step(message):
    try:
        sum_value = int(message.text)
        user_data[message.chat.id]['sum'] = sum_value
        msg = bot.send_message(message.chat.id, "Введите дату оплаты (ГГГГ-ММ-ДД):")
        bot.register_next_step_handler(msg, process_date_step)
    except ValueError:
        msg = bot.send_message(message.chat.id, "Некорректный ввод. Введите сумму:")
        bot.register_next_step_handler(msg, process_sum_step)

def process_date_step(message):
    try:
        payment_date = datetime.datetime.strptime(message.text, '%Y-%m-%d')
        user_data[message.chat.id]['date'] = payment_date.strftime('%Y-%m-%d')
        msg = bot.send_message(message.chat.id, "Введите имена файлов:")
        bot.register_next_step_handler(msg, process_name_step)
    except ValueError:
        msg = bot.send_message(message.chat.id, "Некорректный ввод. Введите дату оплаты (ГГГГ-ММ-ДД):")
        bot.register_next_step_handler(msg, process_date_step)

def process_name_step(message):
    user_data[message.chat.id]['name'] = message.text
    data = user_data.pop(message.chat.id)  
    if data['action'] == 'add_new':
        if db.add_new(data['id'], data['user_name'], data['sum'], data['date'], data['name']) == 'ok':
            bot.send_message(message.chat.id, "Данные успешно добавлены.")
        else:
            bot.send_message(message.chat.id, "При добавлении пользователя произошла ошибка.")
    elif data['action'] == 'change':
        db.change(data['id'], data['user_name'], data['sum'], data['date'], data['name'])
        bot.send_message(message.chat.id, "Данные успешно изменены.")
            
def renew(message):
    try:
        user_id = int(message.text)
        user_data[message.chat.id]['id'] = user_id
        msg = bot.send_message(message.chat.id, "Введите количество месяцев продления:")
        bot.register_next_step_handler(msg, renew_step)
    except ValueError:
        msg = bot.send_message(message.chat.id, "Некорректный ввод. Введите ID пользователя:")
        bot.register_next_step_handler(msg, renew)

def renew_step(message):
    try:
        user_data[message.chat.id]['num'] = int(message.text)
        if user_data[message.chat.id]['num'] < 0:
            user_data[message.chat.id]['num'] = 1
        data = user_data.pop(message.chat.id) 
        db.renew(data['id'], data['num'])
        bot.send_message(message.chat.id, 'Данные успешно обновлены.')
    except ValueError:
        msg = bot.send_message(message.chat.id, "Некорректный ввод. Введите количество месяцев продления еще раз:")
        bot.register_next_step_handler(msg, renew_step)

def cancel(message):
    try:
        user_id = int(message.text)
        db.cancel(user_id)
        bot.send_message(message.chat.id, 'Пользователь удален.')
    except ValueError:
        msg = bot.send_message(message.chat.id, 'Некорректный ввод. Введите ID пользователя:')
        bot.register_next_step_handler(msg, cancel)

def check(message):
    try:
        user_id = int(message.text)
        bot.send_message(message.chat.id, db.check(user_id))
    except ValueError:
        msg = bot.send_message(message.chat.id, 'Некорректный ввод. Введите ID пользователя:')
        bot.register_next_step_handler(msg, check)

def send_notifications():
    current_date = datetime.datetime.now().date()
    users = db.get_notifications_users()
    
    for user_id, two_days_before, one_day_before, payment_day in users:
        if current_date == two_days_before.date():
            bot.send_message(user_id, f'Уважаемый пользователь, через два дня вам необходимо произвести оплату.')
        elif current_date == one_day_before.date():
            bot.send_message(user_id, f'Уважаемый пользователь, завтра вам необходимо произвести оплату.')
        elif current_date == payment_day.date():
            db.update_status(user_id)
            bot.send_message(user_id, f'Вы не произвели оплату.')
        

def job():
    send_notifications()

schedule.every().day.at("15:20").do(job)

def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    schedule_thread = threading.Thread(target=run_schedule)
    schedule_thread.start()
    bot.polling()
