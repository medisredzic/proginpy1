"""
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
"""

import hashlib
import os
import types
from glob import glob


def print_outs(outs, line_token="-"):
    print(line_token * 40)
    print(outs, end="" if isinstance(outs, str) and outs.endswith("\n") else "\n")
    print(line_token * 40)


ex_file = "ex12.py"
full_points = 2.5
points = full_points

directories = sorted(glob(os.path.join("ex12_testfiles", "*")))
if not len(directories):
    raise FileNotFoundError("Could not find files in directory 'ex12_testfiles'")
if len(directories) != 4:
    raise FileNotFoundError(f"Expected 4 folders in 'ex12_testfiles', found {len(directories)}")

inputs = directories

correct_outs = [(list(range(8)), [8] * 8,
                 ['correct_0.gene.dat', 'correct_1.gene.dat', 'correct_2.gene.dat', 'correct_3.gene.dat',
                  'correct_4.gene.dat', 'correct_5.gene.dat', 'correct_6.gene.dat', 'correct_7.gene.dat'],
                 '9693a68544c8fd4e19843e7c27a825d0'),
                (list(range(7)), [7] * 7,
                 ['correct_0.gene.dat', 'correct_1.gene.dat', 'correct_2.gene.dat', 'correct_3.gene.dat',
                  'correct_4.gene.dat', 'correct_5.gene.dat', 'correct_6.gene.dat'],
                 '8d22dfcd40d97012c165baf4ed8fe9fa'),
                ([], [],
                 [],
                 'd41d8cd98f00b204e9800998ecf8427e'),
                (list(range(12)), [12] * 12,
                 ['correct_in_a_subfolder.gene.dat', 'correct_0.gene.dat', 'correct_1.gene.dat', 'correct_2.gene.dat',
                  'correct_3.gene.dat', 'correct_4.gene.dat', 'correct_5.gene.dat', 'correct_6.gene.dat',
                  'correct_7.gene.dat', 'correct_8.gene.dat', 'correct_9.gene.dat', 'correct_10.gene.dat'],
                 '555ad62ac832beb8c1a79038da564b59')]

print(f"Unittest for: {ex_file}")

for test_i, test_params in enumerate(zip(inputs, correct_outs)):
    directory, solution = test_params
    correct_i_s = solution[0]
    correct_nfiles_s = solution[1]
    correct_filepaths = solution[2]
    correct_checksum = solution[3]
    i_s = None
    nfiles_s = None
    filepaths = None
    checksum = None

    try:
        from ex12 import get_hamsters
        generator = get_hamsters(folderpath=directory)
        errs = ""
        if not isinstance(generator, types.GeneratorType):
            points -= full_points / len(inputs)
            raise TypeError(f"not a generator object but {type(generator)} object")
        else:
            generator = list(generator)
            if not len(generator):
                i_s, nfiles_s, filepaths, filecontents = [], [], [], []
            else:
                i_s, nfiles_s, filepaths, filecontents = zip(*[(fi, fn, fp, fc) for fi, fn, fp, fc in generator])
                i_s = list(i_s)
                nfiles_s = list(nfiles_s)
                filepaths = list(filepaths)
            # Checking indexes
            if i_s != correct_i_s:
                points -= full_points / len(inputs) / 4
            # Checking total number of files
            if nfiles_s != correct_nfiles_s:
                points -= full_points / len(inputs) / 4
            # Checking file content (use a checksum instead of the actual (huge) file content)
            checksum = hashlib.md5()
            _ = [checksum.update(bytes(c, "utf-8")) for c in filecontents]
            checksum = checksum.hexdigest()
            if checksum != correct_checksum:
                points -= full_points / len(inputs) / 4
            # Checking filepaths
            if any([rfp != cfp for rfp, cfp in zip(filepaths, correct_filepaths)]):
                points -= full_points / len(inputs) / 4
    except Exception as e:
        errs = e
        points -= full_points / len(inputs)
    
    print()
    print_outs(f"Test {test_i}", line_token="#")
    print("Input was:")
    print_outs(f"folderpath = '{directory}'")

    if errs:
        print(f"Some unexpected errors occurred:")
        print_outs(f"{type(errs).__name__}: {errs}")
    else:
        outs = "\n".join([str(x) for x in zip(i_s, nfiles_s, filepaths,
                                              [f"<content of '{f}'>" for f in filepaths])])
        correct_outs = "\n".join([str(x) for x in zip(correct_i_s, correct_nfiles_s, correct_filepaths,
                                                      [f"<content of '{f}'>" for f in correct_filepaths])])
        # Must check checksum manually since it is not part of the actual output
        if outs == correct_outs and checksum == correct_checksum:
            print(f"The output was correct and was:")
            print_outs(outs)
        else:
            print("Unexpected output:")
            print_outs(outs)
            print("Output should be:")
            if checksum != correct_checksum:
                print_outs(f"{correct_outs}\n---> The file contents do not match.")
            else:
                print_outs(correct_outs)

    # due to floating point calculations it could happen that we get -0 here
    if points < 0:
        assert abs(points) < 1e-7, f"points were {points} < 0: error when subtracting points?"
        points = abs(points)
    print(f"Current points: {points:.2f}")

print(f"\nEstimated points upon submission: {points:.2f} (out of {full_points:.2f})")
print(f"This is only an estimate, see 'Instructions for submitting homework' in Moodle "
      f"for common mistakes that can still lead to 0 points.")
