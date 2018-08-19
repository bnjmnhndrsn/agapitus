import os
import tweepy
import requests
import io

PETRONAX_API = 'http://petronax.herokuapp.com/api/wikipedia'

def get_image():
    r = requests.get(PETRONAX_API, params={'date': '1950-01-01'})
    return r.json()[0]
    
def tweet_image(status, filename, file_url):
    C_KEY = os.environ.get('TWITTER_CONSUMER_KEY')
    C_SECRET = os.environ.get('TWITTER_CONSUMER_SECRET')
    A_TOKEN = os.environ.get('TWITTER_ACCESS_TOKEN')
    A_TOKEN_SECRET = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')

    r = requests.get(file_url, allow_redirects=True)
    f = io.BytesIO(r.content)

    auth = tweepy.OAuthHandler(C_KEY, C_SECRET)  
    auth.set_access_token(A_TOKEN, A_TOKEN_SECRET)  
    api = tweepy.API(auth)
    api.update_with_media(filename='f.jpg', status=status, file=f)

def tweet():
    image = get_image()
    status = image['title']
    filename = image['title'].replace('File:', '')
    file_url = image['scaled_url']
    tweet_image(status, filename, file_url)
    
tweet()