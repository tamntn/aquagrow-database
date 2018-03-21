import csv

ph_raw_text_file = 'dataset/pH_level_raw.txt'
ph_clean_text_file = 'dataset/ph_level_clean.txt'
ph_clean_csv_file = 'dataset/ph_level_clean.csv'

with open(ph_clean_text_file, 'wb') as clean_text_file:
    with open(ph_raw_text_file, 'rb') as raw_text_file:
        count = 1
        for line in raw_text_file.readlines():
            # If line number is odd, edit the plant name
            if count % 2 == 1:
                line = line.strip().title()
            # If line number if even, edit the pH level
            elif count % 2 == 0:
                line = line.replace(',', '.').replace(' ','').strip()
            # Increment line number
            count += 1
            # Write processed line to clean file
            clean_text_file.write(line + '\n')


with open(ph_clean_csv_file, 'wb') as clean_csv_file:
    writer = csv.writer(clean_csv_file)
    header = ['name', 'ph_range']
    writer.writerow(header)
    with open(ph_clean_text_file, 'rb') as clean_text_file:
        lines = clean_text_file.readlines()
        for i in range(0, len(lines), 2):
            name = lines[i].strip()
            level = lines[i+1].strip()
            row = [name, level]
            writer.writerow(row)