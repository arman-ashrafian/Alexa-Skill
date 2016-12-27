from flask import Flask
from flask_ask import Ask, statement, question, session
import json
import requests
import time
import unidecode
import os



app = Flask(__name__)
ask = Ask(app, "/")

def get_headlines():
    user_pass_dict = {'user': 'ash63',
                      'password': 'colts31fan',
                      'api_type': 'json'}
    sess = requests.Session()
    sess.headers.update({'User-Agent': 'testing'})
    sess.post('https://www.reddit.com/api/login', data = user_pass_dict)

    time.sleep(1)

    url = 'https://reddit.com/r/worldnews/.json?limit=10'
    html = sess.get(url)
    data = json.loads(html.content.decode('utf-8'))

    titles = []
    for listing in data['data']['children']:
        titles.append(unidecode.unidecode(listing['data']['title']))

    titles = '...'.join([i for i in titles])
    return titles


titles = get_headlines()
print(titles)

@app.route("/")
def index():
    return "index"

@ask.launch
def start_skill():
    welcome_message = 'Hi nigger, you like butt stuff?'
    return question(welcome_message)

@ask.intent("YesIntent")
def share_headlines():
    headlines = get_headlines()
    headline_msg = 'The current world news headlines are {}'.format(headlines)
    return statement(headline_msg)

@ask.intent("NoIntent")
def no_intent():
    bye_text = 'Ok bye'
    return statement(bye_text)

if __name__ == "__main__":

    # declaring host and port so the servers runs in Cloud9
    app.run(debug=True)
