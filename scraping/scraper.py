import sys
sys.path.insert(0, '../../data_301_project')
from scraping.twitter_scraper import scrape_tweets

def scraper():
    print('scraping')
    print('scraping tweets')
    scrape_tweets()

if __name__ == '__main__':
    scraper()
