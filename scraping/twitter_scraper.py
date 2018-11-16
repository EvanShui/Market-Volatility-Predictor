# scraping tweets from Twitter
import tweepy
# inserting path to look for keys
import sys
sys.path.insert(0, '../../data_301_project/')
from keys.credentials import *
from pprint import pprint

print('successfully imported api keys file')

def scrape_tweets():
    auth = tweepy.OAuthHandler(app_key, app_secret)
    auth.set_access_token(access_token, access_secret)
    print('confirmed authentication')
    api = tweepy.API(auth)
    print('setting authentication')
    for tweet in tweepy.Cursor(api.search, q='#brazil', count=50, lang='en',since='2017-04-03').items():
        print("\n----------------\n")
        print(type(tweet))
        # Tweet status provides entity recognition. (just presence though).
        print(tweet._json['text'])
        # pprint(tweet)

if __name__ == '__main__':
    scrape_tweets()
