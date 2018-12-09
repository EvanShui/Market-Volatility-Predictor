import re
import time
# inserting path to look for keys
import nltk
# a high-level library built on top of NLTK which utilizes the data from movie reviews to categorize
# whether text i considered 'positive' or 'negative'
from textblob import TextBlob
from nltk.corpus import stopwords
from string import punctuation
from pprint import pprint
from datetime import datetime
from datetime import timedelta

def clean_string(tweet):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

def sentiment_analysis_helper(text):
    analysis = TextBlob(clean_string(text))
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
    # gets rid of stop words, punctuation, and only keeps noun-based words with
    # part of speech tagging
    for word in nltk.pos_tag(nltk.word_tokenize(line)):
        if word[0] not in stop_words and word[0] not in punctuation and word[1] in ['JJ', 'NN', 'NNP', 'NNS']:
            lst.append(word[0])
    return(' OR '.join(lst))

def sentiment_analysis(id_num, title, date):
    """
    Determine the positivity of the title of the news article

    Input: 
    id_num (int): ID num
    title (string): headline of the event
    date (string): formatted in 'YYYY-MM-DD'
    
    Output:
    JSON string
    {
    'id_num': ID of the entry,
    'title': Title of the entry,
    'sa': Sentiment analysis performed on the title. 1 if positive, 0 if
    neutral, -1 if negative
    }

    """
    tokenized_title = tokenize_title(title)
    date = datetime.utcfromtimestamp(date)
    print("getting sentiment analysis on: ", tokenized_title)
    sa = sentiment_analysis_helper(tokenized_title)
    return {
            'id_num': id_num,
            'title': title,
            'sa': sa,
            }
