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
import sys
import subprocess
from glob import glob
import numpy as np
import pandas as pd


def print_outs(outs, line_token="-"):
    print(line_token * 40)
    print(outs, end="" if isinstance(outs, str) and outs.endswith("\n") else "\n")
    print(line_token * 40)


ex_file = "ex14.py"
full_points = 5
points = full_points
python = sys.executable

dirnames = sorted(glob(os.path.join("ex14_testfiles", "*/")))
dirnames = [d for d in dirnames if os.path.isdir(d)]

sequence = "atgc"

ntests = 3
if len(dirnames) != ntests:
    raise FileNotFoundError(f"Could not find {ntests} folders in directory 'ex14_testfiles'")

inputs = dirnames

print(f"Unittest for: {ex_file}")

for test_i, test_params in enumerate(inputs):
    foldername = test_params
    hamsterfilefolder = os.path.join(foldername, f"{test_i}")
    unittestoutputfile = os.path.join(foldername, "unittest_output.csv")
    correctoutputfile = os.path.join(foldername, "example_output.csv")
    
    function_call = "could not be called"
    outs = ""

    try:
        function_call = [sys.executable, ex_file, hamsterfilefolder, unittestoutputfile, sequence]
        with subprocess.Popen(function_call, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE) as proc:
            _, stderr = proc.communicate(timeout=30)
            with open(unittestoutputfile, "r") as f:
                created_content = pd.read_csv(f, sep=",", dtype=float)
            with open(correctoutputfile, "r") as f:
                correct_content = pd.read_csv(f, sep=",", dtype=float)
            
            if stderr:
                errs = stderr.decode("utf-8")
                points -= full_points / len(inputs)
            else:
                errs = ""
                if list(created_content.columns) != list(correct_content.columns):
                    outs += f"Columns: {list(created_content.columns)} != {list(correct_content.columns)}\n"
                    points -= (full_points / len(inputs)) / 4
                
                if not created_content.shape == correct_content.shape:
                    outs += f"Shapes of file columns/rows not equal: {created_content.shape} != {correct_content.shape}"
                    points -= (full_points / len(inputs)) * 3 / 4
                elif not np.all(np.isclose(created_content.values, correct_content.values, atol=0)):
                    inds = list(zip(*np.where(~np.isclose(created_content.values, correct_content.values, atol=0))))
                    outs += f"Values not equal at indices {inds}"
                    points -= (full_points / len(inputs)) * 3 / 4
    except Exception as e:
        outs = ""
        errs = e
        points -= full_points / len(inputs)
    finally:
        # Remove the output we created for this test
        if os.path.exists(unittestoutputfile):
            os.remove(unittestoutputfile)

    print()
    print_outs(f"Test {test_i}", line_token="#")
    print("Program call was:")
    print_outs(" ".join(function_call))

    if errs:
        print(f"Some unexpected errors occurred:")
        print_outs(f"{type(errs).__name__}: {errs}")
    else:
        print("Notes:")
        print_outs("No issues found" if outs == "" else outs)

    # due to floating point calculations it could happen that we get -0 here
    if points < 0:
        assert abs(points) < 1e-7, f"points were {points} < 0: error when subtracting points?"
        points = abs(points)
    print(f"Current points: {points:.2f}")

print(f"\nEstimated points upon submission: {points:.2f} (out of {full_points:.2f})")
print(f"This is only an estimate, see 'Instructions for submitting homework' in Moodle "
      f"for common mistakes that can still lead to 0 points.")
