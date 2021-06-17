from bs4 import BeautifulSoup
import requests
import os
from pathlib import Path
import csv

GLOBAL_CAT_URL = 'https://books.toscrape.com/'

# Fonction permettant de récupérer les informations demandé d'un livre
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
        category = books.find(class_='breadcrumb').find_all('a')[2].text# p8  récupération de la cathégorie d'une liste retourné par find_all a la position 2
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
            'image_url': GLOBAL_CAT_URL + filter_img
            }

# fonction permettant de récuperer les images
def save_img(url, path, category_name):
    r = requests.get(url)
    os.makedirs('images', exist_ok=True)
    os.makedirs('images/'+ category_name, exist_ok=True)
    with open ('images/'+  category_name + '/' + path, 'wb') as img_file:# Je met en paramètre la création du dossier "images" en concaténant la variable category_name ainsi que le slash pour la création des sous dossier
        img_file.write(r.content)
            

# fonction qui récupère les différentes catégories
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
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    for books in soup.find_all('article', class_='product_pod'):
        books_link_url = books.find('a', href = True)
        books_url = books_link_url.get('href').strip('../../../')
        links.append(GLOBAL_CAT_URL + 'catalogue/' + books_url)
    next = soup.find('li', class_='next')
    if next is not None:
        # destructuration de l'url category_url du dernier element "index.html"
        next_page = url.split('/')[0 : -1]
        # ajout de l'element ciblé sur la nouvelle url "page-2.html"
        next_page.append(next.find('a').get('href'))
        # restructuration de l'url avec le nouvel element
        next_page_url = '/'.join(next_page)
        links.extend(get_books_data(next_page_url))
    return links


        
# Code d'execution du programme qui collecte les images ainsi que les categories au format csv du site en les stockants dans des dossiers spécifiques.
for category_name,category_url in get_categories().items():
    os.makedirs('data_csv', exist_ok=True)
    with open('data_csv/' + category_name + '.csv', 'w', encoding='utf-8') as csvfile:
        fieldnames = ['product_page_url', 'upc', 'title', 'price_including_tax', 'price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating', 'image_url']
        wr = csv.DictWriter(csvfile, fieldnames=fieldnames)
        wr.writeheader()
        for url in get_books_data(category_url):# je boucle sur les différentes fonctions en les appellants
            book_info = book_data(url)
            wr.writerow(book_info)
            save_img(url = book_info['image_url'], path = book_info['upc'] + '.jpg', category_name = book_info['category'])# J'affecte les paramètress de la fonction a une variable qui récupère les clés du dictionaire de la fonction " book_data " qui renvois les info d'un livre
            

