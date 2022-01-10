"""
Author: Medis Redzic
Matr.Nr.: K11934616
Exercise: Exercise 15
"""

import argparse
import os
import sys
import subprocess
from plot_csv import plot_csv

parser = argparse.ArgumentParser()
parser.add_argument('output_folder', type=str)
args = parser.parse_args()

output_folder = args.output_folder
folder_path = f'{output_folder}/125'

try:
    os.makedirs(folder_path)
except FileExistsError:
    print(folder_path)
    pass
finally:
    subprocess.call([sys.executable, "hamstergenegen.py", folder_path])
    subprocess.call([sys.executable, "ex14.py", folder_path, f'{output_folder}/patterns_analysis.csv', 'acag'])
    plot_csv(output_folder + '/patterns_analysis.csv', output_folder + '/patterns_analysis')