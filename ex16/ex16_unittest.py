"""
Author -- Michael Widrich, Andreas Schörgenhumer
Contact -- schoergenhumer@ml.jku.at
updated by: Van Quoc Phuong Huynh, 11.2021

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
import pickle
from glob import glob

import numpy as np


def print_outs(outs, line_token="-"):
    print(line_token * 40)
    print(outs, end="" if isinstance(outs, str) and outs.endswith("\n") else "\n")
    print(line_token * 40)


ex_file = 'ex16.py'
full_points = 11
points = full_points

filenames = sorted(glob(os.path.join("ex16_testfiles", "*.config")))
if not len(filenames):
    raise FileNotFoundError("Could not find files in directory ex16_testfiles")

inputs = filenames

with open(os.path.join('ex16_testfiles', 'correct_outputs.pkl'), 'rb') as pfh:
    correct_outs = pickle.load(pfh)

print(f"Unittest for: {ex_file}")

for test_i, (filename, solution) in enumerate(zip(inputs, correct_outs)):
    outs = ''
    errs = ''
    points_before = points
    
    try:
        from ex16 import read_config_file
        proper_import = True
    except Exception as e:
        errs = e
        points -= full_points / len(inputs)
        proper_import = False
    
    if proper_import:
        try:
            outs = read_config_file(config_file=filename)
            if solution == '<ValueError> should be raised':
                points -= full_points / len(inputs)
            elif solution == '<AttributeError> should be raised':
                points -= full_points / len(inputs)
            else:
                n_expected_returns = 5
                if len(outs) != n_expected_returns:
                    points -= full_points / len(inputs)
                else:
                    if not isinstance(outs[0], int) or outs[0] != solution[0]:
                        points -= full_points / len(inputs) / n_expected_returns
                    if outs[1] != solution[1]:
                        points -= full_points / len(inputs) / n_expected_returns
                    if outs[2] != solution[2]:
                        points -= full_points / len(inputs) / n_expected_returns

                    try:
                        if not np.all(outs[3] == solution[3]) or not np.issubdtype(outs[3].dtype, np.integer):
                            points -= full_points / len(inputs) / n_expected_returns
                    except Exception as e:
                        points -= full_points / len(inputs) / n_expected_returns

                    try:
                        for i in range(len(solution[4])):
                            if not isinstance(outs[4][i], int) or outs[4][i] != solution[4][i]:
                                points -= full_points / len(inputs) / n_expected_returns
                                break
                    except Exception as e:
                        points -= full_points / len(inputs) / n_expected_returns
        except Exception as e:
            # Overwrite solution with the string message or the code below that checks
            # "outs == solution" does not work. A bit hacky, but OK for now.
            if solution == '<ValueError> should be raised':
                if isinstance(e, ValueError):
                    outs = f'<ValueError> was raised: {e}'
                    solution = outs
                else:
                    outs = ''
                    errs = e
                    points -= full_points / len(inputs)
            elif solution == '<AttributeError> should be raised':
                if isinstance(e, AttributeError):
                    outs = f'<AttributeError> was raised: {e}'
                    solution = outs
                else:
                    outs = ''
                    errs = e
                    points -= full_points / len(inputs)
            else:
                outs = ''
                errs = e
                points -= full_points / len(inputs)

    print()
    print_outs(f"Test {test_i}", line_token="#")
    print("Function call was:")
    print_outs(f"read_config_file(configpath=r'{filename}')")
    
    if errs:
        print(f"Some unexpected errors occurred:")
        print_outs(f"{type(errs).__name__}: {errs}")
    else:
        if points_before == points:  # this means everything worked as expected
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

