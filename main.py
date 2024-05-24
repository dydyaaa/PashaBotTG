import telebot, os, sqlite3, datetime, test
import config as cfg
import buttons as btn
import messages as msg
import database as db


bot = telebot.TeleBot(cfg.TOKEN)
user_data = {}

@bot.message_handler(commands=['start'])
def start(message):
    if message.chat.id == cfg.ADMIN:
        bot.send_message(message.chat.id, msg.start_admin, reply_markup=btn.admin_start_btn())
    else:
        bot.send_message(message.chat.id, db.check_time_to_pay(message.chat.id))

@bot.callback_query_handler(func=lambda call: call.data in ["add_new", "change", "renew", "cancel", "check", "stat"])
def admin_panel(call):
    match call.data:
        case 'add_new':
            user_data[call.message.chat.id] = {} 
            user_data[call.message.chat.id]['action'] = call.data
            msg = bot.send_message(call.message.chat.id, "Введите ID пользователя:")
            bot.register_next_step_handler(msg, process_id_step)
        case 'change':
            user_data[call.message.chat.id] = {}    
            user_data[call.message.chat.id]['action'] = call.data 
            msg = bot.send_message(call.message.chat.id, "Введите ID пользователя:")
            bot.register_next_step_handler(msg, process_id_step)
        case 'renew':
            pass
        case 'cancel':
            pass
        case 'check':
            pass
        case 'stat':
            pass
    
def process_id_step(message):
    try:
        user_id = int(message.text)
        user_data[message.chat.id]['id'] = user_id
        msg = bot.send_message(message.chat.id, "Введите сумму:")
        bot.register_next_step_handler(msg, process_sum_step)
    except ValueError:
        msg = bot.send_message(message.chat.id, "Некорректный ввод. Введите ID пользователя:")
        bot.register_next_step_handler(msg, process_id_step)

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
        print(f"{payment_date} {payment_date.strftime('%Y-%m-%d')}")
        msg = bot.send_message(message.chat.id, "Введите имя:")
        bot.register_next_step_handler(msg, process_name_step)
    except ValueError:
        msg = bot.send_message(message.chat.id, "Некорректный ввод. Введите дату оплаты (ГГГГ-ММ-ДД):")
        bot.register_next_step_handler(msg, process_date_step)

def process_name_step(message):
    user_data[message.chat.id]['name'] = message.text
    data = user_data.pop(message.chat.id)  
    if data['action'] == 'add_new':
        db.add_new(data['id'], data['sum'], data['date'], data['name'])
        bot.send_message(message.chat.id, "Данные успешно добавлены.")
    elif data['action'] == 'change':
        db.change(data['id'], data['sum'], data['date'], data['name'])
        bot.send_message(message.chat.id, "Данные успешно изменены.")
            

if __name__ == "__main__":
    bot.polling()