import requests
import csv
import pprint
from bs4 import BeautifulSoup

uf_homepage = 'https://www.ufseeds.com'
uf_urls = 'dataset/uf_urls.csv'
uf_data = 'dataset/uf_data.csv'

burpee_homepage = 'https://www.burpee.com'
burpee_urls = 'dataset/burpee_urls.csv'
burpee_data = 'dataset/burpee_data.csv'


# Add Product URL to file
def UrbanFarmerAddUrlToFile(category, main, main_url, main_pic, product, product_url):
    row = [category, main, main_url, main_pic, product, product_url]
    with open(uf_urls, 'a') as uf_urls_file:
        writer = csv.writer(uf_urls_file)
        writer.writerow(row)
        uf_urls_file.close()


# Scraping sub titles from each main titles
# From Urban Farmer
def UrbanFarmerGetProductUrl(category, mainName, mainURL):
    r = requests.get(mainURL)
    soup = BeautifulSoup(r.content, 'html.parser')
    try:
        main = soup.find("div", {"class": "shop-container"})
        descriptionDiv = main.find("div", {"class": "term-description"})
        try:
            mainPic = 'https:' + descriptionDiv.find("img").get('src')
        except:
            mainPic = 'N/A'
        productsDiv = main.find("div", {"class": "products"})
        productsText = main.findAll("div", {"class": "product-title"})
        for product in productsText:
            productName = product.find("a").get_text()
            productURL = 'https:' + product.find("a").get('href')
            print '|     |---' + productName
            UrbanFarmerAddUrlToFile(category, mainName, mainURL, mainPic, productName, productURL)
    except Exception as e:
        print '|     |---Error:', e


# Scraping main titles from each categories
# From Urban Farmer
def UrbanFarmerGetMainUrl(category, categoryURL):
    r = requests.get(categoryURL)
    soup = BeautifulSoup(r.content, 'html.parser')
    main = soup.find("div", {"class": "col-inner"})
    URLsWithoutPics = main.find("div", {"class": "medium-3"}).findAll("li")
    URLsWithPics = main.find("div", {"class": "medium-9"}).findAll("div", {"class": "medium-4"})
    # Get Main URLs from The Div With Pictures (Not All Items)
    # for urlDiv in URLsWithPics:
    #     mainURL = uf_homepage + urlDiv.find("a").get('href')
    #     picURL = 'https:' + urlDiv.find("img").get('src')
    #     title = urlDiv.find("p").get_text()
    #     print '|---' + title
    #     UrbanFarmerGetProductUrl(category, title, mainURL)

    # Get URLs from The Sidebar ( All Items)
    for urlDiv in URLsWithoutPics:
        try:
            mainURL = uf_homepage + urlDiv.find("a").get('href')
            title = urlDiv.find("a").get_text()
            print '|---' + title
            UrbanFarmerGetProductUrl(category, title, mainURL)
        except:
            print '|---Error: No Available URL'


# Scraping all plants' URLs
# From Urban Farmer
def UrbanFarmerGetAllUrls(homepage):
    # Create Urban Farmer Product URL File
    # Add Header Row
    with open(uf_urls, 'wb') as uf_urls_file:
        writer = csv.writer(uf_urls_file)
        headerRow = ['category', 'main', 'main_url', 'main_pic', 'product', 'product_url']
        writer.writerow(headerRow)


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
        print 'Processing:', category, '.......'
        UrbanFarmerGetMainUrl(category, categories_dict[category])


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


# Get all plants information
# From Urban Farmers list of URLs
def UrbanFarmer():
    uf_data_output = {}
    with open(uf_urls, 'rb') as uf_urls_file:
        reader = csv.reader(uf_urls_file)
        header = reader.next()
        rows = [row for row in reader if row]
        for row in rows:
            category = row[0]
            main = row[1]
            main_url = row[2]
            main_pic = row[3]
            product = row[4]
            product_url = row[5]
            if (category in uf_data_output):
                uf_data_output[category].append([{
                    "main": main,
                    "main_url": main_url
                }])
            else:
                uf_data_output[category] = [{
                    "main": main,
                    "main_url": main_url
                }]
                
    pprint.pprint(uf_data_output)


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


# UrbanFarmer()
UrbanFarmerGetAllUrls(uf_homepage)

# Processing Sprouts (Main) Separately Because of Urban Farmer's Site Error
UrbanFarmerGetProductUrl('Vegetables', 'Sprouts', 'https://www.ufseeds.com/product-category/vegetables/sprout-seed/')

# UrbanFarmerGetPlantData('https://www.ufseeds.com/product/sweet-g90-corn-seed/')