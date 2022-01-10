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

import os
import itertools
import regex
from glob import glob


def print_outs(outs, line_token="-"):
    print(line_token * 40)
    print(outs, end="" if isinstance(outs, str) and outs.endswith("\n") else "\n")
    print(line_token * 40)


ex_file = "ex11.py"
full_points = 5.5
points = full_points

filenames = sorted(glob(os.path.join("ex11_testfiles", "*")))
if not len(filenames):
    raise FileNotFoundError("Could not find files in directory 'ex11_testfiles'")
if not (len(filenames) == 8):
    raise FileNotFoundError(f"Expected 8 files in directory 'ex11_testfiles' but found {len(filenames)}")

subsequences = ["ATtC", "aT"]

inputs = list(itertools.product(filenames, subsequences))

correct_outs = [(0, {'a': 1, 'c': 2, 'g': 2, 't': 2}),
                (0, {'a': 1, 'c': 2, 'g': 2, 't': 2}),
                (0, {'a': 4, 'c': 2, 'g': 0, 't': 2}),
                (1, {'a': 4, 'c': 2, 'g': 0, 't': 2}),
                (0, {'a': 2, 'c': 2, 'g': 1, 't': 2}),
                (1, {'a': 2, 'c': 2, 'g': 1, 't': 2}),
                (1, {'a': 3, 'c': 3, 'g': 2, 't': 4}),
                (1, {'a': 3, 'c': 3, 'g': 2, 't': 4}),
                (3, {'a': 5, 'c': 5, 'g': 1, 't': 12}),
                (5, {'a': 5, 'c': 5, 'g': 1, 't': 12}),
                (3, {'a': 10, 'c': 7, 'g': 1, 't': 19}),
                (10, {'a': 10, 'c': 7, 'g': 1, 't': 19}),
                (0, {'a': 0, 'c': 0, 'g': 0, 't': 0}),
                (0, {'a': 0, 'c': 0, 'g': 0, 't': 0}),
                (2, {'a': 84, 'c': 71, 'g': 69, 't': 107}),
                (23, {'a': 84, 'c': 71, 'g': 69, 't': 107})]

print(f"Unittest for: {ex_file}")

for test_i, test_params in enumerate(zip(inputs, correct_outs)):
    (filename, subsequence), solution = test_params
    with open(filename, "r") as f:
        file_content = f.read()
    
    try:
        from ex11 import count_bases_and_subsequence
        outs = count_bases_and_subsequence(data_as_string=file_content, subsequence=subsequence)
        errs = ""
        if len(outs) != 2:
            points -= full_points / len(inputs)
        else:
            if outs[0] != solution[0]:
                points -= full_points / len(inputs) / 2
            if outs[1] != solution[1]:
                points -= full_points / len(inputs) / 2
    except Exception as e:
        outs = ""
        errs = e
        points -= full_points / len(inputs)
    
    print()
    print_outs(f"Test {test_i}", line_token="#")

    if errs:
        print(f"Some unexpected errors occurred:")
        print_outs(f"{type(errs).__name__}: {errs}")
    else:
        if outs == solution:
            print(f"The output was correct and was:")
            print_outs(outs)
        else:
            print("Unexpected output:")
            print_outs(outs)
            print("Output should be:")
            print_outs(solution)

    # due to floating point calculations it could happen that we get -0 here
    if points < 0:
        assert abs(points) < 1e-7, f"points were {points} < 0: error when subtracting points?"
        points = abs(points)
    print(f"Current points: {points:.2f}")

print(f"\nEstimated points upon submission: {points:.2f} (out of {full_points:.2f})")
print(f"This is only an estimate, see 'Instructions for submitting homework' in Moodle "
      f"for common mistakes that can still lead to 0 points.")
