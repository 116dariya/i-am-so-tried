import telegram
import manga
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,ConversationHandler, CallbackQueryHandler)
bot = telegram.Bot(token = '303806740:AAFM7baM6SiJaqwbx9-SW7YT9UvlBW6kqcM')
from telegram.ext import Updater
updater = Updater(token = '303806740:AAFM7baM6SiJaqwbx9-SW7YT9UvlBW6kqcM')
dispatcher = updater.dispatcher
import json


import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))




RESTRAUNT, CATEGORY, PRODUCT, ADD_BASKET, ORDER, INFO = range(6)



callback_data = None
status = {}
basket = {}
user_basket = {}
def start(bot, update):
	custom_keyboard = [
		['Manga Sushi'], 
		['Ginger Pizza'], 
		['Pizza Hut'],
		['Ciao Pizza'], 
		['Samurai Sushi']]
	reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
	bot.sendMessage(chat_id = update.message.chat_id, text = "Выберите пиццерию или суши-бар:", reply_markup = reply_markup)
	return RESTRAUNT

def restaunt(bot, update):
	global status
	text = update.message.text
	user_id = str(update.message.from_user.id)
	if user_id in status:
		status[user_id]["restaunt"] = text
	else:
		status[user_id] = {}
		status[user_id]["restaunt"] = text

	custom_keyboard = [
		['rolls'], 
		['sushi'], 
		['pizza']]
	reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
	bot.sendMessage(chat_id = update.message.chat_id, text = "Выберите категорию меню:", reply_markup = reply_markup)
	return CATEGORY

def build_menu(buttons,
               n_cols,
               header_buttons = None,
               footer_buttons = None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu


def category(bot, update):
	print(update.message.text)
	global status
	global callback_data
	#rolls, sushi, pizza
	text = update.message.text
	user_id = str(update.message.from_user.id)
	if user_id in status:
		status[user_id]["category"] = text
	else:
		status[user_id] = {}
		status[user_id]["category"] = text
	file = open("manga.json", "r", encoding='utf-8')
	menu = json.loads(file.read())
	print(menu)
	products = menu[text]
	print(products)
	for item in products:
		photo_url = "http://manga-sushi.kz" + item["img_url"]
		title = item["name"]
		description = item["description"]
		price = item['price']
		print(title)
		print(photo_url)
		print(description)
		print(price)
		data_id = item['data_id']

		button_list = [
		    InlineKeyboardButton("Добавить в корзину", callback_data='Товар добавлен в корзину'),
		    InlineKeyboardButton("Удалить из корзины", callback_data='Товар удален с корзины'),
		    InlineKeyboardButton("Показать корзину", callback_data= "Ваша корзина состоит из:"),
		    InlineKeyboardButton("Оформить заказ", callback_data= "Оформите форму заказа"),

		    #InlineKeyboardButton("add", callback_data='add %s' % item['data-id']),
		    #InlineKeyboardButton("remove", callback_data='remove %s' % item['data-id']),
		]
		reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=3))
		bot.sendPhoto(chat_id = update.message.chat_id, photo = photo_url, caption = title)
		bot.sendMessage(chat_id = update.message.chat_id, text = description)
		bot.sendMessage(chat_id = update.message.chat_id, text = price, reply_markup = reply_markup)

		if callback_data == 'Товар добавлен в корзину':
			basket.update(({data_id: 1})) #n
			user_basket.update(({title: 1}))
			bot.sendMessage(chat_id = update.message.chat_id, text = "test")


		if callback_data == 'Товар удален с корзины':
			del basket[data_id]
			del user_basket[title]

			#if basket.has_key(data_id) == True:
				#basket.update(({data_id: 0})) #n-1

		if callback_data == 'Ваша корзина состоит из:':

			print(basket)	
			print(user_basket)
			for i in range(0, len(user_basket)):
				bot.sendMessage(chat_id = update.message.chat_id, text = basket[i])

		if callback_data == 'Оформить заказ':
			n = 1
			from manga import make_order
			if n == 1:
				bot.sendMessage(chat_id = update.message.chat_id, text = "Ваше полное имя")
				order['name'] = bot.getUpdates()[-1].update_id
				n = n + 1
			if n == 2:
				bot.sendMessage(chat_id = update.message.chat_id, text = "Ваш точный адрес")
				order['address'] = bot.getUpdates()[-1].update_id
				n = n + 1
			if n == 3:
				bot.sendMessage(chat_id = update.message.chat_id, text = "Ваш номер сотового телефона")
				order['phone'] = bot.getUpdates()[-1].update_id
				n = n + 1
			if n == 4:
				bot.sendMessage(chat_id = update.message.chat_id, text = "Ваш email")
				order['email'] = bot.getUpdates()[-1].update_id#.compile("^\w+\.?\w+@(gmail\.com|mail\.ru)$")
				n = n + 1
			if n == 5:
				result = make_order(order)
				print(result)



	return ConversationHandler.END
	

def button(bot, update):
    query = update.callback_query
    print(query)

    bot.editMessageText(text="Selected option: %s" % query.data,
                        chat_id=query.message.chat_id,
                        message_id=query.message.message_id)

def cancel(bot, update):
    user = update.message.from_user
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            RESTRAUNT: [MessageHandler(Filters.text, restaunt)],

            CATEGORY: [RegexHandler('^(rolls|sushi|pizza)$', category)],

        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

dispatcher.add_handler(conv_handler)
updater.dispatcher.add_handler(CallbackQueryHandler(button))
dispatcher.add_error_handler(error)

updater.start_polling()

