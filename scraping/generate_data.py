from reddit import reddit
import json
import sys
import os
sys.path.insert(0, '../../data_301_project/')

def generate_reddit_data():
    # generating data in increments of 100 days
    lst = []
    print('gathering data...')
    for i in range(0, 2100, 100):
        lst += reddit(i, i+100) 
    print('data gathered')
    os.chdir("..")
    print("writing file...")
    with open('./data/reddit_data.json', 'w+') as f:
        json.dump(lst, f)
    print("done writing file")

if __name__ == '__main__':
    generate_reddit_data()