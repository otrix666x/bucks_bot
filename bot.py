import telebot
from telebot import types
import time
import sqlite3
import keyboard, config

bot = telebot.TeleBot(config.token)

@bot.message_handler(commands=['start'])
def start_bot(message):
    username = str(message.from_user.username)
    userid = str(message.chat.id)
    connect = sqlite3.connect('bot.db')
    q = connect.cursor()
    q.execute('''CREATE TABLE IF NOT EXISTS users(
        id TEXT, username TEXT
    )''')
    q.execute('''CREATE TABLE IF NOT EXISTS admins(
        id TEXT
    )''')
    connect.commit()
    res = q.execute(f"SELECT * FROM users where id = {userid}").fetchone()
    if res is None:
        q.execute("INSERT INTO users(id, username) VALUES ('%s', '%s')"%(userid, username))
        connect.commit()
        bot.send_photo(userid, "https://i.imgur.com/hB06KX3.jpg", caption="<b>ТЕКСТ ПРИВЕТСВИЯ НОВОГО ПОЛЬЗОВАТЕЛЯ</b>",parse_mode="html", reply_markup=keyboard.menu)
    else:
        bot.send_photo(userid, "https://i.imgur.com/hB06KX3.jpg", caption="<b>ТЕКСТ ПРИВЕТСВИЯ РАНЕЕ ЗАРЕГИСТРИРОВАНОГО ПОЛЬЗОВАТЕЛЯ</b>", parse_mode="html", reply_markup=keyboard.menu)

@bot.message_handler(commands=['admin'])
def adm(message):
    adm = []
    connect = sqlite3.connect('bot.db')
    q = connect.cursor()
    res = q.execute("SELECT id FROM admins").fetchall()
    for i in res:
        adm.append(i[0])
    if message.chat.id in config.admins or str(message.chat.id) in adm:
        bot.send_sticker(message.chat.id, "CAACAgIAAxkBAAECfL1g2F23u2MLMzpNIeVbfc9wb-7hoAACzAADe04qEF9nkGXzCRxAIAQ", reply_markup=keyboard.adm)
    else:
        bot.send_message(message.chat.id, "Для вас эта команда недоступна🙅")

@bot.message_handler(content_types=['text'])
def txt_answ(message):
    userid = message.chat.id
    if message.text ==  "☘️Довереные магазины☘️":
        bot.delete_message(chat_id=userid, message_id=message.message_id)
        bot.send_photo(userid, "https://i.imgur.com/4goCZtM.jpg", caption="описание", reply_markup=keyboard.trust_shop)
    
    if message.text == "🍊Эл.Услуги🍊":
        bot.delete_message(chat_id=userid, message_id=message.message_id)
        key = types.InlineKeyboardMarkup()
        key1 = types.InlineKeyboardButton("Отзывы", url="https://t.me/joinchat/FpM6lg6gvy4wYTcy")
        key2 = types.InlineKeyboardButton("Прайс",url="https://t.me/citrusxxxx")
        key3 = types.InlineKeyboardButton("Оператор", url="https://t.me/CitrusShopM")
        key.row(key1, key2, key3)
        key.row(types.InlineKeyboardButton("❌Закрыть", callback_data="delete"))
        bot.send_photo(userid, "https://i.imgur.com/BhZdFHG.jpg", caption="описание", reply_markup=key)
    
    if message.text == "🧑‍💻Админ🧑‍💻":
        key = types.InlineKeyboardMarkup()
        key.row(types.InlineKeyboardButton("❌Закрыть", callback_data="delete"))
        bot.delete_message(chat_id=userid, message_id=message.message_id)
        bot.send_message(userid, f"<a href='https://t.me/jambo_squirt'> Cвязаться с админом</a>",disable_web_page_preview=True, parse_mode="html", reply_markup=key)
    
    if message.text == "Чаты🤼":
        key = types.InlineKeyboardMarkup()
        key.row(types.InlineKeyboardButton("❌Закрыть", callback_data="delete"))
        bot.delete_message(chat_id=userid, message_id=message.message_id)
        bot.send_message(userid, f"ОПИСАНИЕ....<a href='https://t.me/jambo_squirt'>Ссылка на пост</a>",disable_web_page_preview=True, parse_mode="html", reply_markup=key)

    if message.text == "Меню🎆":
        bot.delete_message(chat_id=userid, message_id=message.message_id)
        bot.send_message(userid, "🎆", reply_markup=keyboard.menu)
    
    if message.text == "Запустить рассылку🔈":
        bot.delete_message(chat_id=userid, message_id=message.message_id)
        bot.send_message(userid, "Тип рассылки?", reply_markup=keyboard.spam)
    
    if message.text == "Добавить админа🧑‍🔧":
        bot.delete_message(chat_id=userid, message_id=message.message_id)
        send = bot.send_message(userid, "Введите ID пользователя")
        bot.clear_step_handler_by_chat_id(userid)
        bot.register_next_step_handler(send, new_adm)
    
    if message.text == "💫PORTAL DNR💫":
        bot.delete_message(chat_id=userid, message_id=message.message_id)
        key = types.InlineKeyboardMarkup()
        key1 = types.InlineKeyboardButton("КНОПКА 1", url="https://t.me/jambo_squirt")
        key2 = types.InlineKeyboardButton("КНОПКА 2",url="https://t.me/jambo_squirt")
        key3 = types.InlineKeyboardButton("КНОПКА 3", url="https://t.me/jambo_squirt")
        key.row(key1, key2, key3)
        key.row(types.InlineKeyboardButton("❌Закрыть", callback_data="delete"))
        bot.send_photo(userid, "https://i.imgur.com/BhZdFHG.jpg", caption="описание", reply_markup=key)



        
        





@bot.callback_query_handler(func=lambda call: True)
def confirm_answer(call):
    userid = call.message.chat.id
    if call.data == "1":
        key = types.InlineKeyboardMarkup()
        key.row(types.InlineKeyboardButton("txt", url='https://t.me/CitrusShopM'))
        key.row(types.InlineKeyboardButton("Вернуться назад", callback_data="back"))
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.send_photo(userid, "https://i.imgur.com/BhZdFHG.jpg", caption="описание", reply_markup=key)
    
    if call.data == "3":
        key = types.InlineKeyboardMarkup()
        key.row(types.InlineKeyboardButton("txt", url='https://t.me/CitrusShopM'))
        key.row(types.InlineKeyboardButton("Вернуться назад", callback_data="back"))
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.send_photo(userid, "https://i.imgur.com/BhZdFHG.jpg", caption="описание", reply_markup=key)
    
    if call.data == "5":
        key = types.InlineKeyboardMarkup()
        key.row(types.InlineKeyboardButton("txt", url='https://t.me/CitrusShopM'))
        key.row(types.InlineKeyboardButton("Вернуться назад", callback_data="back"))
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.send_photo(userid, "https://i.imgur.com/BhZdFHG.jpg", caption="описание", reply_markup=key)
    
    if call.data == "7":
        key = types.InlineKeyboardMarkup()
        key.row(types.InlineKeyboardButton("txt", url='https://t.me/CitrusShopM'))
        key.row(types.InlineKeyboardButton("Вернуться назад", callback_data="back"))
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.send_photo(userid, "https://i.imgur.com/BhZdFHG.jpg", caption="описание", reply_markup=key)
    
    if call.data == "back":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.send_photo(userid, "https://i.imgur.com/4goCZtM.jpg", caption="описание", reply_markup=keyboard.trust_shop)
    
    if call.data == "delete":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    
    if call.data == "stop_spam":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    
    if call.data == "text":
        send = bot.edit_message_text(chat_id=userid, message_id=call.message.message_id, text="📩Введите текст для рассылки📩")
        bot.clear_step_handler_by_chat_id(userid)
        bot.register_next_step_handler(send, conf_text)
    
    if call.data == "pics":
        send = bot.edit_message_text(chat_id=userid, message_id=call.message.message_id, text="🌌Введите ссылку на фото с бота @imgurbot_bot🌌")
        bot.clear_step_handler_by_chat_id(userid)
        bot.register_next_step_handler(send, caption)
    
    
    if call.data == "text_but":
        send = bot.edit_message_text(chat_id=userid, message_id=call.message.message_id, text="📩Введите текст для рассылки📩")
        bot.clear_step_handler_by_chat_id(userid)
        bot.register_next_step_handler(send, text_but)
    
    if call.data == "pics_but":
        send = bot.edit_message_text(chat_id=userid, message_id=call.message.message_id, text="🌌Введите ссылку на фото с бота @imgurbot_bot🌌")
        bot.clear_step_handler_by_chat_id(call.message.chat.id)
        bot.register_next_step_handler(send, caption1)

def caption1(message):
    link = message.text
    send = bot.send_message(message.chat.id, "Введите текст под фото")
    bot.clear_step_handler_by_chat_id(message.chat.id)
    bot.register_next_step_handler(send, but_pic, link)

def but_pic(message, link):
    capt = message.text
    send = bot.send_message(message.chat.id, "Введите текст ссылку для кнопки\n"\
        "<b>ТЕКСТ И ССЫЛКА ЧЕРЕЗ ПРОБЕЛ!</b>", parse_mode='html')
    bot.clear_step_handler_by_chat_id(message.chat.id)
    bot.register_next_step_handler(send, conf_but_pic, capt, link)

def conf_but_pic(message,capt, link):
    btn = message.text
    arr = message.text.split(" ")
    key = types.InlineKeyboardMarkup()
    key1 = types.InlineKeyboardButton(f"{arr[0]}", url=f"{arr[1]}")
    key2 = types.InlineKeyboardButton("Закрыть", callback_data="delete")
    key.row(key1)
    key.row(key2)
    send = bot.send_photo(message.chat.id, link, caption=f"{capt}\n\n"\
        "Отправлять? ДА/НЕТ", parse_mode="html", reply_markup=key)
    bot.clear_step_handler_by_chat_id(message.chat.id)
    bot.register_next_step_handler(send, send_but_pic, capt, link, btn)

def send_but_pic(message,capt,link,btn):
    if message.text.lower() == "да":
        arr = btn.split(" ")
        key = types.InlineKeyboardMarkup()
        key1 = types.InlineKeyboardButton(f"{arr[0]}", url=f"{arr[1]}")
        key2 = types.InlineKeyboardButton("Закрыть", callback_data="delete")
        key.row(key1)
        key.row(key2)
        try:
            connect = sqlite3.connect('bot.db')
            q = connect.cursor()
            res = q.execute("SELECT id FROM users").fetchall()
            k = 0
            bot.send_message(message.chat.id, "<b>Рассылка начнеться через 3 секунды...</b>", parse_mode="html")
            time.sleep(3)
            bot.send_message(message.chat.id, "<b>Рассылка пошла...</b>", parse_mode="html")
            for i in res:
                try:
                    bot.send_photo(i[0], link, caption=capt, parse_mode="html", reply_markup=key)
                    time.sleep(0.3)
                except Exception as e:
                    print(e)
                k += 1
            bot.send_message(message.chat.id, f"Рассылку получило {k} чел.")

        except Exception as e:
            print(e)

    else:
        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
        bot.send_message(message.chat.id, "Рассылка отменена!")



def text_but(message):
    text = message.text
    send = bot.send_message(message.chat.id, "Введите текст ссылку для кнопки\n"\
        "<b>ТЕКСТ И ССЫЛКА ЧЕРЕЗ ПРОБЕЛ!</b>", parse_mode='html')
    bot.clear_step_handler_by_chat_id(message.chat.id)
    bot.register_next_step_handler(send, conf_all_but, text)

def conf_all_but(message, text):
    but = message.text
    arr = message.text.split(" ")
    key = types.InlineKeyboardMarkup()
    key1 = types.InlineKeyboardButton(f"{arr[0]}", url=f"{arr[1]}")
    key2 = types.InlineKeyboardButton("Закрыть", callback_data="delete")
    key.row(key1)
    key.row(key2)
    
    send = bot.send_message(message.chat.id, f"{text}\n\n"\
        "Отправлять? ДА/НЕТ", reply_markup=key)
    bot.clear_step_handler_by_chat_id(message.chat.id)
    bot.register_next_step_handler(send, send_all_but, but, text)




def send_all_but(message, but, text):
    if message.text.lower() == "да":
        arr = but.split(" ")
        key = types.InlineKeyboardMarkup()
        key1 = types.InlineKeyboardButton(f"{arr[0]}", url=f"{arr[1]}")
        key2 = types.InlineKeyboardButton("Закрыть", callback_data="delete")
        key.row(key1)
        key.row(key2)
        try:
            connect = sqlite3.connect('bot.db')
            q = connect.cursor()
            res = q.execute("SELECT id FROM users").fetchall()
            bot.send_message(message.chat.id, "<b>Рассылка начнеться через 3 сукунды!</b>", parse_mode="html")
            time.sleep(3)
            bot.send_message(message.chat.id, "<b>Рассылка пошла!</b>", parse_mode="html")
            k = 0
            for i in res:
                try:
                    bot.send_message(i[0], text,disable_web_page_preview=True, parse_mode="html", reply_markup=key)
                    time.sleep(0.3)
                except Exception as e:
                    print(e)
                k += 1
            bot.send_message(message.chat.id, f"Рассылку получило {k} чел.")
            
        except:
            bot.send_message(message.chat.id, "Ошибка")
    else:
        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
        bot.send_message(message.chat.id, "Рассылка отменена!")


def caption(message):
    photo = message.text
    text = bot.send_message(message.chat.id, "Введите текст под фото")
    bot.clear_step_handler_by_chat_id(message.chat.id)
    bot.register_next_step_handler(text, conf_photo, photo)

def conf_photo(message, photo):
    text = message.text
    send = bot.send_photo(message.chat.id, photo, caption=f"{text}\n\n"\
        "Отправлять? ДА/НЕТ")
    bot.clear_step_handler_by_chat_id(message.chat.id)
    bot.register_next_step_handler(send, send_photo,text, photo)




def send_photo(message,text, photo):
    if message.text.lower() == "да":
        try:
            caption = message.text
            connect = sqlite3.connect('bot.db')
            q = connect.cursor()
            res = q.execute("SELECT id FROM users").fetchall()
            bot.send_message(message.chat.id, "<b>Рассылка начнеться через 3 сукунды!</b>", parse_mode="html")
            time.sleep(3)
            bot.send_message(message.chat.id, "<b>Рассылка пошла!</b>", parse_mode="html")
            k = 0
            for i in res:
                try:
                    bot.send_photo(i[0], photo,caption=caption, parse_mode="html", reply_markup=keyboard.user_spam)
                    time.sleep(0.3)
                except:
                    pass
                k += 1
            bot.send_message(message.chat.id, f"Рассылку получило {k} чел.")
            
        except:
            bot.send_message(message.chat.id, "Ошибка")
    else:
        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
        bot.send_message(message.chat.id, "Рассылка отменена!")



def conf_text(message):
    text = message.text
    send = bot.send_message(message.chat.id, f"{text}\n\n"\
        "Отправлять? ДА/НЕТ")
    bot.clear_step_handler_by_chat_id(message.chat.id)
    bot.register_next_step_handler(send, send_all, text)



def send_all(message, text):
    if message.text.lower() == "да":
        try:
            connect = sqlite3.connect('bot.db')
            q = connect.cursor()
            res = q.execute("SELECT id FROM users").fetchall()
            bot.send_message(message.chat.id, "<b>Рассылка начнеться через 3 сукунды!</b>", parse_mode="html")
            time.sleep(3)
            bot.send_message(message.chat.id, "<b>Рассылка пошла!</b>", parse_mode="html")
            k = 0
            for i in res:
                try:
                    bot.send_message(i[0], text,disable_web_page_preview=True, parse_mode="html", reply_markup=keyboard.user_spam)
                    time.sleep(0.3)
                except:
                    pass
                k += 1
            bot.send_message(message.chat.id, f"Рассылку получило {k} чел.")
            
        except:
            bot.send_message(message.chat.id, "Ошибка")
    else:
        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
        bot.send_message(message.chat.id, "Рассылка отменена!")
        
def new_adm(message):
    if message.text.isdigit():
        chat_id = message.text
        connect = sqlite3.connect("bot.db")
        q = connect.cursor()
        res = q.execute(f"SELECT * FROM admins where id = {chat_id}").fetchone()
        if res is None:
            q.execute("INSERT INTO admins(id) VALUES ('%s')"%(chat_id))
            connect.commit()
            bot.send_message(message.chat.id, "Админ успешно добавлен😌")
            bot.send_message(chat_id, "<b>⚡️Вам были выданы права админа: пропишите команду /admin ⚡️</b>", parse_mode="html")
        else:
            bot.send_message(message.chat.id, "Админ уже есть в базе 🧑‍💻")


    else:
        bot.send_message(message.chat.id, "Не корректное ID!")



while True:
    try:
        bot.polling(none_stop=True, interval=0)
    except Exception as e:
        for i in config.admins:
            bot.send_message(i, f"Ошибка {e}\n\n"\
                "Обратитесь к @jambo_squirt")