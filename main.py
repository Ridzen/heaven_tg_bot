import telebot
import logging
import json
import os
from datetime import datetime, timedelta
from settings import TOKEN

bot = telebot.TeleBot(TOKEN)

current_directory = os.path.dirname(os.path.abspath(__file__))
nick_file = os.path.join(current_directory, 'user_nicks.json')

logging.basicConfig(filename='requests_log.txt', level=logging.INFO)


def load_nicks():
    if os.path.exists(nick_file):
        with open(nick_file, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}


def save_nicks(nicks):
    with open(nick_file, 'w') as f:
        json.dump(nicks, f, ensure_ascii=False, indent=4)


user_nicks = load_nicks()
awaiting_nicks = {}


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот, который может тегать всех участников группы.\n"
                          "Что-бы тегнуть всех участников группы, напишите: Взываю к небесам\n"
                          "Что-бы настроить себе ник, вы можете написать: Выбор божественного имени")


@bot.message_handler(func=lambda message: 'выбор божественного имени' in message.text.lower())
def request_nick(message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    awaiting_nicks[user_id] = chat_id
    bot.reply_to(message, "Пожалуйста, напишите свой ник.")


@bot.message_handler(func=lambda message: message.from_user.id in awaiting_nicks)
def receive_nick(message):
    user_id = message.from_user.id
    chat_id = awaiting_nicks.pop(user_id)
    nick = message.text

    if chat_id not in user_nicks:
        user_nicks[chat_id] = {}

    user_nicks[chat_id][user_id] = nick
    save_nicks(user_nicks)

    bot.reply_to(message, f"Твой ник '{nick}' был успешно сохранен для этой беседы!")


@bot.message_handler(func=lambda message: 'взываю к небесам' in message.text.lower())
def tag_all(message):
    chat_id = message.chat.id
    thread_id = message.message_thread_id
    try:
        members = bot.get_chat_administrators(chat_id)
        tag_message = "Тегаю всех участников группы:\n"
        for member in members:
            user = member.user
            nick = user_nicks.get(chat_id, {}).get(user.id, None)
            if nick:
                tag_message += f"[{nick}](tg://user?id={user.id}) "
            else:
                if user.username:
                    tag_message += f"@{user.username} "
                else:
                    tag_message += f"[{user.first_name}](tg://user?id={user.id}) "
        if thread_id:
            bot.send_message(chat_id, tag_message, reply_to_message_id=thread_id, parse_mode='Markdown')
        else:
            bot.send_message(chat_id, tag_message, parse_mode='Markdown')
    except Exception as e:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logging.error(f'DATETIME: {current_time}, ERROR: {e}')
        bot.reply_to(message, "Не удалось получить список участников группы.")
        print(e)



def polling_with_retry():
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logging.error(f'DATETIME: {current_time}, ERROR: {e}')
        next_polling_time = datetime.now() + timedelta(seconds=5)
        while datetime.now() < next_polling_time:
            pass
        polling_with_retry()


polling_with_retry()
