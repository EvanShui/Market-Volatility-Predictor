# coding: utf-8
import json
import pandas as pd
import datetime
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import pandas_datareader.data as web
from sklearn.feature_extraction import DictVectorizer

def build_model(files):
    print(files)
    with open(files['reddit'], 'r') as f:
        reddit_df = json.load(f)
    reddit_df = pd.DataFrame(reddit_df)

    with open(files['articles'], 'r') as f:
        article_df = pd.DataFrame(json.load(f))
    article_df.sort_values('id')

    with open(files['sa'], 'r') as f:
        sa_df = pd.DataFrame(json.load(f)).rename(columns={'id_num': 'id'})
    sa_df

    # merges json files into single data frame
    proc_df = pd.merge(reddit_df, article_df, on='id', suffixes=['_reddit', '_article'])
    proc_df = pd.merge(proc_df, sa_df, on='id')
    # creates column for human readable date
    proc_df['date_created'] = proc_df.created_utc.apply(lambda x:
                                             datetime.datetime.utcfromtimestamp(x).strftime("%Y-%m-%d"))
    df = proc_df

    date_entries = df.sort_values(by='date_created').groupby('date_created').count()['author']
    date_lte2_entries = [i for i in date_entries[date_entries <= 2].index]
    # filters out all entries with dates that appear less than 3 times
    # want at least 3 articles per date (since that is what we will be passing
    # into this function
    gte3_df = df[~df['date_created'].isin(date_lte2_entries)]

    # get the top three articles filtered by score and store into dataframe
    final_df = gte3_df.sort_values(['date_created', 'score'], ascending=False).groupby('date_created').head(3).sort_values('date_created')

    cut_df = final_df.drop(['author', 'created_utc', 'title_reddit', 'text', 'title_article', 'url', 'title'], axis=1)
    cut_df.rename(columns={'date_created':'Date'}, inplace=True)
    date_df = cut_df[['id', 'Date']]

    # handling categorical variables
    vec = DictVectorizer(sparse=False, dtype =int)
    result = vec.fit_transform(cut_df.drop('Date', axis=1).to_dict('records'))
    category_df = pd.DataFrame(result, columns=vec.get_feature_names())
    cut_df = pd.merge(date_df, category_df, on='id')

    # reading in stock closing prices for SPY500
    x = cut_df['Date'].iloc[0]
    y = cut_df['Date'].iloc[-1]
    start = datetime.datetime.strptime(x, '%Y-%m-%d')
    end = datetime.datetime.strptime(y, '%Y-%m-%d')
    f = web.DataReader('SPY', 'yahoo', start, end)
    f = f.reset_index()
    f.Date = f.reset_index().Date.astype('str')
    f['Diff'] = f.set_index('Date').diff().reset_index().drop(0)['Close'].reset_index().drop('index',
            axis=1)
    f = f.dropna()
    # merge stock prices with current dataframe
    final_df = pd.merge(f.reset_index()[['Date', 'Diff']], cut_df, on='Date')
    # calculate the 'true score' of a dataframe by adding up the three score
    # values of the articles and dividing it by the highest score
    true_score_df = pd.DataFrame(final_df.groupby('Date').apply(lambda x: sum(x['score']) / max(x['score']))).reset_index().rename(columns={0:'true_score'})
    cut_df = pd.merge(true_score_df, final_df, on='Date')

    # compressing three entries on same day into one by combining the
    # categorical variable vectors into a single vector and summing the
    # sentiment analysis column
    summed_df = cut_df.drop(['id', 'score'], axis=1).groupby(['Date',
        'true_score', 'Diff'])[['category=business','category=entertainment',
                                                                         'category=politics', 'category=sport',
                                                                         'category=tech', 'sa']].sum()
    final_df = summed_df.reset_index()

    final_df = final_df[['true_score', 'category=business', 'category=entertainment',
                                                'category=sport',
                                                'category=politics',
                                                'category=tech','sa', 'Diff']]

    # building regression model
    X = final_df.iloc[:, :-1].values
    y = final_df.iloc[:, -1]. values
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)
    regressor = LinearRegression()
    regressor.fit(X_train, y_train)
    y_pred = regressor.predict(X_test)
    # we're predicting on the MINIMUM value threshold of SPY500. If the
    # predicted value is less than the actual value, we consider that to be
    # a 'correct' prediction, since the actual value was greater than the
    # minimum threshold we predicted.
    print("number of current predictions: ", sum((y_test- y_pred) > 0))
    print("total number of predictions: ", len(y_test))
    print("accuracy: ", sum((y_test-y_pred) > 0) / len(y_test))
