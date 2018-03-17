import requests
from bs4 import BeautifulSoup

uf_homepage = 'https://www.ufseeds.com'
burpee_homepage = 'https://www.burpee.com'

# Getting a plant's information
# from an Urban Farmer URL
def getPlantDataFromUF(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    title = soup.find("h1", {"class": "product-title"}).get_text().strip()
    data = soup.find("div", {"id": "tab-additional_information"})
    rows = data.findAll("tr")
    for row in rows:
        th = row.find('th').get_text().strip()
        td = row.find('td').get_text().strip()
        print th, ": ", td


# Getting a plant's information
# from a Burpee URL
def getPlantDataFromBurpee(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    title = soup.find("h1", {"class": "b-product_name"}).get_text().strip()
    # data = soup.find("section", {"class": "b-product_properties"})
    details = soup.find("div", {"class": "b-product_details"})
    rows = details.findAll("div", {"class": "b-product_attribute"})
    for row in rows:
        category = row.find("div", {"class": "b-product_attribute-title"}).get_text().strip()
        description = row.find("div", {"class": "b-product_attribute-description"}).get_text().strip()
        print category, ": ", description


getPlantDataFromUF('https://www.ufseeds.com/product/bouquet-dill-seeds/')
getPlantDataFromBurpee('https://www.burpee.com/herbs/dill/dill-mammoth-prod000472.html')