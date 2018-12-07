from reddit import reddit
from article_scraper import scrape_article
from datetime import datetime
import json
import sys
import os
sys.path.insert(0, '../../data_301_project/')

def generate_reddit_json(time):
    # generating data in increments of 100 days
    lst = []
    print('gathering data...')
    for i in range(0, 2100, 100):
        lst += reddit(i, i+100) 
    id_num = 1
    for i in lst:
        i['id'] = id_num
        id_num += 1
    print('appended id\'s')
    print('data gathered')
    print("writing file...")
    print("generate reddit data cwd: ", os.getcwd())
    file_name = './data/{}_reddit_data.json'.format(time)    
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
    for reddit_entry in reddit_json:
        print(reddit_entry['title'], reddit_entry['url'])
        newspaper_json = scrape_article(reddit_entry['id'], reddit_entry['title'], reddit_entry['url'])
        if newspaper_json['title']:
            success += 1
        else:
            error += 1
        print(newspaper_json)
        ret_lst.append(newspaper_json) 
    with open('./data/{}_new_articles.json'.format(time), 'w+') as f:
        json.dump(ret_lst, f)
    print("SUCCESS: {}\nERROR: {}".format(tracker.success, tracker.error))

if __name__ == '__main__':
    os.chdir("..")
    current_time = datetime.utcnow().strftime("%Y-%m-%d_%H:%M:%S")
    reddit_file = generate_reddit_json(current_time)
    generate_articles_json(reddit_file, current_time)