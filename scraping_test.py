from bs4 import BeautifulSoup
import requests
import csv
# declarer la variable avec url pour le scrape


def get_categories_data(base_url):
    
    # variable + methode pour la liaison entre le client et le site internet
    response = requests.get(base_url)
    # variable + methodepour recuperer les données
    html_soup = BeautifulSoup(response.content, 'html.parser')
    # definir une variable en appellant la variable pour craper et l'utiliser dans une boucle
    get_categories = html_soup.find_all('div', class_='side_categories')
    for category in get_categories:
        for category in category.find_all('a', href = True):
            category = category.text.strip() # afficher les données récupéré en utilisant une méthode qui récurpère uniquement le texte du lien "href" et de couper les espaces inutiles " .strip "
            print(category)
            return {'movie_categories': category}

def cat_csv():
    base_url = 'https://books.toscrape.com'
    response = requests.get('https://books.toscrape.com')
    html_soup = BeautifulSoup(response.content, 'html.parser')
    get_categories = html_soup.find_all('div', class_='side_categories')
    with open('categories.csv', 'w') as csvfile:
        for category in get_categories:
            for category in category.find_all('a', href = True):
                fieldnames = ['movie_categories']
                wr = csv.DictWriter(csvfile, fieldnames=fieldnames)
                wr.writeheader()
                wr.writerow(get_categories_data(base_url))
cat_csv()

