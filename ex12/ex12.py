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

if __name__ == "__main__":
    folderpath = "ex12_testfiles\\test3"
    file_reader = get_hamsters(folderpath=folderpath)
    # This should print the name and length of each file content for all sorted files:
    for i, nfiles, filename, file_content in file_reader:
        # file_content should be the content of a file as string
        print(f"[{i + 1}/{nfiles}] {filename}: {len(file_content)}")