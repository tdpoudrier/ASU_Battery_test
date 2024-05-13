"""
Read and write practice for csv files
"""

import csv
import numpy as np

#with releases all resources when complete
#Read data from one csv file and copy it to a new csv
with open('data.txt', 'r', newline='') as read_file, open('data.csv', 'w', newline='') as write_file:
    reader = csv.reader(read_file, delimiter=',')
    writer = csv.writer(write_file)
    for row in reader:
        writer.writerow(row)

#Create a csv with 10 random numbers in the range 1-10
with open('randomData.csv', 'w', newline='') as file:
    writer = csv.writer(file, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
    for i in range(10):
        number = np.random.randint(1,11) # 1 inclusive, 11 exlusive
        writer.writerow([number])