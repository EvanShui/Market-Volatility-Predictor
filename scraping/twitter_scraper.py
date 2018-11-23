# scraping tweets from Twitter
import tweepy
import re
import time
# inserting path to look for keys
import sys
import nltk
# a high-level library built on top of NLTK which utilizes the data from movie reviews to categorize
# whether text is considered 'positive' or 'negative'
from textblob import TextBlob
from nltk.corpus import stopwords
from string import punctuation
from pprint import pprint

sys.path.insert(0, '../../data_301_project/')
from keys.credentials import *

print('successfully imported api keys file')

def clean_tweet(tweet):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

def sentiment_analysis(tweet):
    analysis = TextBlob(clean_tweet(tweet))
    if analysis.sentiment.polarity > 0:
        return 1
    elif analysis.sentiment.polarity == 0:
        return 0
    else:
        return -1 

def scrape_tweets(title, date):
    tweets = []
    try:
        auth = tweepy.OAuthHandler(app_key, app_secret)
        auth.set_access_token(access_token, access_secret)
        print('setting authentication')
        api = tweepy.API(auth)
        print('confirmed authentication')
        for tweet in api.search(q = title, count = 100):
            # print("\n----------------\n")
            # Tweet status provides entity recognition. (just presence though).
            parsed_tweet = {}
            parsed_tweet['text'] = tweet._json['text']
            parsed_tweet['sentiment'] = sentiment_analysis(tweet._json['text'])
            tweets.append(parsed_tweet)
        print(tweets)
        return tweets
    except:
        print("Error with authentication")
        return 

def tokenize_titles(test_titles):
    stop_words = set(stopwords.words('english'))

    ret_lst = []
    for i in test_titles:
        lst = []
        line = (re.sub(r'[^\w\s]', '', i))
        for word in (nltk.word_tokenize(line)):
            if word not in stop_words and word not in punctuation:
                lst.append(word)
        ret_lst.append(' OR '.join(lst))
    return(ret_lst)

if __name__ == '__main__':
    test_titles = ["San Francisco rallies for 'Batkid' Miles Scott, leukaemia survivor",
            "California wildfires: Number of missing leaps to 631",
            "Trump renews threat to close Mexico border over migrants"]
    dates = ['', '', '2018-11-15']
    post_titles = tokenize_titles(test_titles)
    print("getting tweets about: {}".format(post_titles[2]))
    time.sleep(1)
    tweets = scrape_tweets(post_titles[2], dates[2])
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 1]
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 0]
    netweets = [tweet for tweet in tweets if tweet['sentiment'] == -1]
    print("Percent of positive tweets: ", len(ptweets) * 100 / len(tweets))
    print("Percent of negative tweets: ", len(ntweets) * 100 / len(tweets))
    print("Percent of neutral tweets: ", len(netweets) * 100 / len(tweets))
