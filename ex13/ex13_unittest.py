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

import sys
import os
from glob import glob


def print_outs(outs, line_token="-"):
    print(line_token * 40)
    print(outs, end="" if isinstance(outs, str) and outs.endswith("\n") else "\n")
    print(line_token * 40)


ex_file = "ex13.py"
full_points = 5
points = full_points

filenames = sorted(glob(os.path.join("ex13_testfiles", "*")))
if not len(filenames):
    raise FileNotFoundError("Could not find files in directory 'ex13_testfiles'")
if len(filenames) != 13:
    raise FileNotFoundError(f"Expected 13 folders in 'ex13_testfiles', found {len(filenames)}")

inputs = filenames

correct_outs = [TypeError, AttributeError, AttributeError,
                AttributeError, AttributeError, AttributeError,
                AttributeError, ('0', 1, ['info', 'base', 'quality']),
                ('235gsa', 5, ['col0', 'col1', 'col2']), ('0', 1, ['info', 'base', 'quality']),
                ('0', 1, ['info', 'base', 'quality']), ('235gsa', 5, ['col0', 'col1', 'col2']),
                ('0', 1, ['info', 'base', 'quality'])]

print(f"Unittest for: {ex_file}")

for test_i, test_params in enumerate(zip(inputs, correct_outs)):
    filename, solution = test_params
    with open(filename, "r") as f:
        file_content = f.read()

    try:
        from ex13 import get_file_metadata
        outs = get_file_metadata(data_as_string=file_content)
        errs = ""
        if len(outs) != 3:
            points -= full_points / len(inputs)
        else:
            if outs[0] != solution[0]:
                points -= full_points / (len(inputs) / 3)
            if outs[1] != solution[1]:
                points -= full_points / (len(inputs) / 3)
            if outs[2] != solution[2]:
                points -= full_points / (len(inputs) / 3)
    except Exception as e:
        if type(solution) == type and isinstance(e, solution):
            # instance check is done, overwrite solution with the string message
            # or the code below that checks "outs == solution" does not work
            # a bit hacky, but OK for now
            solution = f"{type(e).__name__}: {e}"
            outs = solution
            errs = ""
        else:
            outs = ""
            errs = e
            points -= full_points / len(inputs)
    
    print()
    print_outs(f"Test {test_i}", line_token="#")
    print("Input was:")
    print_outs(f"data_as_string = <content of file {filename}>")

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
