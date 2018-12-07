import requests
import sys
from bs4 import BeautifulSoup
import stringdist
import json
from pprint import pprint
import random
from newspaper import Article

def load_reddit_json():
    """
    """
    headline = []
    with open('reddit_data.json') as f:
        data = json.load(f)
    for d in data:
        headline.append(d)
    return(headline)

def scrape_article(id_num, headline, url):

    article = Article(url)
    from time import sleep
    from newspaper.article import ArticleException, ArticleDownloadState

    # Download article
    slept = 0
    try:
        article.download()
        while article.download_state == ArticleDownloadState.NOT_STARTED:
            # Raise exception if article download state does not change after 10 seconds
            if slept > 9:
                raise ArticleException('Download never started')
            sleep(1)
            slept += 1
        # Parse article
        article.parse()
    except:
        return {'id': id_num, 'title': None, 'text':None, 'url':url}
    print("article title: {} article text: {}".format(article.title,
        article.text))
    return {'id': id_num, 'title': article.title,'text': article.text, 'url':
            url}
"""
if __name__ == '__main__':
    reddit_json = load_reddit_json()
    ret_lst = []
    for reddit_entry in reddit_json:
        newspaper_json = newspaper(reddit_entry['id'], reddit_entry['title'], reddit_entry['url'])
        ret_lst.append(newspaper_json) 
    with open('articles.json', 'w+') as f:
        json.dump(ret_lst, f)
"""