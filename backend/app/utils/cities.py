import csv
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(current_dir, 'data', 'inseecode_postalcode_bycity.csv')

postalcodeByCity = dict()
inseecodeByCity = dict()
with open(csv_path) as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=';')
    for row in csv_reader:
            inseecodeByCity[row["Commune"].lower()] = row["Code INSEE"]
            postalcodeByCity[row["Commune"].lower()] = row["Code Postal"]