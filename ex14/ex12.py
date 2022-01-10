"""
Author: Medis Redzic
Matr.Nr.: K11934616
Exercise: Exercise 12
"""
import os


def get_hamsters(folderpath: str):

    rel_files = []

    for directory, _, files in os.walk(folderpath):
        for file in files:
            if file.endswith('.gene.dat'):
                rel_files.append(os.path.join(directory, file))

    rel_files = sorted(rel_files)

    for n in range(len(rel_files)):
        f = open(rel_files[n])
        yield n, len(rel_files), os.path.basename(rel_files[n]), f.read()