from flask import request, json
from src.routes.bot.bot import Bot

PAGE_ACCESS_TOKEN = 'EAAJ4csJ8PXEBALWyZCrobcQ8MzdFFeUTiwaZC39US6krcH1ovnsWWQ7g2ZABFLGjtaZCXzQZAgHy3czzpOYgZAMfr8eE3EXNQsaq1xqPWxuMs0EqDM2R28yzQvFCq6vMMlWFhITbF1oMHdMVZCkBBAdlwZCw5F6meEroU9pSCgvnGfAinMyXiDt4'

GREETINGS = ['hola', 'buenas', 'lindo dia']

def get_post(app):
    @app.route('/', methods=['GET', 'POST'])
    def webhook():
        if request.method == 'GET':
            token = request.args.get('hub.verify_token')
            challenge = request.args.get('hub.challenge')
            if token == 'secret':
                return str(challenge) 
            return '400'
        else:
            data = json.loads(request.data)
            messaging_events = data['entry'][0]['messaging']
            bot = Bot(PAGE_ACCESS_TOKEN)
            for message in messaging_events:
                user_id = message['sender']['id']
                text_input = message['message'].get('text')
                response_text = 'buenas'
                if text_input in GREETINGS:
                    response_text = 'hola que tal'
                print('Message from user ID {} - {}'.format(user_id, text_input))
                bot.send_text_message(user_id, response_text)
            return '200'