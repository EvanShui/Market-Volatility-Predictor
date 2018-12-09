from sklearn.externals import joblib
import os

categories = ['business', 'entertainment', 'politics', 'sport', 'tech']

def bbc_categorization(contents, id_num):

    arr = [contents]
    print(id_num)

    # Load model and vectorizer
    text_clf = joblib.load('./models/util/bbc_cat_model.sav')
    vectorizer = joblib.load('./models/util/vectorizer.sav')

    predicted = text_clf.predict(vectorizer.transform(arr))

    return categories[predicted[0]]

# Example
def main():

    title = 'Pelosis supporters are confident she will have votes to become House speaker'
    contents = 'During her more than 30 years in the House, and about half of that time as the ' \
               'chambers top Democrat, Pelosi has built a reputation as a master vote-counter and ' \
               'dealmaker within her party. But in recent years, she also has become a favorite ' \
               'target of the GOP — to the extent that several Democrats campaigning during this ' \
               'year’s midterm elections sought to distance themselves from her, even pledging to not ' \
               'vote for Pelosi as speaker. Pelosi has been working to change the minds of those members ' \
               'and shore up the support she has among the incoming class. Over the weekend, Sharice ' \
               'Davids — who won in a Kansas district that went handily to Trump in 2016 — announced she ' \
               'would back Pelosi and look to shake up the partys leadership elsewhere.'

    topic =  bbc_categorization(title + ' ' + contents)

    # Print the results of the prediction
    print('Topic is: ', topic)

    return topic

if __name__ == '__main__':
   main()