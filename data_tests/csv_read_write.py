import csv
import numpy as np

#with is equivelent to try-catch statement in java
with open('data.txt', 'r', newline='') as read_file, open('data.csv', 'w', newline='') as write_file:
    reader = csv.reader(read_file, delimiter=',')
    writer = csv.writer(write_file)
    for row in reader:
        writer.writerow(row)

with open('randomData.csv', 'w', newline='') as file:
    writer = csv.writer(file, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
    for i in range(10):
        number = np.random.randint(1,11)
        writer.writerow([number])