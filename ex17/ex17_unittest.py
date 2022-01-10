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


ex_file = 'ex17.py'
full_points = 11
points = full_points

input_files = sorted(glob(os.path.join("ex17_testfiles", "input*.pkl")))
output_files = sorted(glob(os.path.join("ex17_testfiles", "output*.pkl")))
if not len(input_files) or not len(output_files):
    raise FileNotFoundError("Could not find files in directory ex17_testfiles")

print(f"Unittest for: {ex_file}")

for test_i, test_params in enumerate(zip(input_files, output_files)):
    input_file, output_file = test_params
    
    with open(input_file, 'rb') as f:
        input_state, input_scope = pickle.load(f)
    with open(output_file, 'rb') as f:
        correct_state = pickle.load(f)
    
    try:
        from ex17 import gen_next_state
        outs = gen_next_state(state=input_state, scope=input_scope)
        errs = ''
        if not isinstance(outs, np.ndarray):
            points -= full_points / len(input_files)
        else:
            if not np.issubdtype(outs.dtype, np.integer) or np.any(outs != correct_state):
                points -= full_points / len(input_files)
    except Exception as e:
        outs = ''
        errs = e
        points -= full_points / len(input_files)
    
    print()
    print_outs(f"Test {test_i}", line_token="#")
    print("Function call was:")
    print_outs(f"gen_next_state(state=\n{input_state},\nscope={input_scope})")
    
    if errs:
        print(f"Some unexpected errors occurred:")
        print_outs(f"{type(errs).__name__}: {errs}")
    else:
        if (outs == correct_state).all():
            print(f"The output was correct and was:")
            print_outs(outs)
        else:
            print("Unexpected output:")
            print_outs(outs)
            print("Output should be:")
            print_outs(correct_state)
    
    # due to floating point calculations it could happen that we get -0 here
    if points < 0:
        assert abs(points) < 1e-7, f"points were {points} < 0: error when subtracting points?"
        points = abs(points)
    print(f"Current points: {points:.2f}")

print(f"\nEstimated points upon submission: {points:.2f} (out of {full_points:.2f})")
print(f"This is only an estimate, see 'Instructions for submitting homework' in Moodle "
      f"for common mistakes that can still lead to 0 points.")
