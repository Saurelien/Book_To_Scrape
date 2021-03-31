from bs4 import BeautifulSoup
import requests
import csv
# declarer la variable avec url pour le scrape
base_url = 'https://books.toscrape.com'
base_url2 = 'https://books.toscrape.com/catalogue/finders-keepers-bill-hodges-trilogy-2_807/index.html'
category_url = 'https://books.toscrape.com/catalogue/category/books/fiction_10/index.html'

def get_categories():
    
    # variable + methode pour la liaison entre le client et le site internet
    response = requests.get(base_url)
    # variable + methodepour recuperer les données
    html_soup = BeautifulSoup(response.content, 'html.parser')
    # definir une variable en appellant la variable pour craper et l'utiliser dans une boucle
    get_categories = html_soup.find_all('div', class_='side_categories')
    for category in get_categories:
        for category in category.find_all('a', href = True):
            category = category.text.strip() # afficher les données récupéré en utilisant une méthode qui récurpère uniquement le texte du lien "href" et de couper les espaces inutiles " .strip "
            return {'Categories': category}
        
get_categories()




def get_books(category_url):
    
    response = requests.get(category_url)
    cat_soup = BeautifulSoup(response.content, 'html.parser')
    get_books = cat_soup.find_all(class_='default')
    
    data = ['https://books.toscrape.com/catalogue/category/books/fiction_10/index.html',
            'https://books.toscrape.com/catalogue/category/books/fiction_10/page-2.html',
            'https://books.toscrape.com/catalogue/category/books/fiction_10/page-3.html',
            'https://books.toscrape.com/catalogue/category/books/fiction_10/page-4.html']
    
    for get_books_data in get_books :
        for get_books_data in get_books_data.find_all('h3'):
            books_link = get_books_data.find(href= True)
            prices = get_books_data.find('div', class_='product_price')
            images = get_books_data.find('a', href = True).find_next('img', class_='thumbnail')
            print(images.get('src').strip('../../../../'))
            print(prices)
            print(books_link.get('href').strip('../../../'))
            print(get_books_data.text.lower().strip('...'))
            
    next = True
    if next is True:
        
        next_btn = get_books_data.find('a', class_='next')
        print(next_btn)
        data2 = get_books(category_url + 'page=4')
        data.extend(data2)
        
    #return {}
get_books(category_url)

def get_book_data(base_url2):
    # p1 recuperation url de la page produit
    response = requests.get(base_url2)
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
        
        return {'product_page_url': base_url2,
            'upc': upc,
            'title': title,
            'price_including_tax': price_include,
            'price_excluding_tax':price_exclude,
            'number_available': availability,
            'product_description':description,
            'category':category,
            'review_rating':review,
            'image_url':filter_img
            }


for category_url in get_categories():
    with open('categories.csv', 'w') as csvfile:
        for book_url in get_books(category_url):
            data = get_book_data(book_url)
            fieldnames = ['movie_categories', 'image_url', 'book_url']
            wr = csv.DictWriter(csvfile, fieldnames = fieldnames)
            wr.writeheader()
            wr.writerows(category_url)
         #Récupération de l'image



