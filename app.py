from webexteamssdk import WebexTeamsAPI
from flask import Flask, request
import dialogflow_v2 as dialogflow

app = Flask(__name__)
api = WebexTeamsAPI()

def interpret(text):
    project_id = "faq-bot-fxxt"
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, "001")
    text_input = dialogflow.types.TextInput(text=text, language_code="es")
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = session_client.detect_intent(session=session, query_input=query_input)
    return response.query_result.fulfillment_messages[0].text.text[0]

@app.route('/')
def hello():
    return "Hello World!"

@app.route('/webhook', methods=['POST'])
def webhook():
    me = api.people.me()
    data = request.get_json()
    person_id = data['data']['personId']
    
    if person_id != me.id:
        message_id = data['data']['id']
        room_id = data['data']['roomId']
        message = api.messages.get(message_id)
        response = interpret(message.text)
        api.messages.create(roomId=room_id, text=response)
    return "Success"

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=8085)