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
import shutil
import subprocess
import sys


def print_outs(outs, line_token="-"):
    print(line_token * 40)
    print(outs, end="" if isinstance(outs, str) and outs.endswith("\n") else "\n")
    print(line_token * 40)


ex_file = "ex15.py"
full_points = 5
points = full_points
python = sys.executable

inputs = ["outputs_1", "outputs_2"]

for inputfolder in inputs:
    if os.path.exists(inputfolder):
        raise FileExistsError(f"The unit test will create and delete the folders {inputs}. "
                              f"If you want to keep yours, you have to rename them.")

print(f"Unittest for: {ex_file}")

for test_i, test_params in enumerate(inputs):
    foldername = test_params
    raw_data_folder = "125"
    
    function_call = "could not be called"
    outs = ""

    try:
        function_call = [sys.executable, ex_file, foldername]
        with subprocess.Popen(function_call, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE) as proc:
            _, stderr = proc.communicate(timeout=60*5)
            
            if len(stderr):
                errs = stderr.decode("utf-8")
                points -= full_points / len(inputs)
            else:
                errs = ""
                if os.path.exists(os.path.join(foldername, raw_data_folder)):
                    outs += f"Creation of folders seems correct\n"
                else:
                    points -= full_points / len(inputs) / 3
                    outs += f"Folder {os.path.join(foldername, raw_data_folder)} not found\n"

                if os.path.exists(os.path.join(foldername, "patterns_analysis.csv")):
                    outs += f"Creation of {os.path.join(foldername, 'patterns_analysis.csv')} seems correct\n"
                else:
                    points -= full_points / len(inputs) / 3
                    outs += f"File {os.path.join(foldername, 'patterns_analysis.csv')} not found\n"

                if os.path.exists(os.path.join(foldername, "patterns_analysis.png")):
                    outs += f"Creation of {os.path.join(foldername, 'patterns_analysis.png')} seems correct\n"
                else:
                    points -= full_points / len(inputs) / 3
                    outs += f"File {os.path.join(foldername, 'patterns_analysis.png')} not found\n"
    except Exception as e:
        outs = ""
        errs = e
        points -= full_points / len(inputs)
    finally:
        # Remove the output we created for this test
        shutil.rmtree(foldername, ignore_errors=True)

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
