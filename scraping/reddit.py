import json
import urllib3
import pandas as pd
from datetime import datetime
http = urllib3.PoolManager()

import bbc

def reddit(start_time, end_time):
    user_agent = ""
    # specify the url name and parameters
    pushshift_url = (
        'https://api.pushshift.io/reddit/search/submission/?subreddit=news&sort_type=score&'
        'sort=desc&before={start}d&after={end}d&size=500&filter=score,title,author,created_utc,url'
        ).format(start=start_time, end=end_time)

    # query pushshift API and retrieve the JSON reddit posts in r/news
    response = http.request('GET', pushshift_url)
    reddit_posts = json.loads(response.data.decode('utf-8'))['data']

    # extract just the title from each post in the list of reddit posts

    #print(datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))

    # test call of the bbc function
    # at the moment this seems to be either returning None or
    # resulting in a runtime error
    # bbc.bbc(headlines[5])
    return reddit_posts
