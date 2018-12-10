# data_301_project

## purpose
We want to determine whether there is a correlation between the impact an event has with the volatity of the stock market. Specifically, we want to see if a high impact event will lead to a high volatility of the stock market of next trading day and vice versa.

## Project Overview
To determine impact of an event, we have 3 metrics: 
* popularity of an event, scraped from Reddit
  * Popularity is determined by number of net votes by a post and number of shares.
* positivity of a news article
  * positivity is determined by using semantic analysis on Reddit post headlines.
* context of an event, scraped from BBC.
  * Context of an event inculdes keywords of the event, title of the event, and what sector that event belongs in (Business, Politics, Sports, Etc.)

These metrics are passed to a multivariate linear regression model to determine what the difference is of the Standard and Poor’s 500 Index (SPY500) between the current day and the next trading day.

### Data Scraping
To scrape data from Reddit, we utilized the Pushshift API to access comments and submission datasets. Another python library, Newspaper, was used to scrape and parse news articles for their content and title.

### NLP Processing
NLTK was employed to tokenize strings from Reddit article headlines and TextBlob was used for Sentiment Analysis. A value of 1 reflects positive reaction, 0 for neutral, and -1 if negative. For BBC article text, the sklearn library was used to create a classifier capable of receiving new, unlabeled text data and assign it to the best fitting category. The model was trained on a BBC dataset of 2225 articles each assigned to 5 categories: business, politics, entertainment, sports, and technology.

### Preprocessing Data
After gathering all data needed from Reddit, BBC articles, and performing semantic analysis on article titles, the information is collectively used to train and test the final linear regression model (80% training, 20% test). Information from different sources were associated by date, and to aggregate multiple entries (for a single date) into one value for testing and training our model we did the following:
* Reddit popularity score: calculate a true/‘normalized’ score to reduce redundancy, increase integrity, and standardize impact
* BBC Articles: vectorize values for article categories/topics to work with numerical data
* Semantic Analysis: sum of semantic analysis values on Reddit article titles 
* Stock Prices (SPY500):  difference between closing stock prices of the current and next trading day


### Creating a model
We used scikit_learn to create a multivariate linear regression model in order to predict what the minimum threshold value is for the next trading day. The model aggregates all data collected (Preprocessing Data), while also reading in stock closing prices for SPY500, to make the prediction.

### Main Function
The function that will be running all of the scripts, nlp processing, and model creation will be in the parent directory, it will be main.py. It contains two functions right now, generate_data, which will re-generate all of the data from scratch, and build_model, which will process the data and train / test the LinearRegression model.

## Standards
We will be using Anaconda and it's version of Python to work on this project.
Tabs - set to 4 spaces.
Every member should fork this project and work on it in their own repository. Then, when you want to submit a change, submit a pull request to the main repo (the respository in EvanShui's github account) and two members will review it.
DOCUMENTATION. Document every function you write.

## File Structure

### Data
Holds all of the JSON data that we will be working with for this project. All JSON files should be written into this folder. There should never be JSON files stored in any of the other folders.

### Scraper
Holds all of the scripts that scrape the web. The 'main.py' file in this folder is scraper.py.

### NLP
Holds all of the scripts that will analyze the raw data from the scraping scripts. The 'main.py' file in this folder is analyze.py

### Model
Holds the script that creates the multi-variate linear regression model. The 'main.py' file in this folder is build_model.py
