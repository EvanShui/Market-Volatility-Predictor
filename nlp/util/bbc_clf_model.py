import sklearn
import numpy as np
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn import metrics
from sklearn.externals import joblib


### 1. Set categories
categories = ['business', 'entertainment', 'politics', 'sport', 'tech']


### 2. Load dataset
docs_to_train = sklearn.datasets.load_files("./bbc", description=None, categories=categories,
                                            load_content=True, encoding='utf-8',
                                            decode_error="replace",
                                            shuffle=True, random_state=42)

### 2a. Calculate count of each category
labels, counts = np.unique(docs_to_train.target, return_counts=True)

# Convert data.target_names to np array for fancy indexing
labels_str = np.array(docs_to_train.target_names)[labels]
print(dict(zip(labels_str, counts)))


### 3. Split dataset into training (80%) and test set (20%)
# X_train: test file data to train, y_train: category names for train data
# X_test: test file data to test, y_test: category names for test data
X_train, X_test, y_train, y_test = train_test_split(docs_to_train.data,
                                                    docs_to_train.target,
                                                    test_size=0.2)

### 4. Transform training data
vectorizer = TfidfVectorizer(stop_words='english',
                             max_features=1000, decode_error="ignore")
vectorizer.fit(X_train)


### 5. Transform test data
vectorizer = TfidfVectorizer(stop_words='english',
                             max_features=1000, decode_error="ignore")
vectorizer.fit(X_test)


### 6. Train Classifier/Model
text_clf = SGDClassifier(loss='hinge', penalty='l2',
                    alpha=1e-3, random_state=42,
                    max_iter=5, tol=None)

text_clf.fit(vectorizer.transform(X_train), y_train)


#### 7. Test trained model using test data
predicted = text_clf.predict(vectorizer.transform(X_test))

# Print the results of the predictions
for doc, cat in zip(X_test, predicted):
    print('%r => %s' % (doc, categories[cat]))


### 8. Evaluate Accuracy

# Note the average is pretty close to 1, meaning the model performs pretty well
print(metrics.classification_report(y_test, predicted,
    target_names=docs_to_train.target_names))


### 9. Persistence

# Save model and vectorizer
joblib.dump(text_clf, 'util/bbc_cat_model.sav')
joblib.dump(vectorizer, 'util/vectorizer.sav')


