from django.http import JsonResponse
from django.shortcuts import render, redirect
import apiai, json

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


def index(request):
	return render(request, './index.html')

def talk(request):

	if ('talk' in request.POST) :

		requestW = apiai.ApiAI('906077644bb24b12af0e4fe805a1418c').text_request() 
		requestW.lang = 'en'
		requestW.session_id = 'small-talk-2f79c' # ID of bot dialog
		requestW.query = request.POST['talk'] # sending answer to DF for future learning
		responseJson = json.loads(requestW.getresponse().read().decode('utf-8'))
		answer = responseJson['result']['fulfillment']['speech'] # getting answer
		if answer=='':
			answer = 'Do not understand'
	    # did bot understood?
	else:
		answer = '!error!'

	return JsonResponse({'answer':answer})