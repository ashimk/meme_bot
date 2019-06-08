import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "songsbot-gymnux-9f2779ee1206.json"
import requests
import json
import dialogflow_v2 as dialogflow
dialogflow_session_client = dialogflow.SessionsClient()
PROJECT_ID = "songsbot-gymnux"
from gnewsclient import gnewsclient
client = gnewsclient.NewsClient(max_results=3)

from pymongo import MongoClient
mongo_client = MongoClient("mongodb+srv://ashimk:cseismylife13@cluster0-mu5le.mongodb.net/test?retryWrites=true&w=majority")
db = mongo_client.get_database('meme_bot')

records = db.queries

def get_news(parameters):
	client.topic = parameters.get('news_type')
	client.language = parameters.get('language')
	# client.location = parameters.get('geo-country')
	return client.get_news()


def get_meme(query):
    records.insert_one({'User Query':query})
    url1 = "https://api.imgflip.com/get_memes"
    r = requests.get(url1)
    x = r.json()
    y = x['data']['memes']
    print("\n\n",y)
    return y


def detect_intent_from_text(text, session_id, language_code='en'):
    session = dialogflow_session_client.session_path(PROJECT_ID, session_id)
    text_input = dialogflow.types.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = dialogflow_session_client.detect_intent(session=session, query_input=query_input)
    return response.query_result


def fetch_reply(msg, session_id):
    response = detect_intent_from_text(msg, session_id)
    if response.intent.display_name == 'get_meme':
        meme = get_meme(msg)
        meme_str = 'Here is your meme'
        for row in meme:
            y=row['name']
            if y==msg:
                imageURL = row['url']
                #meme_str += "\n\n{}\n\n".format(row['name'])
                finlUrl = "Here is your Meme Template:\n\n" + imageURL
        return finlUrl
    elif response.intent.display_name == 'get_news':
        news = get_news(dict(response.parameters))
        news_str = 'Here is your news'
        for row in news:
            news_str += "\n\n{}\n\n{}\n\n".format(row['title'],row['link'])
        return news_str
    else:
        return response.fulfillment_text
