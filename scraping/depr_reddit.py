import json
import urllib3
http = urllib3.PoolManager()

import bbc

def reddit(start_time, end_time):
    user_agent = ""
    # specify the url name and parameters
    pushshift_url = (
        f'https://api.pushshift.io/reddit/search/submission/?sort_type=score'
        f'&subreddit=news&&after={start_time}&&before={end_time}&&score>=100'
    )

    # query pushshift API and retrieve the JSON reddit posts in r/news
    response = http.request('GET', pushshift_url)
    reddit_posts = json.loads(response.data.decode('utf-8'))['data']

    # extract just the title from each post in the list of reddit posts
    headlines = [post['title'] for post in reddit_posts]
    print(headlines)
    print(pushshift_url)

    # test call of the bbc function
    # at the moment this seems to be either returning None or
    # resulting in a runtime error
    # bbc.bbc(headlines[5])

start_time = '1d'
end_time = '0d'
reddit(start_time, end_time)
