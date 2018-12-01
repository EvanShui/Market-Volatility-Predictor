"""Script that executes all other scripts in this repository
"""
from scraping.scraper import scraper
import sys

def main():
    scraper()
    print('hello world')

if __name__ == '__main__':
    main()
