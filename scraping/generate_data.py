from datetime import datetime
import random
import json
import sys
import os
import time
sys.path.insert(0, '../../data_301_project/')
from scraping.reddit import reddit
from scraping.article_scraper import scrape_article
from scraping.sentiment_analysis import sentiment_analysis

def generate_reddit_json(time, total_days, days_apart, num_entries):
    # generating data in increments of 100 days
    lst = []
    print('gathering data...')
    for i in range(0, total_days, days_apart):
        lst += reddit(i, i+days_apart, num_entries) 
    print("length of reddit list: ", len(lst))
    id_num = 1
    for i in lst:
        i['id'] = id_num
        id_num += 1
    print('appended id\'s')
    print('data gathered')
    print("writing file...")
    print("generate reddit data cwd: ", os.getcwd())
    file_name = './data/{}_reddit.json'.format(time)    
    with open(file_name, 'w+') as f:
        json.dump(lst, f)
    print("done writing file")
    return file_name

def generate_articles_json(reddit_file, time):
    success = 0
    error = 0
    ret_lst = []
    with open(reddit_file, 'r') as f:
        reddit_json = json.load(f)
    print("-"*100)
    print("reddit json length: ", len(reddit_json))
    print(reddit_file)
    for reddit_entry in reddit_json:
        print(reddit_entry['title'], reddit_entry['url'])
        newspaper_json = scrape_article(reddit_entry['id'], reddit_entry['title'], reddit_entry['url'])
        if newspaper_json['title']:
            success += 1
        else:
            error += 1
        print(newspaper_json)
        ret_lst.append(newspaper_json) 
    file_name = './data/{}_articles.json'.format(time)
    with open(file_name, 'w+') as f:
        json.dump(ret_lst, f)
    print("SUCCESS: {}\nERROR: {}".format(success, error))
    return file_name

def generate_sentiment_analysis_json(reddit_file, time):
    TEST = 0
    ret_lst = []
    with open(reddit_file, 'r') as f:
        reddit_json = json.load(f)
        if TEST:
            rand_ind = random.sample(range(len(reddit_json)), 1)
            reddit_json = [reddit_json[i] for i in rand_ind]
    for reddit_entry in reddit_json:
        sa_json = sentiment_analysis(reddit_entry['id'],
                reddit_entry['title'],reddit_entry['created_utc'])
        ret_lst.append(sa_json)
        file_name = './data/{}_sa.json'.format(time)
    # Change this after creating a blank document
    with open(file_name, 'w+') as f:
        json.dump(ret_lst, f)
    return file_name

def generate_data(total_days, days_apart, num_entries):
    """
    Script to scrape for all data

    Input:
    total_days(int): Total number of days to scrape for on Reddit
    days_apart(int): The number of days apart from each scraping period
    num_entries(int): Number of entries per scraping period

    Output:
    reddit_data.json
    articles.json
    sa.json
    (look at /data/recent_files.json for exact file names)
    """

    TEST_REDDIT = 1
    TEST_ARTICLES = 1
    TEST_SA = 1
    current_time = datetime.utcnow().strftime("%Y-%m-%d_%H:%M:%S")
    file_json = {}
    if TEST_REDDIT:
        reddit_file = './data/reddit_data.json'
    else:
        reddit_file = generate_reddit_json(current_time, total_days, days_apart, num_entries)
    file_json['reddit'] = reddit_file
    if TEST_ARTICLES:
        articles_file = './data/articles.json'
    else:
        articles_file = generate_articles_json(reddit_file, current_time)
    file_json['articles'] = articles_file
    if TEST_SA:
        sa_file = './data/sa.json'  
    else:
        sa_file = generate_sentiment_analysis_json(reddit_file, current_time)
    file_json['sa'] = sa_file

    if TEST_REDDIT and TEST_ARTICLES and TEST_SA:
        with open('./data/default_files.json', 'w+') as f:
            json.dump(file_json, f)
    else:
        with open('./data/recent_files.json', 'w+') as f:
            json.dump(file_json, f)