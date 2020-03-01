import time
import telebot
from telebot import types
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException

chromedriver = 'chromedriver'
options = webdriver.ChromeOptions()
options.add_argument('headless')  # для открытия headless-браузера
browser = webdriver.Chrome(executable_path=chromedriver, chrome_options=options)
bot = telebot.TeleBot('1104090737:AAEmkj_arPPd9gdgHx9NeEgNQm0x3j7qaX4')
keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard1.row('Информация о поступлении')
keyboard1.row('Часто задаваемые вопросы')
keyboard1.row('Задать вопрос')

flagpred = False
flag2 = False

def funcb(flag1):
    global flagpred
    flagpred = flag1


def funcb2(flag3):
    global flag2
    flag2 = flag3


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, '+message.chat.first_name, reply_markup=keyboard1)


@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'информация о поступлении':
        keyboard = types.InlineKeyboardMarkup()
        key_yes = types.InlineKeyboardButton(text='Расписание подачи документов', callback_data='yes')
        keyboard.add(key_yes)
        key_no = types.InlineKeyboardButton(text="Какие экзамены нужны:", callback_data='no')
        keyboard.add(key_no)
        bot.send_message(message.chat.id, 'Выберите, что хотите получить:', reply_markup=keyboard)
    elif message.text.lower() == 'часто задаваемые вопросы':
        browser.get('https://pk.mipt.ru/bachelor/question-answer/')
        requiredHtml = browser.page_source
        soup = BeautifulSoup(requiredHtml, 'html5lib')
        h = soup.findChildren('h2')
        questions = []
        for my_h in h:
            questions.append(my_h.text+'\n')
        bot.send_message(message.chat.id, 'Вот список самых часто задаваемых вопросов:')
        for item in questions:
            bot.send_message(message.chat.id, item)

    elif message.text.lower() == 'задать вопрос':
        bot.send_message(message.chat.id, 'Введите вопрос:')
        funcb2(True)
    elif flagpred:
        browser.get('https://tabiturient.ru/vuzu/mipt/proxodnoi/')
        inp = browser.find_element_by_name('search')
        inp.send_keys(message.text.lower())
        srt = ""
        #bs = browser.find_elements_by_class_name('cirfloat')
        #for item in bs:
            #srt.join(item.text+'\n')
        bot.send_message(message.chat.id, 'Для поступленния на данную специальность, вам надо сдать эти предметы:')
        bot.send_message(message.chat.id, srt)
        funcb(False)
    elif flag2:
        Req = message.text.lower()
        funcb2(False)
        bot.send_message(message.chat.id, 'Я принял ваш вопрос, подождите, он находится в обработке...')
    else:
        bot.send_message(message.chat.id, 'Введите еще раз, я вас не понял.')


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "yes":
        bot.send_message(call.message.chat.id, 'Расписание:')
        bot.send_message(call.message.chat.id, 'Приемная комиссия работает с 9.00 до 18.00 с перерывом на обед с 12.00 до 13.00.\nВыходные дни: суббота и воскресенье.')
        bot.send_message(call.message.chat.id, 'Во время летней приемной кампании, в соответствии с графиком работы, который публикуется по ссылке(https://pk.mipt.ru/bachelor/2020_schedule/index.php) в срок до 01 июня.')
        bot.send_message(call.message.chat.id, 'Вступительные испытания начинают проводиться с 01 июня текущего года и заканчивают проводиться не менее, чем за три дня до начала учебного года, в сроки, установленные графиком работы приёмной комиссии.')
        bot.send_message(call.message.chat.id, '27 июля формируются списки поступающих на бюджетные места.')
    elif call.data == "no":
        bot.send_message(call.message.chat.id, 'Введите специальность:')
        funcb(True)


bot.polling()
'''
# Настройки
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import apiai, json
updater = Updater(token='ВАШ API ТОКЕН') # Токен API к Telegram
dispatcher = updater.dispatcher
# Обработка команд
def startCommand(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='Привет, давай пообщаемся?')
def textMessage(bot, update):
    request = apiai.ApiAI('ВАШ API ТОКЕН').text_request() # Токен API к Dialogflow
    request.lang = 'ru' # На каком языке будет послан запрос
    request.session_id = 'BatlabAIBot' # ID Сессии диалога (нужно, чтобы потом учить бота)
    request.query = update.message.text # Посылаем запрос к ИИ с сообщением от юзера
    responseJson = json.loads(request.getresponse().read().decode('utf-8'))
    response = responseJson['result']['fulfillment']['speech'] # Разбираем JSON и вытаскиваем ответ
    # Если есть ответ от бота - присылаем юзеру, если нет - бот его не понял
    if response:
        bot.send_message(chat_id=update.message.chat_id, text=response)
    else:
        bot.send_message(chat_id=update.message.chat_id, text='Я Вас не совсем понял!')
# Хендлеры
start_command_handler = CommandHandler('start', startCommand)
text_message_handler = MessageHandler(Filters.text, textMessage)
# Добавляем хендлеры в диспетчер
dispatcher.add_handler(start_command_handler)
dispatcher.add_handler(text_message_handler)
# Начинаем поиск обновлений
updater.start_polling(clean=True)
# Останавливаем бота, если были нажаты Ctrl + C
updater.idle()
'''