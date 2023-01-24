
import requests
from bs4 import BeautifulSoup as BS

BASE_URL = 'https://asiastore.kg/'

def get_soup(url):
    response = requests.get(url)
    soup = BS(response.text, 'lxml')
    return soup

def get_categories(url):
    soup = get_soup(url)
    category_list = soup.find('div', class_ = 'category-list')
    categories = category_list.find_all('span')
    cats = [x.text.strip() for x in categories]
    return cats


def main():
    get_categories(BASE_URL + 'apple-iphone/')


if __name__ == '__main__':
    main()

