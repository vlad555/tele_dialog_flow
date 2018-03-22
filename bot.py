import configparser
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import apiai, json


# read config for Telegram (api_key, ip andp por for bot server)
config = configparser.ConfigParser()

if not config.read('config'):
    print("Config file not exist.")
    exit(-1)

# Interacting with dialogflow(DF)
def textMessage(bot, update):
    request = apiai.ApiAI(config.get('App data', 'dialogflow_token')).text_request() # Token Dialogflow
    request.lang = 'en' # Lanuage
    request.session_id = 'small-talk-2f79c' # ID of bot dialog
    request.query = update.message.text # sending answer to DF for future learning
    responseJson = json.loads(request.getresponse().read().decode('utf-8'))
    response = responseJson['result']['fulfillment']['speech'] # getting answer
    # did bot understood?
    if response:
        bot.send_message(chat_id=update.message.chat_id, text=response)
    else:
        bot.send_message(chat_id=update.message.chat_id, text='It is not clear for me')

# Commands 
def startCommand(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='Hello! How are you?')

def textMessage_echo(bot, update):
    response = 'You wrote: ' + update.message.text
    bot.send_message(chat_id=update.message.chat_id, text=response)

updater = Updater(token=config.get('App data', 'api_token')) # get token for bot
dispatcher = updater.dispatcher

# handlers
start_command_handler = CommandHandler('start', startCommand)
text_message_handler = MessageHandler(Filters.text, textMessage)
#text_message_handler = MessageHandler(Filters.text, textMessage_echo) #echo function for testing

# adding handlers to dispatch
dispatcher.add_handler(start_command_handler)
dispatcher.add_handler(text_message_handler)

# search for updates
updater.start_polling(clean=True)
# stop
updater.idle()