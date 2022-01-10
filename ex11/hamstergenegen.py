# -*- coding: utf-8 -*-
"""hamstergenegen.py

Author -- Michael Widrich, Andreas Schörgenhumer
Contact -- schoergenhumer@ml.jku.at
Date -- 04.11.2021

###############################################################################

The following copyright statement applies to all code within this file.

Copyright statement:
This  material,  no  matter  whether  in  printed  or  electronic  form,
may  be  used  for personal  and non-commercial educational use only.
Any reproduction of this manuscript, no matter whether as a whole or in parts,
no matter whether in printed or in electronic form, requires explicit prior
acceptance of the authors.

###############################################################################

This file generates fictional gene data for Assignment 2 and writes it to a
file in the specified directory.

Arguments
-------------
dir : str
    Directory to place gene data in
"""
import os
import argparse
import itertools
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument("dir", help="directory to place gene data in (name must only contain digits)", type=str)
args = parser.parse_args()

output_dir = args.dir

output_folder = os.path.basename(output_dir)
if not os.path.exists(output_dir):
    raise ValueError(f"specified output directory does not exist: '{output_dir}'")
try:
    output_dir_int = int(output_folder)
except ValueError as exc:
    raise ValueError(f"specified output directory name must only contain digits: '{output_folder}'") from exc
rnd_gen = np.random.RandomState(seed=output_dir_int)

character_set = np.array(list("acgtn") + list("acgtn".upper()) + ['-', '_'])
annotation_set = list("hamsters") + list("hamsters".upper())
annotation_set = np.array([''.join(t) for t in itertools.combinations(annotation_set, r=3)]
                          + [''.join(t) for t in itertools.combinations(annotation_set, r=2)]
                          + list(annotation_set))

gene_length = 800
n_hamsters = 15
n_days = 180

gene_seq = rnd_gen.choice(character_set, size=(n_hamsters, gene_length))
gene_qs = rnd_gen.uniform(size=(n_hamsters, n_days, gene_length))
gene_annotations = rnd_gen.choice(annotation_set, size=(n_hamsters, n_days, gene_length))
post_data_end = rnd_gen.uniform(size=(n_hamsters, n_days))
random_whitespace = rnd_gen.uniform(size=(n_hamsters, n_days, gene_length))

print(f"Creating gene data for {n_hamsters} hamsters for {n_days} days. Please wait...")
for day in range(n_days):
    mutations = rnd_gen.randint(low=0, high=gene_length, size=(int(gene_length / 100),))
    gene_seq[:, mutations] = 'G'
    
    for hamster in range(n_hamsters):
        header = f"""% HEADER_START
% ID: {hamster}
% Date: {day}
% Columns: info;base;quality
% HEADER_END"""
        with open(os.path.join(output_dir, f'data_{hamster:02}-{day:03}.gene.dat'), 'w', newline='\n') as hf:
            print(header, file=hf)
            for i in range(len(gene_seq[hamster])):
                print(f"{gene_annotations[hamster, day, i]};"
                      f"{gene_seq[hamster, i]};"
                      f"{gene_qs[hamster, day, i]}", file=hf)
                if random_whitespace[hamster, day, i] < 0.01:
                    print(f"% Additional; annotation; here", file=hf)
            print("% DATA_END", file=hf)
            if post_data_end[hamster, day] < 0.1:
                for i in range(int(post_data_end[hamster, day] * 100)):
                    random_noise = rnd_gen.choice(annotation_set, 3)
                    print(f"{random_noise[0]};"
                          f"{random_noise[1]};"
                          f"{random_noise[2]}", file=hf)
print("Successfully created data")
