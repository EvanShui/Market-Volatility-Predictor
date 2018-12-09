import json
import pandas as pd
lst = []
with open('categories.json', 'r') as f:
    lst = json.load(f)
with open('articles_w_categories' ,'w+') as f:
    json.dump(pd.DataFrame(lst).to_dict('records'), f)