# data_301_project

## purpose
We want to determine whether there is a correlation between the impact an event has with the volatity of the stock market. Specifically, we want to see if a high impact event will lead to a high volatility of the stock market of next trading day and vice versa.

## Project Overview
To determine impact of an event, we have 3 metrics: 
* popularity of an event, scraped from Reddit
  * Popularity is determined by number of net votes by a post and number of shares.
* general public emotion, scraped from Twitter
  * Emotion is determined by using emotional semantic analysis on Twitter posts relating to the given event.
* context of an event, scraped from BBC.
  * Context of an event inculdes keywords of the event, title of the event, and what sector that event belongs in (Finance, Government, Sports, Etc.)

By using these metrics, we aim to pass these to a multivariate linear regression model to determine what the threshold is (minimum value) of the volatity index (VIX) of next trading day.

### Data Scraping
We will be using Beautiful Soup 4 to scrape Reddit and BBC. We also plan on using some kind of Twitter API to scrape posts on Twitter. We will then be processing all of these scripts on Python 3.7, where we will store the results on GCP (Google Cloud Platform). These scripts will be stored in /scraping

### NLP Processing
We will be using NLTK on BBC articles to determine the context of the articles and Twitter posts for emotional semantic analysis. The scripts that process the data will be stored in /nlp

### Creating a model
We will be using scikit_learn to create a multivariate linear regression model to predict the next trading day VIX threshold. The scripts that create the model (and the model itself) will be stored in /model

### Main Function
The function that will be running all of the scripts, nlp processing, and model creation will be in the parent directory, it will be main.py.

## Standards
We will be using Anaconda and it's version of Python to work on this project.
Tabs - set to 4 spaces.
Every member should fork this project and work on it in their own repository. Then, when you want to submit a change, submit a pull request to the main repo (the respository in EvanShui's github account) and two members will review it.
