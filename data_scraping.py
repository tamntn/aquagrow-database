import requests
import csv
from bs4 import BeautifulSoup

uf_homepage = 'https://www.ufseeds.com'
uf_urls = 'dataset/uf_urls.csv'
uf_data = 'dataset/uf_data.csv'

burpee_homepage = 'https://www.burpee.com'
burpee_urls = 'dataset/burpee_urls.csv'
burpee_data = 'dataset/burpee_data.csv'


# Create Urban Farmer Product URL File
# Add Header Row
with open(uf_urls, 'wb') as uf_urls_file:
    writer = csv.writer(uf_urls_file)
    headerRow = ['category', 'main', 'product', 'product_url']
    writer.writerow(headerRow)


# Add Product URL to file
def UrbanFarmerAddUrlToFile(category, main, product, product_url):
    row = [category, main, product, product_url]
    with open(uf_urls, 'a') as uf_urls_file:
        writer = csv.writer(uf_urls_file)
        writer.writerow(row)
        uf_urls_file.close()


# Scraping sub titles from each main titles
# From Urban Farmer
def UrbanFarmerGetProductUrl(category, title, titleURL):
    r = requests.get(titleURL)
    soup = BeautifulSoup(r.content, 'html.parser')
    try:
        main = soup.find("div", {"class": "shop-container"})
        descriptionDiv = main.find("div", {"class": "term-description"})
        productsDiv = main.find("div", {"class": "products"})
        productsText = main.findAll("div", {"class": "product-title"})
        for product in productsText:
            productName = product.find("a").get_text()
            productURL = 'https:' + product.find("a").get('href')
            print '|     |---' + productName
            UrbanFarmerAddUrlToFile(category, title, productName, productURL)
    except:
        print '|     |---Error: Failed'


# Scraping main titles from each categories
# From Urban Farmer
def UrbanFarmerGetTitleUrl(category, categoryURL):
    r = requests.get(categoryURL)
    soup = BeautifulSoup(r.content, 'html.parser')
    main = soup.find("div", {"class": "col-inner"})
    URLsWithoutPics = main.find("div", {"class": "medium-3"})
    URLsWithPics = main.find("div", {"class": "medium-9"}).findAll("div", {"class": "medium-4"})
    for urlDiv in URLsWithPics:
        titleURL = uf_homepage + urlDiv.find("a").get('href')
        picURL = 'https:' + urlDiv.find("img").get('src')
        title = urlDiv.find("p").get_text()
        print '|---' + title
        UrbanFarmerGetProductUrl(category, title, titleURL)


# Scraping all plants' URLs
# From Urban Farmer
def UrbanFarmerGetAllUrls(homepage):
    # Request Homepage
    r = requests.get(homepage)
    # Get homepage content
    soup = BeautifulSoup(r.content, 'html.parser')
    # Main Nav Bar
    nav = soup.find("ul", {"id":"ubermenu-nav-main-57-primary"})
    # Getting the main 4 categories from nav bar
    categories = nav.findAll("li", {"class": "ubermenu-item-level-0"})[0:4]
    categories_dict = {}

    # Get the URL of each main categories
    for li in categories:
        url = uf_homepage + li.find("a", {"class": "ubermenu-target"}).get('href')
        category = li.find("a", {"class": "ubermenu-target"}).get_text()
        categories_dict[category] = url

    for category in categories_dict:
        print 'Processing:', category, '...'
        UrbanFarmerGetTitleUrl(category, categories_dict[category])


# Getting a plant's information
# from an Urban Farmer URL
def UrbanFarmerGetPlantData(url):
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
def BurpeeGetPlantData(url):
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


UrbanFarmerGetAllUrls(uf_homepage)
# UrbanFarmerGetPlantData('https://www.ufseeds.com/product/sweet-g90-corn-seed/')