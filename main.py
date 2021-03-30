from bs4 import BeautifulSoup
import requests
import csv

def book_data(url):
    # p1 recuperation url de la page produit
    response = requests.get(url)
    # Déclaration de la variable de la classe beautifulsoup et s'en servir pour collecter les données nécessaires.
    book_soup = BeautifulSoup(response.content, 'html.parser')
    booking = book_soup.find_all(class_='default')

    for books in booking:
        # p2 Collecte du code produit
        upc = books.find('th', text='UPC').find_next_sibling('td').text
        # p3 collecte du titre du livre
        title = books.find('h1').text
        # p4 prix avec taxe.
        price_include = books.find('th', text='Price (incl. tax)').find_next_sibling('td').text
        # p5 prix hors taxe.
        price_exclude = books.find('th', text='Price (excl. tax)').find_next_sibling('td').text
        # p6 disponibilité.
        availability = books.find('th', text='Availability').find_next_sibling('td').text
        stock = availability.strip('In stock () available')
        # p7 description produit.
        description = books.find(class_='sub-header').find_next_sibling('p').text
        # p8 cathégory.
        category = books.find(class_='breadcrumb').find_next('a', text='Fiction').text
        # p9 avis clients
        review = books.find('p', class_='star-rating Five').get('class')[1] # je cherche a retourner la valeur de la position dans la class star-rating[0] Five[1]
        # p10 url de l'image.
        image_scrape = books.find('div', class_='item active').find_next('img')
        filter_img = image_scrape.get('src').strip('../..')
        
        return {'product_page_url': url,
            'upc': upc,
            'title': title,
            'price_including_tax': price_include,
            'price_excluding_tax':price_exclude,
            'number_available': stock,
            'product_description':description,
            'category':category,
            'review_rating':review,
            'image_url':filter_img
            }


def csv_file():
    url = 'http://books.toscrape.com/catalogue/finders-keepers-bill-hodges-trilogy-2_807/index.html'
    # p1 recuperation url de la page produit
    response = requests.get('http://books.toscrape.com/catalogue/finders-keepers-bill-hodges-trilogy-2_807/index.html')
    # Déclaration de la variable de la classe beautifulsoup et s'en servir pour collecter les données nécessaires.
    book_soup = BeautifulSoup(response.content, 'html.parser')
    booking = book_soup.find_all(class_='default')
    with open('book.csv', 'w') as csvfile:
        fieldnames = ['product_page_url', 'upc', 'title', 'price_including_tax', 'price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating', 'image_url']
        wr = csv.DictWriter(csvfile, fieldnames=fieldnames)
        wr.writeheader()
        wr.writerow(book_data(url))
        
csv_file()