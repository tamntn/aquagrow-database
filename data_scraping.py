from __future__ import print_function
import requests
import csv
import json
import pprint
import sys
import time
from bs4 import BeautifulSoup

uf_homepage = 'https://www.ufseeds.com'
uf_urls = 'dataset/uf_urls.csv'
uf_data = 'dataset/uf_data.json'

burpee_homepage = 'https://www.burpee.com'
burpee_urls = 'dataset/burpee_urls.csv'
burpee_data = 'dataset/burpee_data.json'


# Getting a plant's information
# from an Urban Farmer URL
def UrbanFarmerGetPlantData(product, product_url):
    productDetails = {
        "product": product,
        "product_url": product_url
    }
    try:
        r = requests.get(product_url)
        soup = BeautifulSoup(r.content, 'html.parser')
        title = soup.find("h1", {"class": "product-title"}).get_text().strip()
        data = soup.find("div", {"id": "tab-additional_information"})
        rows = data.findAll("tr")
        for row in rows:
            th = row.find('th').get_text().strip()
            td = row.find('td').get_text().strip()
            productDetails[th] = td
        return productDetails
    except:
        return "Error"


# Get all plants information
# From Urban Farmers list of URLs
def UrbanFarmerGetAllPlantsData():
    uf_data_output = {}
    with open(uf_urls, 'rb') as uf_urls_file:
        reader = csv.reader(uf_urls_file)
        header = reader.next()
        rows = [row for row in reader if row]
        count = 1
        error = 0
        for row in rows:
            category = row[0]
            main = row[1]
            main_url = row[2]
            main_pic = row[3]
            product = row[4]
            product_url = row[5]
            product_details = UrbanFarmerGetPlantData(product, product_url)
            if product_details == "Error":
                error += 1
            else:
                if (category in uf_data_output):
                    if not any(main_item.get("main", None) == main for main_item in uf_data_output[category]):
                        uf_data_output[category].append({
                            "main": main,
                            "main_url": main_url,
                            "main_pic": main_pic,
                            "products": [product_details]
                        })
                    else:
                        for main_item in uf_data_output[category]:
                            if main_item["main"] == main:
                                main_item["products"].append(product_details)
                else:
                    uf_data_output[category] = [{
                        "main": main,
                        "main_url": main_url,
                        "main_pic": main_pic,
                        "products": [product_details]
                    }]

            time.sleep(0.03) # Wait 300 Miliseconds to Execute Next URL
            status = "\rProcessed " + str(count) + "/" + str(len(rows)) + " - Error: " + str(error)
            sys.stdout.write(status)
            sys.stdout.flush()
            count += 1
            
    with open(uf_data, 'wb') as output_file:
        json.dump(uf_data_output, output_file)
        output_file.close()

    print("\nFinished!")


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
        category = row.find(
            "div", {"class": "b-product_attribute-title"}).get_text().strip()
        description = row.find(
            "div", {"class": "b-product_attribute-description"}).get_text().strip()
        print(category, ": ", description)


UrbanFarmerGetAllPlantsData()
# UrbanFarmerGetPlantData('Sweetg90', 'https://www.ufseeds.com/product/sweet-g90-corn-seed/')
