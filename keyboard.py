import telebot
from telebot import types

menu = types.ReplyKeyboardMarkup(True)
menu.add("☘️Довереные магазины☘️")
menu.add("🍊Эл.Услуги🍊","Чаты🤼")
menu.add("💫PORTAL DNR💫")
menu.add("🧑‍💻Админ🧑‍💻")

adm = types.ReplyKeyboardMarkup(True)
adm.add("Запустить рассылку🔈", "Добавить админа🧑‍🔧")
adm.add("Меню🎆")

trust_shop = types.InlineKeyboardMarkup()
trust1 = types.InlineKeyboardButton("1", callback_data="1")
trust2 = types.InlineKeyboardButton("2", url="https://t.me/CitrusShopM")
trust3 = types.InlineKeyboardButton("3", callback_data="3")
trust4 = types.InlineKeyboardButton("4", url="https://t.me/CitrusShopM")
trust5 = types.InlineKeyboardButton("5", callback_data="5")
trust6 = types.InlineKeyboardButton("6",url="https://t.me/CitrusShopM")
trust7 = types.InlineKeyboardButton("7", callback_data="7")
trust8 = types.InlineKeyboardButton("8", url="https://t.me/CitrusShopM")
trust9 = types.InlineKeyboardButton("9", url="https://t.me/CitrusShopM")
delete = types.InlineKeyboardButton("Закрыть", callback_data="delete")
trust_shop.row(trust1,trust2)
trust_shop.row(trust3,trust4)
trust_shop.row(trust5,trust6)
trust_shop.row(trust7,trust8,trust9)
trust_shop.row(delete)


spam = types.InlineKeyboardMarkup()
spam_text = types.InlineKeyboardButton("💬Спам текстом💬", callback_data="text")
spam_text_but = types.InlineKeyboardButton("💬Спам текстом + кнопка💬", callback_data="text_but")
spam_pic = types.InlineKeyboardButton("🖼Спам с картинкой🖼", callback_data="pics")
spam_pic_but = types.InlineKeyboardButton("🖼Спам с картинкой + кнопка🖼", callback_data="pics_but")
cancel_spam = types.InlineKeyboardButton("🙅Отмена рассылки🙅", callback_data="stop_spam")
spam.row(spam_text, spam_pic)
spam.row(spam_text_but,spam_pic_but)
spam.row(cancel_spam)

user_spam = types.InlineKeyboardMarkup()
user_spam.row(delete)
