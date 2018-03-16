import requests
from bs4 import BeautifulSoup

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

def getPlantDataFromBurpee(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    title = soup.find("h1", {"class": "b-product_name"}).get_text().strip()
    print title

# getPlantDataFromUF('https://www.ufseeds.com/product/bouquet-dill-seeds/')
getPlantDataFromBurpee('https://www.burpee.com/herbs/dill/dill-mammoth-prod000472.html')
