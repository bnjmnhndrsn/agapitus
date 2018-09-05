import os
import tweepy
import requests
import io
import random
from datetime import datetime, date, timedelta
from db import Session, Post

PETRONAX_API = 'http://petronax.herokuapp.com/api/wikipedia'

#TODO: Deal with leap years
def generate_date():
    today = date.today()
    year = random.randint(1875, 1990)
    return today.replace(year=year)

def create_post(session, date):
    image_data = find_unused_image_data(session, date)
    if image_data:
        return Post(
            date=date,
            page_id=image_data['page_id'],
            image_url=image_data['scaled_url'],
            page_url=image_data['description_url'],
            title=image_data['title'].replace('File:', ''),
            created_at=datetime.now(),
            description=image_data['description']
        )

def find_unused_image_data(session, date):
    twenty_four_hours_ago = datetime.now() - timedelta(hours=24)
    if session.query(Post).filter(Post.date == date).filter(Post.created_at > twenty_four_hours_ago).count():
        return None
        
    r = requests.get(PETRONAX_API, params={'date': str(date), 'limit': 10})
    r.raise_for_status()
    for item in r.json():
        if not session.query(Post).filter(Post.page_id == item['page_id']).one_or_none():
            return item
    
    return None
    
def tweet_post(post):
    datestring = '{} years ago today'.format(date.today().year - post.date.year)
    trimmed_description = post.description.rstrip()
    status_beginning = '[{}] {}'.format(datestring, trimmed_description)
    if (len(status_beginning) + len(post.page_url)) > 275:
        available_length = 275 - len(post.page_url)
        status_beginning = status_beginning[:available_length].rstrip() + '...'
    status = '{}\n{}'.format(status_beginning, post.page_url)
    filename = post.title
    file_url = post.image_url
    
    C_KEY = os.environ.get('TWITTER_CONSUMER_KEY')
    C_SECRET = os.environ.get('TWITTER_CONSUMER_SECRET')
    A_TOKEN = os.environ.get('TWITTER_ACCESS_TOKEN')
    A_TOKEN_SECRET = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')

    file_request = requests.get(file_url, allow_redirects=True)
    image_file = io.BytesIO(file_request.content)

    auth = tweepy.OAuthHandler(C_KEY, C_SECRET)  
    auth.set_access_token(A_TOKEN, A_TOKEN_SECRET)  
    api = tweepy.API(auth)
    api.update_with_media(filename=filename, status=status, file=image_file)

def tweet():
    session = Session()
    post = None
    
    try:
        #TODO: Make this exit if all possible images are posted
        while post is None:
            date = generate_date()
            post = create_post(session, date)
    except requests.exceptions.HTTPError:
        print('Request to Petronax failed.')
        return 
    
    try:
        tweet_post(post)
        session.add(post)
        session.commit()
    except requests.exceptions.HTTPError:
        print('Posting to Twitter failed')
        return
    
    print('Tweet successful')
    
