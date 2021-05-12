from bs4 import BeautifulSoup
import requests
import csv

URL = 'https://books.toscrape.com/catalogue/finders-keepers-bill-hodges-trilogy-2_807/index.html'
GLOBAL_CAT_URL = 'https://books.toscrape.com/'
CATEGORY_URL = 'https://books.toscrape.com/catalogue/category/books/fiction_10/index.html'

def book_data(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    booking = soup.find_all(class_='default')

    for books in booking:
        upc = books.find('th', text='UPC').find_next_sibling('td').text# p2 Collecte du code produit
        title = books.find('h1').text# p3 collecte du titre du livre
        price_include = books.find('th', text='Price (incl. tax)').find_next_sibling('td').text# p4 prix avec taxe
        price_exclude = books.find('th', text='Price (excl. tax)').find_next_sibling('td').text# p5 prix hors taxe.
        availability = books.find('th', text='Availability').find_next_sibling('td').text# p6 disponibilité.
        stock = availability.strip('In stock () available')
        description = books.find(class_='sub-header').find_next('p')# p7 description produit.
        book_description = description.text
        category = books.find(class_='breadcrumb').find_next('a').text# p8 cathégory.
        review = books.find('p', class_='star-rating').get('class')[1] #"avis" je cherche a retourner la valeur de la position dans la class star-rating[0] Five[1]
        image_scrape = books.find('div', class_='item active').find_next('img')# p10 url de l'image.
        filter_img = image_scrape.get('src').strip('../..')
        
    return {'product_page_url': url,
            'upc': upc,
            'title': title,
            'price_including_tax': price_include,
            'price_excluding_tax':price_exclude,
            'number_available': stock,
            'product_description':book_description,
            'category':category,
            'review_rating':review,
            'image_url':filter_img
            }


def get_categories():
    global_cat_url = 'https://books.toscrape.com/'
    data = {}
    response = requests.get(global_cat_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    category_scrape = soup.find('div', class_='side_categories').find('li').find_all('li')
    for category in category_scrape:
        books_url = category.find('a', href = True).get('href')
        cat_title = category.text.strip() # afficher les données récupéré en utilisant une méthode qui récurpère uniquement le texte du lien "href" et de couper les espaces inutiles " .strip "
        data[cat_title] = global_cat_url + books_url  # data a pour clef la varaible cat_title des titres des categories et à comme valeur l'url des categories.
    return data

# fonction qui boucle sur les livres d'une catégorie et les pages qui la compose
def get_books_data(url):
    links = []
    r = requests.get(url) # récupération de l'url pour le scrape
    soup = BeautifulSoup(r.content, 'html.parser') # méthode pour récupérer les données
    for books in soup.find_all('article', class_='product_pod'):# boucler sur la methode et récuperer toutes les données d'une page ou plusieurs pages selon la condition
        books_link_url = books.find('a', href = True)
        books_url = books_link_url.get('href').strip('../../../')
        links.append(GLOBAL_CAT_URL + 'catalogue/' + books_url)
    next = soup.find('li', class_='next')
    if next is not None:
        next_page = url.split('/')[0 : -1] # destructuration de l'url category_url du dernier element "index.html"
        next_page.append(next.find('a').get('href')) # ajout de l'element ciblé sur la nouvel url "page-2.html"
        next_page_url = '/'.join(next_page) # restructuration de l'url avec le nouvel element
        links.extend(get_books_data(next_page_url))
    return links          

for category_name,category_url in get_categories().items():
    with open(category_name + '.csv', 'w', encoding='utf-8') as csvfile:
        fieldnames = ['product_page_url', 'upc', 'title', 'price_including_tax', 'price', 'price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating', 'image_url']
        wr = csv.DictWriter(csvfile, fieldnames=fieldnames)
        wr.writeheader()
        for url in get_books_data(category_url):
            book_info = book_data(url)
            wr.writerow(book_info)