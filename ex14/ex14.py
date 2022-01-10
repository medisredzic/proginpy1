"""
Author: Medis Redzic
Matr.Nr.: K11934616
Exercise: Exercise 14
"""

import argparse
import numpy as np

from ex11 import count_bases_and_subsequence
from ex12 import get_hamsters
from ex13 import get_file_metadata

parser = argparse.ArgumentParser()

parser.add_argument('input_folder', help='Folder containing input files', type=str)
parser.add_argument('output_file', help='File to print output to', type=str)
parser.add_argument('subsequence', help='Subsequence to search for', type=str)

args = parser.parse_args()

generator = get_hamsters(folderpath=args.input_folder)

count = np.zeros(shape=(180, 5), dtype=np.float64)

for i, _, pathname, content in generator:
    print(f"[{i+1}/2700] Processing '{pathname}'")
    hamster, date, _ = get_file_metadata(content)
    count_sub, count_base = count_bases_and_subsequence(content, args.subsequence)

    count[date, 0] += count_base['a'] / 15
    count[date, 1] += count_base['c'] / 15
    count[date, 2] += count_base['g'] / 15
    count[date, 3] += count_base['t'] / 15
    count[date, 4] += count_sub / 15

with open(args.output_file, 'w') as file:
    file.write('subsequence,a,c,g,t\n')

    for n in range(len(count)):
        file.write(f'{count[n, 4]},{count[n, 0]},{count[n, 1]},{count[n, 2]},{count[n, 3]}\n')
