"""Script that executes all other scripts in this repository
"""
from scraping.generate_data import generate_data
from models.build_model import build_model 
import json

def main():
    NEW_DATA = 0
    GEN_DATA = 1
    # allows for user to choose variables for data collection, may yield better
    # results in the future
    if GEN_DATA:
        generate_data(50, 10, 10)
    if NEW_DATA:
        with open('./data/recent_files.json', 'r') as f:
            file_name = json.load(f)
    else:
        with open('./data/default_files.json', 'r') as f:
            file_name = json.load(f)
    build_model(file_name)

if __name__ == '__main__':
    main()
