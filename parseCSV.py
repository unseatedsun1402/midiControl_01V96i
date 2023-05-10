import csv

with open('meterValues.csv','r')as csv_file:
    csv_reader = csv.DictReader(csv_file,delimiter=',')
    for line in csv_reader:
        print(line)