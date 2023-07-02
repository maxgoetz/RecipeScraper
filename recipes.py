from bs4 import BeautifulSoup
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scopes = [
'https://www.googleapis.com/auth/spreadsheets',
'https://www.googleapis.com/auth/drive'
]

credentials = ServiceAccountCredentials.from_json_keyfile_name("C:\\Users\\13366\\Downloads\\Summer Projects\\RecipeScraper\\secret_key.json", scopes)
file = gspread.authorize(credentials)
workbook = file.open("Recipes")
sheet = workbook.sheet1

def findRecipes():
    html_text = requests.get("https://www.bbcgoodfood.com/recipes/collection/vegetarian-dinner-recipes").text
    soup = BeautifulSoup(html_text, 'lxml')
    recipes = soup.find_all('li', class_ = "dynamic-list__list-item list-item")
    for recipe in recipes:
        name = recipe.find('h2', 'heading-4').text
        partial_link = recipe.find("a", "link d-block")['href']
        link = f"http://www.bbcgoodfood.com{partial_link}"
        checkProtein(link, name)


def checkProtein(link, name):
    recipe_html = requests.get(link).text
    soup_jr = BeautifulSoup(recipe_html, 'lxml')
    description = soup_jr.find('div', 'editor-content mt-sm pr-xxs hidden-print').text
    nut_facts_table = soup_jr.find("table", "key-value-blocks hidden-print mt-xxs")
    for index, row in enumerate(nut_facts_table.find_all('tr')):
        if index == 1:
            cals = row.find('td', 'key-value-blocks__value').text
        if index == 7:
            protein = row.find('td', 'key-value-blocks__value').text
            break
    protein = protein[:-1]
    ratio = int(cals) / int(protein)
    if (ratio < 20):
        updateSheet(name, description, cals, protein, ratio, link)


def updateSheet(name, description, cals, protein, ratio, link):
    body = [name, description, cals, protein, ratio, link]
    sheet.append_row(body, table_range="A1:F1") 


if __name__ == '__main__':
    findRecipes()