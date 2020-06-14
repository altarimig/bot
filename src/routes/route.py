import os
from flask import request, json
from src.routes.bot.bot import Bot
from dotenv import load_dotenv
from pathlib import Path

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


PAGE_ACCESS_TOKEN = os.getenv('PAGE_ACCESS_TOKEN')
webhooks_token = os.getenv('WEBHOOKS_VERIFY_TOKEN')  # os.getenv('secret')

primero = ['hola', 'buenas', 'lindo dia']
segundo = ['bien y tu?', 'bien', 'bien y usted?', 'bien y tu']
tercero = ['bueno gracias', 'gracias', 'muy bien']

def get_post(app):
    @app.route('/', methods=['GET', 'POST'])
    def webhook():
        if request.method == 'GET':
            token = request.args.get('hub.verify_token')
            challenge = request.args.get('hub.challenge')
            if token == webhooks_token: # if token == secret:
                return str(challenge) 
            return '400'
        else:
            data = json.loads(request.data)
            messaging_events = data['entry'][0]['messaging']
            bot = Bot(PAGE_ACCESS_TOKEN)
            for message in messaging_events:
                user_id = message['sender']['id']
                text_input = message['message'].get('text')
                response_text = 'esta bien'
                if text_input in primero:
                    response_text = 'hola ¿que tal?'
                if text_input in segundo:
                    response_text = 'tambien, mucha suerte :)'
                if text_input in tercero:
                    response_text = 'Gracias, chau'
                print('Message from user ID {} - {}'.format(user_id, text_input))
                bot.send_text_message(user_id, response_text)
            return '200'