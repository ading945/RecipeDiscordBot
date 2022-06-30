import json
import requests

from bs4 import BeautifulSoup

headers = {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"}


class JamieOliverRecipe:

  def __init__(self, url):
    self.url = url 
    self.soup = BeautifulSoup(requests.get(url, headers=headers).content, 'html.parser')

  def recipe_name(self):
    """ Locates the recipe title """
    # Some of the urls are not recipe urls so to avoid errors we use try/except 
    try:
      return self.soup.find('h1').text.strip()
      # return self.soup.select('ht.hidden-xs')[0].text.strip()
    except: 
      return None
          
  def serves(self):
    """ Locates the number of people the meal serves """
    try:
      return self.soup.find('div', {'class': 'recipe-detail serves'}).text.split(' ',1)[1]
    except:
      return None 

  def cooking_time(self):
    """ Locates the cooking time (in mins or hours and mins) """
    try:
      return self.soup.find('div', {'class': 'recipe-detail time'}).text.split('In')[1]
    except:
      return None


  def difficulty(self):
    """ Locates the cooking difficulty """
    try:
      return self.soup.find('div', {'class': 'col-md-12 recipe-details-col remove-left-col-padding-md'}).text.split('Difficulty')[1]
    except:
      return None

  def ingredients(self):
    """ Creating a list containing the ingredients of the recipe """
    try:
      ingredients = [] 
      for li in self.soup.select('.ingred-list li'):
        ingred = " ".join(li.text.split())
        ingredients.append(ingred)
      return ingredients
    except:
      return None

def jamie_oliver_get_urls():
  url = "https://www.jamieoliver.com/recipes/category/course/mains/"
  
  # Fetching html from the website
  page = requests.get(url)
  # BeautifulSoup enables to find the elements/tags in a webpage 
  soup = BeautifulSoup(page.text, "html.parser")
  
  links = []
  for link in soup.find_all('a'):
    href = link.get('href')
    #make sure that that the link is a recipe, essestially sorting the URls
    if "/recipes/" in href and "-recipes/" in href and "course" not in href\
    and "books" not in href and href.endswith("recipes/") == False:
      if "https://www.jamieoliver.com" not in href:
        links.append("https://www.jamieoliver.com" + href)
      else:
        links.append(href)
  
  return links
    
def write_data_file():
  urls = jamie_oliver_get_urls() 
  recipes = []
  for url in urls:
    recipe = JamieOliverRecipe(url) 
    if recipe.ingredients is not None:
        try:
          recipe_dict = {
            "link": url,
            "recipe_name": recipe.recipe_name(),
            "serves": recipe.serves().strip(),
            "cooking_time": recipe.cooking_time().strip(),
            "difficulty": recipe.difficulty().strip(),
            "ingredients": recipe.ingredients()  
          }
          recipes.append(recipe_dict)
        except:
          print("No data")
  with open("JamieOliver.txt", "a") as fh:
    json.dump(recipes, fh, indent = 2)

