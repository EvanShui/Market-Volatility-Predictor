import urllib3
from urllib.request import Request, urlopen
http = urllib3.PoolManager()
from bs4 import BeautifulSoup

# specify the url
start_time = 1540623600
end_time = 1540796400
redditsearch_url = (
    f'https://redditsearch.io/?term=&dataviz=false&aggs=false'
    f'&subreddits=news&searchtype=posts&search=true&start={start_time}'
    f'&end={end_time}&size=20'
)

r = Request(redditsearch_url, headers={'User-Agent': 'Mozilla/5.0'})
w = urlopen(r).read()
print('yo')
print(w)

# query redditsearch website and retrieve the html
response = http.request('GET', redditsearch_url)
reddit_page = response.data

# parse the html using BeautifulSoup
reddit_page = BeautifulSoup(reddit_page, 'html.parser')

# from the reddit page, extract the div containing the actual news
# news = reddit_page.find('div', attrs={'id': 'posts'})

# all the titles are enclosed in <div> tags with the class 'title'
# extract all titles from news
# headlines = reddit_page.find_all('div', attrs={'class': 'title'})

# for i in range(len(headlines)):
#     print(headlines[i].text)
