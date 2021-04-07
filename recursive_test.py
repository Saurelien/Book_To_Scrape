from bs4 import BeautifulSoup
import requests
import csv
from PIL import Image

global_cat_url = 'https://books.toscrape.com/'
global_url = 'https://books.toscrape.com/catalogue/category/books/fiction_10/index.html'



def recursive_scrape(scraping_books):
    data = []
    r = requests.get(global_url)
    soup = BeautifulSoup(r.content, 'html.parser')
    get_scraped = soup.find_all(class_='default')
    
    for get_scraped_test in get_scraped:
        for get_scraped_test in get_scraped_test.find_all('li', class_='col-xs-6 col-sm-4 col-md-3 col-lg-3'):
            books_title = get_scraped_test.find('h3')
            books_link_url = get_scraped_test.find(href= True)
            prices = get_scraped_test.find('p', class_='price_color')
            switch = get_scraped_test.find('div').find_next('li', class_='next', text = 'next')
            images = get_scraped_test.find('a', href = True).find_next('img', class_='thumbnail')
            print(images.get('src').strip('../../../../'))
            print(prices.text.strip())
            print(books_link_url.get('href').strip('../../../'))
            print(books_title.text.lower().strip())
            print(switch.text)
            next = True
            if next is True:
                data2 = recursive_scrape(scraping_books + 'page=4')
                data.extend(data2)
    return data
        


#for scraping_books in get_categories():
#    with open('categories_test.csv', 'w') as csvfile:
#        for 
#            fieldnames = ['movie_categories']
#            wr = csv.DictWriter(csvfile, fieldnames=fieldnames)
#            wr.writeheader()
#            wr.writerow(recursive_scrape(global_url))
recursive_scrape('scraping_books')