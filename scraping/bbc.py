import requests
import sys
from bs4 import BeautifulSoup
import stringdist

def bbc(headline):
    headline_list = []
    print("headline: " + headline)

    # Collect and parse first page
    url = ('https://www.bbc.co.uk/search?q=' + headline)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Pull all text from the BodyText div
    news_list = soup.find("ol", class_="search-results")
    
    #check if there is an Error
    if news_list is None:
        print("Error: No article with that date and headline")
        return None
    
    news_list_items = news_list.find_all('a')
    # Create for loop to print out all artists' names
    for news in news_list_items:
            names = news.text
            link = news.attrs['href']
            if(len(names) > 0 and names[0] != '\n'):
                headline_list.append((names,link))

    # calculating Levenshtein distance between entered headline and bbc headlines 
    l_min = stringdist.levenshtein(headline_list[0][0], headline)
    closest_headline = headline_list[0]
    for i in range(1,len(headline_list)):
        l_value = stringdist.levenshtein(headline_list[i][0], headline)
        if l_value < l_min:
            l_min = l_value
            closest_headline = headline_list[i]

    # setting up article's content
    article_text = ''
    
    # Collect and parse the headline with the smallest Levenshtein distance
    url = (closest_headline[1])
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Pull all text from the BodyText div
    date = soup.find("div", {"class":"date"}).text
    print("Date: ",date)
    article = soup.find("div", {"class":"story-body__inner"}).findAll('p')
    
    if article is None:
        print("Error: Content of headline ",closest_headline[0],"couldn't be found at",closest_headline[1])
        return None
    for element in article:
        article_text += '\n' + ''.join(element.findAll(text = True))
    
    result = {'title': closest_headline[0],
            'date': date,
            'content': article_text}
    return result

#headline = "fire at a town"
#print(bbc(headline))
