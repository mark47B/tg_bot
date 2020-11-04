import telebot
import time
import os
import nn

TOKEN = '11'

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(content_types=['voice'])
def handler(message):
    bot.send_message(message.chat.id, 'Напиши словами, не могу послушать')


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message,
    "Привет, я PuppyKittynator3000, меня создали для распознования кошек и \
собак на фото, загрузи фото питомца, и я отвечу это собака или кошка")


@bot.message_handler(commands=['calc'])
def send_calcResult(message):
    messageText = message.text
    messageText = messageText.split(' ')
    if messageText[2] in ("+", "-", "*", "/"):
        x = float(messageText[1])
        y = float(messageText[3])
        sign = messageText[2]
        if sign == '+':
            bot.reply_to(message, x + y)
        elif sign == '-':
            bot.reply_toe(message, x - y)
        elif sign == '*':
            bot.reply_to(message, x * y)
        elif sign == '/':
            if y != 0:
                bot.reply_to(message, x / y)
            else:
                bot.reply_to(message, "Деление на ноль!")


@bot.message_handler(content_types=['dice'])
def send_welcome(message):
    if(message.dice.value > 3):
        time.sleep(4)
        bot.send_message(message.chat.id, "Ты выйграл!")
    else:
        time.sleep(4)
        bot.send_message(message.chat.id, "Ты проиграл")


@bot.message_handler(commands=['help'])
def start_help_handler(message):
    bot.send_message(message.chat.id, "1. Ты можешь загрузить фото с \
кошкой или собакой, и я определю кто на фото \n 2. Ещё я умею \
решать простые примеры, на подобии 6 + 2 \n 3. Я могу поиграть \
с тобой в кости, просто отправь мне эмоджи")


@bot.message_handler(content_types=['photo'])
def photo_handler(message):
    photo = message.photo[-1]
    file_id = photo.file_id
    file_path = bot.get_file(file_id).file_path
    downloaded_file = bot.download_file(file_path)
    name = str(file_id) + ".jpg"
    directory = "images/"
    existsDir = os.listdir(directory)
    if str(message.from_user.id) not in existsDir:
        os.mkdir(directory + str(message.from_user.id))
    directory = directory + str(message.from_user.id)
    new_file = open(directory + '/' + name, mode='wb')
    new_file.write(downloaded_file)
    new_file.close()
    res = nn.predict_img_from_dir(directory + '/', name)
    bot.send_message(message.from_user.id, str(res['кошка']) + ' ' + str(res['собака']))
    if res['кошка'] > res['собака']:
        bot.send_message(message.from_user.id, "Ну, это кошка")
    else:
        bot.send_message(message.from_user.id, "Ну, это собака")


@bot.message_handler(func=lambda m: True)
def all_handler(message):
    bot.send_message(message.chat.id, "H123123123!!!")


bot.polling()
