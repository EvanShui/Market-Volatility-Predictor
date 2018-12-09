"""Script that executes all other scripts in this repository
"""
from scraping.generate_data import generate_data
from models.build_model import build_model 


def main():
    GEN_DATA = 0
    # allows for user to choose variables for data collection, may yield better
    # results in the future
    if GEN_DATA:
        generate_data(50, 10, 10)
    build_model()

if __name__ == '__main__':
    main()
