import csv

with open('METER_DATA.csv','r')as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for line in csv_reader:
        print(line)