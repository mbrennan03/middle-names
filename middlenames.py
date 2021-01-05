import random
import re
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup


def simple_get(url):
    # attempt to get html or xml content at the url

    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None
    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    # returns true if response is html

    content_type = resp.headers['Content-type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


def log_error(e):
    print(e)


nouns = {}

# make a list of all chemical elements
elements = []
raw_element_html = simple_get('https://en.wikipedia.org/wiki/List_of_chemical_elements')
element_html = BeautifulSoup(raw_element_html, 'html.parser')
element_table = element_html.find_all('table', class_='wikitable')[0]

for row in element_table.findAll('tr'):
    element_info = row.findAll('td')

    if len(element_info) > 2:
        element_name = element_info[2].text
        elements.append(element_name)

nouns['elements'] = elements


# make a list of all animal names
animals = []
raw_animal_html = simple_get('https://en.wikipedia.org/wiki/List_of_animal_names')
animal_html = BeautifulSoup(raw_animal_html, 'html.parser')
animal_table = animal_html.find_all('table', class_='wikitable')[1]

for row in animal_table.findAll('tr'):
    animal_info = row.findAll('td')
    if len(animal_info) > 0:
        animal_name = animal_info[0].text

        # only take one word animal names and those without tilde
        if ' ' not in animal_name and '\u00f1' not in animal_name:
            animal_name = re.split(r'[(\[,/]', animal_name)[0]
            animal_name = animal_name.strip('\n')
            animal_name = animal_name.strip('\xa0')
            animal_name = animal_name.rstrip()
            animals.append(animal_name)

nouns['animals'] = animals


# make a list of all plant names
plants = []
raw_plant_html = simple_get('https://en.wikipedia.org/wiki/List_of_plants_by_common_name')
plant_html = BeautifulSoup(raw_plant_html, 'html.parser')

# some plant names are in ordered lists and some in unordered
plant_tags = ['ol', 'ul']


def generate_plant_names(list_tag):
    for ultag in plant_html.find_all(list_tag):

        for litag in ultag.find_all('li'):
            plant = litag.contents[0]

            # for plant names that aren't embedded links
            if isinstance(plant, str):
                # get rid of en-dashes
                plant_name = re.sub(u'\u2013', '', plant).rstrip()
                # remove plant names longer than one word and blank strings
                if ' ' not in plant_name and '-' not in plant_name and (len(plant_name) > 2):
                    plants.append(plant_name)

            # for plant names that are embedded links
            else:
                plant_name = plant.text
                if len(plant_name) > 2 and ' ' not in plant_name and '-' not in plant_name:
                    if plant_name != 'Top' and plant_name != '0\u20139':
                        plants.append(plant_name)


for plant_tag in plant_tags:
    generate_plant_names(plant_tag)

# remove everything after Zedoary
plants_end = plants.index('Zedoary')
plants = plants[:plants_end+1]

nouns['plants'] = plants

print(nouns)
