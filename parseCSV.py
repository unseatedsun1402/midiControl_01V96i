from concurrent.futures import process
import csv
from os import RWF_NOWAIT

for row in (csv.reader('METER_DATA.cs',dialect='excel')):
    process(row)
    print(row)