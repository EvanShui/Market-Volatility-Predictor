
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import SGDClassifier

from sklearn.pipeline import Pipeline

#comp.os.ms-windows.misc
#comp.sys.ibm.pc.hardware
#comp.sys.mac.hardware
#comp.windows.x

# Categories
categories = ['rec.autos', 'rec.motorcycles', 'rec.sport.baseball', 'rec.sport.hockey', 'sci.crypt',
              'sci.electronics', 'sci.space', 'misc.forsale', 'talk.politics.misc',
              'talk.politics.guns', 'talk.politics.mideast', 'talk.religion.misc','alt.atheism', 'soc.religion.christian', 'comp.graphics', 'sci.med']


# Load files matching categories
# twenty_train is a "bunch" (holder object)
# fields that may be accessed as python dict keys object attributes
# files are in data attribute: twenty_train.data
twenty_train = fetch_20newsgroups(subset='train', categories=categories, shuffle=True, random_state=42)

# Bag of words: turning text content into numerical feature vectors
count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(twenty_train.data)

# Tf-IDF
# Fit estimator to data, then transform count-matrix (above) to tf-idf representation
tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)

# TRAINING CLASSIFIER
clf = MultinomialNB().fit(X_train_tfidf, twenty_train.target)

# ----------------------------------------------------------------------#

# PIPELINE to vectorize -> transform -> classify
text_clf = Pipeline([('vect', CountVectorizer()),
                     ('tfidf', TfidfTransformer()),
                     ('clf', SGDClassifier(loss='hinge', penalty='l2',
                                           alpha=1e-3, random_state=42,
                                           max_iter=5, tol=None))
                     ])

# Train in a single command
text_clf.fit(twenty_train.data, twenty_train.target)

# NEW DOCS
docs_new = ['Lebron James for the win. Dribbling and 3-pointers!', 'President Obama oh my gosh',
            'Jennifer Aniston is hilarious in Friends. I watch that TV show everyday',
            'I drive a BMW. The car acceleration is pretty good',
            'Adobe is pretty cool tool. I use it to do art on my computer all the time']

#X_new_counts = count_vect.transform(docs_new)
#X_newtfidf = tfidf_transformer.transform(X_new_counts)

# PREDICTION on new docs
predicted = text_clf.predict(docs_new)

# Print the results of the predictions
for doc, cat in zip(docs_new, predicted):
    print('%r => %s' % (doc, twenty_train.target_names[cat]))