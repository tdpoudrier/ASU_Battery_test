"""
Create a unique file to avoid appending to previous test data
"""
from pathlib import Path

string = "ASU_Battery_test_0.csv"
count = 0

my_file = Path(string)

while my_file.is_file():
    # file exists
    index1 = string.rfind('_')
    index2 = string.rfind('.')
    string = string[:index1 + 1] + str(count) + string[index2:]
    my_file = Path(string)
    count = count + 1

open(string, 'x', newline = '')

print("filename:" + string)