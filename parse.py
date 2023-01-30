
import requests
from bs4 import BeautifulSoup as BS
from database.views import *

BASE_URL = 'https://asiastore.kg/'

def get_soup(url):
    response = requests.get(url)
    soup = BS(response.text, 'lxml')
    return soup

def get_categories(url):
    soup = get_soup(BASE_URL + url)
    category_list = soup.find('div', class_ = 'category-list')
    all_a = category_list.find_all('a')
    # urls = category_list.find_all('a')
    # urls2 = [url.get('href') for url in urls]
    # print(urls2)
    cats_urls = {a.find('span').text.strip(): a.get('href') for a in all_a}
    return cats_urls


def parse_goods(url):
    soup = get_soup(url)
    row = soup.find('div', class_ = 'row cat-flex')
    h4 = row.find_all('h4')
    if url.startswith('http://asiastore.kg/apple-iphone'):
        names_to_urls = {h.text.strip(): h.find('a').get('href') for h in h4}

    elif url == 'http://asiastore.kg/apple-mac/mac-studio/':
        names_to_urls = {h.text.strip(): h.find('a').get('href') for h in h4 if h.text.strip().startswith('Apple Mac Studio')}
    
    return names_to_urls



def main():
    # get_categories(BASE_URL + 'apple-iphone/')
    parse_goods('https://asiastore.kg/apple-iphone/iphone-14-pro-max/')


if __name__ == '__main__':
    main()

