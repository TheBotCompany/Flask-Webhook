#Webhook Server para FB Messenger 
import random
from flask import Flask, request
from pymessenger.bot import Bot

app = Flask(__name__)
#Los TOKEN se obtiene después del registro en FB Messenger For Developers
ACCESS_TOKEN = 'EAALantIFqAMBAB9h1XI2Y11rdCRWfc7fL4ftlFPs0LXkDZAkhdm2J6tJuPeEicvboue1P2j9ASVHcOQIKqqvEckO9WXg81evpTbZAjKVZBV2Tfy6U7nxuXkZBEpYO3CrbE0K10Xj9k77MFYMLmLXHlvsXGbiOiamBCmeeLqKmwZDZD'
#Aquí pon el string que ti quieras
VERIFY_TOKEN = 'GERMANY'
bot = Bot(ACCESS_TOKEN)

#Aquí es donde se reciben los mensajes enviados por FB al server
@app.route('/', methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        
        #request a verify_token de confirmación de FB  
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    
    #Si GET truena, se invoca el método POST
    else:
        #Obtén cualquier cosa enviada por el usuario
        output = request.get_json()
        for event in ouput['entry']:
            messaging = event['messaging']
            for message in messaging:
                if message.get('message'):
                    #FBM ID para el usuario. para saber a donde se envía
                    recipient_id = message['sender']['id']
                    if message['message'].get('text'):
                        response_sent_text = get_message()
                        send_message(recipient_id, response_sent_text)
                    
                    #Esto es por si el usuario envía algo que no sea texto
                    if message['message'].get('attachments'):
                        response_sent_nontext = get_message()
                        send_message(recipient_id, response_sent_nontext)

    return "Message Processed"

#FB necesita saber atráves del Access_Token si tu Bot es quien envía mensajes
def verify_fb_token(token_sent):
    #aquí se verifica si el token hace match con el que envías y el de FB
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub_challenge")
    return 'Invalid Verification Token'

#Se escoge un mensaje para envíar, no se envía aún
def get_message():
    sample_responses = ["Coding At Night!","Listening to DeadMau5",
    "Enjoying Coding In Flask", "Learning to Code"]
    #Retorna algo al usuario
    return random.choice(sample_responses)

#PyMessenger envía el mensaje al usuario
def send_message(recipient_id, response):
    bot.send_text_message(recipient_id, response)
    return "Success"

if __name__ == '__main__':
    app.run()
