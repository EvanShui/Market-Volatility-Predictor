import re
import time
# inserting path to look for keys
import sys
import nltk
# a high-level library built on top of NLTK which utilizes the data from movie reviews to categorize
# whether text i considered 'positive' or 'negative'
from textblob import TextBlob
from nltk.corpus import stopwords
from string import punctuation
from pprint import pprint
from datetime import datetime
from datetime import timedelta
import subprocess
sys.path.insert(0, '../../data_301_project/')
from keys.credentials import *
print('successfully imported api keys file')
from GetOldTweets_python import got3 as got
print('successfully imported GetOldTweets')



def clean_tweet(tweet):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

def sentiment_analysis_helper(tweet):
    analysis = TextBlob(clean_tweet(tweet))
    if analysis.sentiment.polarity > 0:
        return 1
    elif analysis.sentiment.polarity == 0:
        return 0
    else:
        return -1 

def tokenize_title(test_title):
    stop_words = set(stopwords.words('english'))
    ret_lst = []
    lst = []
    line = (re.sub(r'[^\w\s]', '', test_title))
    print("original title: ", test_title)
    print(nltk.pos_tag(nltk.word_tokenize(line)))
    for word in nltk.pos_tag(nltk.word_tokenize(line)):
        print(word)
        if word[0] not in stop_words and word[0] not in punctuation and word[1] in ['JJ', 'NN', 'NNP', 'NNS']:
            lst.append(word[0])
    return(' OR '.join(lst))


"""
def scrape_tweets(query, date):
    tweets = []
    str_date = date.strftime('%Y-%m-%d')
    print(str_date)
    str_week_after = (date + timedelta(days=365)).strftime('%Y-%m-%d')
    print(str_week_after)
    try:
        auth = tweepy.OAuthHandler(app_key, app_secret)
        auth.set_access_token(access_token, access_secret)
        print('setting authentication')
        api = tweepy.API(auth)
        print('confirmed authentication')
        for tweet in api.search(q = query, count = 20, lang='en',
                since=str_date,
                until=str_week_after):
            # Tweet status provides entity recognition. (just presence though).
            parsed_tweet = {}
            parsed_tweet['text'] = tweet._json['text']
            parsed_tweet['sentiment'] = sentiment_analysis_helper(tweet._json['text'])
            tweets.append(parsed_tweet)
        return tweets
    except:
        print("Error with authentication")
        return -1
"""

def scrape_old_tweets(query, date):
    tweets = []
    tweetCriteria = got.manager.TweetCriteria()

    str_date = date.strftime('%Y-%m-%d')
    str_week_after = (date + timedelta(days=60)).strftime('%Y-%m-%d')
    tweetCriteria.maxTweets = 20
    tweetCriteria.since = str_date
    tweetCriteria.until = str_week_after
    tweetCriteria.querySearch = query
    tweetCriteria.topTweets = True
    print("Searching...\n")
    for tweet in got.manager.TweetManager.getTweets(tweetCriteria):
        parsed_tweet = {}
        parsed_tweet['text'] = tweet.text
        parsed_tweet['sentiment'] = sentiment_analysis_helper(tweet.text)
        print(tweet.text)
        print(tweet.date.strftime("%Y-%m-%d"))
        tweets.append(parsed_tweet)
    return tweets

def sentiment_analysis(id_num, title, date):
    """Input: title (string): headline of the event
    date (string): formatted in 'YYYY-MM-DD'
    """
    tokenized_title = tokenize_title(title)
    date = datetime.utcfromtimestamp(date)
    str_date = date.strftime('%Y-%m-%d')
    print("getting sentiment analysis on: ", tokenized_title)
    tweets = scrape_old_tweets(tokenized_title, date)
    if tweets == -1:
        return {'error': 1,
                'reason': 'authentication issues'}
    if len(tweets) == 0:
        return {'error': 1,
                'reason': 'tweets is length 0'}
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 1]
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 0]
    netweets = [tweet for tweet in tweets if tweet['sentiment'] == -1]
    percent_pos = len(ptweets) * 100 / len(tweets)
    percent_neg = len(ntweets) * 100 / len(tweets)
    percent_neutral = len(netweets) * 100 / len(tweets)
    print("Percent of positive tweets: ", percent_pos)
    print("Percent of negative tweets: ", percent_neg)
    print("Percent of neutral tweets: ", percent_neutral)
    return {
            'id_num': id_num,
            'title': title,
            'date': str_date,
            'pos':percent_pos,
            'neg':percent_neg,
            'neu':percent_neutral,
            'error': 0
            }

if __name__ == '__main__':
    test_titles = ["San Francisco rallies for 'Batkid' Miles Scott, leukaemia survivor",
            "California wildfires: Number of missing leaps to 631",
            "Trump renews threat to close Mexico border over migrants"]
    dates = ['', '', '2018-11-15']
    sentiment_analysis(test_titles[2], dates[2])
