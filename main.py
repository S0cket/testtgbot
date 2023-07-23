import telebot
import DB


def MainMenu(user: telebot.types.User):
	header = "Я бот, который может подсказать тебе состояние твоей подписки"
	markup = telebot.types.InlineKeyboardMarkup()
	info = telebot.types.InlineKeyboardButton(text="Информация", callback_data="info")
	free = telebot.types.InlineKeyboardButton(text="Бесплатно", callback_data="free")
	subscribe = telebot.types.InlineKeyboardButton(text="Спонсорам", callback_data="sponsors")
	buy = telebot.types.InlineKeyboardButton(text="Купить", callback_data="buy")
	markup.add(info)
	markup.add(free)
	markup.add(subscribe)
	markup.add(buy)
	return header, markup


def InfoMenu(user: telebot.types.User):
	if not DB.isExists(user.id):
		DB.addUser(user.id, user.username)
	stat = DB.getStat(user.id)
	header = "Информация о твоей подписке:\nУровень: {0}".format(stat)
	markup = telebot.types.InlineKeyboardMarkup()
	back = telebot.types.InlineKeyboardButton(text="Назад", callback_data="main")
	markup.add(back)
	return header, markup


def FreeMenu(user: telebot.types.User):
	header = "Бесплатная информация"
	markup = telebot.types.InlineKeyboardMarkup()
	fun = telebot.types.InlineKeyboardButton(text="Тык", callback_data="unused")
	back = telebot.types.InlineKeyboardButton(text="Назад", callback_data="main")
	markup.add(fun)
	markup.add(back)
	return header, markup


def SponsorsMenu(user: telebot.types.User):
	if not DB.isExists(user.id):
		DB.addUser(user.id, user.username)
	stat = DB.getStat(user.id)
	header = "Купите подписку"
	if stat >= 1:
		header = "Информация для подписчиков"
	markup = telebot.types.InlineKeyboardMarkup()
	fun = telebot.types.InlineKeyboardButton(text="Тык", callback_data="unused")
	back = telebot.types.InlineKeyboardButton(text="Назад", callback_data="main")
	if stat >= 1:
		markup.add(fun)
	markup.add(back)
	return header, markup


def BuyMenu(user: telebot.types.User):
	header = "Меню покупки (тест)"
	markup = telebot.types.InlineKeyboardMarkup()
	buy0 = telebot.types.InlineKeyboardButton(text="Купить уровень 0", callback_data="buy0")
	buy1 = telebot.types.InlineKeyboardButton(text="Купить уровень 1", callback_data="buy1")
	buy2 = telebot.types.InlineKeyboardButton(text="Купить уровень 2", callback_data="buy2")
	back = telebot.types.InlineKeyboardButton(text="Назад", callback_data="main")
	markup.add(buy0)
	markup.add(buy1)
	markup.add(buy2)
	markup.add(back)
	return header, markup


def BuyStatMenu(user: telebot.types.User, stat: int):
	if not DB.isExists(user.id):
		DB.addUser(user.id, user.username, stat)

	else:
		DB.setStat(user.id, stat)

	header = "Спасибо, что купили уровень {0}".format(stat)
	markup = telebot.types.InlineKeyboardMarkup()
	back = telebot.types.InlineKeyboardButton(text="Назад", callback_data="main")
	markup.add(back)
	return header, markup


menus = {
	"main": (MainMenu, []),
	"info": (InfoMenu, []),
	"free": (FreeMenu, []),
	"sponsors": (SponsorsMenu, []),
	"buy": (BuyMenu, []),
	"buy0": (BuyStatMenu, [0]),
	"buy1": (BuyStatMenu, [1]),
	"buy2": (BuyStatMenu, [2])
}

API_TOKEN = ""
bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(commands=["start"])
def start(message: telebot.types.Message):
	if not DB.isExists(message.from_user.id):
		DB.addUser(message.from_user.id, message.from_user.username)

	func, args = menus.get("main")
	menu = func(message.from_user, *args)
	bot.send_message(message.chat.id, text=menu[0], reply_markup=menu[1])


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call: telebot.types.CallbackQuery):
	value = menus.get(call.data)
	if value:
		func = value[0]
		args = value[1]
		menu = func(call.from_user, *args)
		bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text=menu[0], reply_markup=menu[1])


bot.infinity_polling()
