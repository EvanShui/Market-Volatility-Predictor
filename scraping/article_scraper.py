import requests
import sys
from bs4 import BeautifulSoup
import stringdist
import json
from pprint import pprint
import random
from newspaper import Article
import sys
sys.path.insert(0, '../../data_301_project/')
from nlp.bbc_categorization import bbc_categorization

def scrape_article(id_num, headline, url):
    """
    Scrapes the article for text and headline

    Input: id_num (int)
    headline(string) - headline of article
    url(string) - url of article

    Output: json object
    {'id': id_num,
     'title': title of the article
     'text': text of the article
     'url': url of the article
     'category': category the article falls under as specified by
     bbc_categorization
    }
    """
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
        # If something goes wrong
        return {'id': id_num, 'title': None, 'text':None, 'url':url,
                'category': None}
    try:
        category = bbc_categorization(article.title + ' ' + article.text,
                id_num)
    except:
        raise AttributeError("issue with bbc")
    return {'id': id_num, 'title': article.title,'text': article.text, 'url':
            url, 'category': category}