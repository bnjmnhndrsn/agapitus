import os
import tweepy
import requests
import io
import random
from datetime import datetime, date, timedelta
from db import Session, Post

PETRONAX_API = 'http://petronax.herokuapp.com/api/wikipedia'

def generate_date():
    today = date.today()
    year = random.randint(1875, 1990)
    return today.replace(year=year)

def find_unused_image(session, date):
    twenty_four_hours_ago = datetime.now() - timedelta(hours=24)
    if session.query(Post).filter(Post.date == date).filter(Post.created_at > twenty_four_hours_ago).count():
        return None
        
    r = requests.get(PETRONAX_API, params={'date': str(date), 'limit': 10})
    for item in r.json():
        if not session.query(Post).filter(Post.page_id == item['page_id']).one_or_none():
            return item
    
    return None
    
def tweet_image(status, filename, file_url):
    print(file_url)
    return
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
    session = Session()
    image = None

    while image is None:
        date = generate_date()
        image = find_unused_image(session, date)
    
    print(image)
    status = image['title']
    filename = image['title'].replace('File:', '')
    file_url = image['scaled_url']
    tweet_image(status, filename, file_url)
    
# p = Post(image_url='test.com')
# session.add(p)
# session.commit()
# print(p.id)    

tweet()