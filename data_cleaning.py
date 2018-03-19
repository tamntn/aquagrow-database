import json
import csv
import pprint

uf_data_file = 'dataset/uf_data_raw.json'
uf_data_clean_file = 'dataset/uf_data_clean.json'

productKeys = []
productKeysToBeRemoved = ['Size', 'Form', 'Dimensions', 'Weight', 'Packet', 'categories', 'types', 'Sow per 1,000 Sq. Ft.',
                          'Garlic Hardneck Type', 'Broadcast Rate per Acre', 'Best Time to Sow', 'Sub Type', 'Corn Use',
                          'Ear Length', 'Color', 'Beet Shape', 'Resistance', 'Fruit Weight', 'Tomato Leaf Type', 'Seed Count',
                          'Vine', 'Shape', 'Fruit Length', 'Uses', 'Yield', 'Corn Seed Type', 'Seeds Per Pound',
                          'Bean Seed Color', 'Cubic Inches', 'Seeds Per Gram', 'Seeds Per Ounce', 'Asparagus']


# Remove unnecessary product fields
# From Urban Farmer scraped data
def deleteUnecessaryProductFiels():
    with open(uf_data_clean_file, 'wb') as output_file:
        with open(uf_data_file, 'rb') as input_file:
            data = json.load(input_file)
            for category in data:
                mains = data[category]
                for main in mains:
                    products = main['products']
                    for product in products:
                        for key in productKeysToBeRemoved:
                            product.pop(key, None)

            json.dump(data, output_file)
            input_file.close()
        output_file.close()


# Get a list of all product properties
# From Urban Farmer scraped data file
def getListOfAllProductProperties():
    with open(uf_data_clean_file, 'rb') as input_file:
        data = json.load(input_file)
        for category in data:
            mains = data[category]
            for main in mains:
                products = main['products']
                for product in products:
                    for key in product:
                        if key not in productKeys:
                            productKeys.append(key)


deleteUnecessaryProductFiels()
getListOfAllProductProperties()
pprint.pprint(productKeys)
print(len(productKeys))
