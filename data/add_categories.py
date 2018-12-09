import sys
sys.path.insert(0, '../data_301_project/')
from nlp.bbc_categorization import bbc_categorization
import json
import pandas as pd

with open('data/articles.json', 'r') as f:
    data = json.load(f)
df = pd.DataFrame(data)
print(df.columns)
print(df.head(10))
print(df['title'][0])
df.dropna(axis=0, inplace=True)
df['category'] = df.apply(lambda x: 
        bbc_categorization(x['title'] + ' ' + x['text'], x['id']), axis=1)
with open('data/categories.json', 'w+') as f:
    f.write(df.to_json())
