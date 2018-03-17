import csv

original_file = "phm_us_zipcode.csv"
output_file = "zipcode_zone.csv"

zones = {
    '1A': '-60 to -55',
    '1B': '-55 to -50',
    '2A': '-50 to -45',
    '2B': '-45 to -40',
    '3A': '-40 to -35',
    '3B': '-35 to -30',
    '4A': '-30 to -25',
    '4B': '-25 to -20',
    '5A': '-20 to -15',
    '5B': '-15 to -10',
    '6A': '-10 to -5',
    '6B': '-5 to 0',
    '7A': '0 to 5',
    '7B': '5 to 10',
    '8A': '10 to 15',
    '8B': '15 to 20',
    '9A': '20 to 25',
    '9B': '25 to 30',
    '10A': '30 to 35',
    '10B': '35 to 40',
    '11A': '40 to 45',
    '11B': '45 to 50',
}

with open(output_file, 'wb') as output:
    writer = csv.writer(output)
    headerRow = ['zipcode', 'zone', 'range']
    writer.writerow(headerRow)
    with open(original_file, 'rb') as input:
        reader = csv.reader(input)
        header = reader.next()
        rows = [row for row in reader if row]
        print len(rows)
        for row in rows:
            zipcode = row[0]
            zone = row[1]
            range = row[2]
            output_row = [zipcode, zone, range]
            writer.writerow(output_row)
            
        input.close()
    output.close()