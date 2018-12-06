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
        f'https://api.pushshift.io/reddit/search/submission/?subreddit=news&sort_type=score&'
        f'sort=desc&before=300d&after=400d&size=500&filter=score,title,author,created_utc'
        )

    # query pushshift API and retrieve the JSON reddit posts in r/news
    response = http.request('GET', pushshift_url)
    reddit_posts = json.loads(response.data.decode('utf-8'))['data']

    # extract just the title from each post in the list of reddit posts

    df = pd.DataFrame(reddit_posts)
    df['human_date'] = df['created_utc'].apply(lambda x:
            datetime.utcfromtimestamp(x).strftime('%Y-%m-%d %H:%M:%S'))
    print(df.human_date)
    #print(datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))

    # test call of the bbc function
    # at the moment this seems to be either returning None or
    # resulting in a runtime error
    # bbc.bbc(headlines[5])

start_time = '100d'
end_time = '0d'
reddit(start_time, end_time)
