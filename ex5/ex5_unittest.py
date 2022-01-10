"""
Author -- Andreas Schörgenhumer
Contact -- schoergenhumer@ml.jku.at
Date -- 26.10.2021

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
import subprocess


def print_outs(outs):
    print("-" * 40)
    print(outs, end="" if isinstance(outs, str) and outs.endswith("\n") else "\n")
    print("-" * 40)


ex_file = "ex5.py"
full_points = 2
points = full_points
python = sys.executable

input_str = "Enter int >= 0 or 'x' to exit: "
invalid_str = "You must enter an int >= 0 or 'x'"
inputs = [
    [1, 5, 4, "x"],
    ["x"],
    ["y", 1, "x"],
    [2, 2.5, -3, 0, "x"]
]
solutions = [
    [input_str, input_str, input_str, input_str, 10],
    [input_str, 0],
    [input_str, invalid_str, input_str, input_str, 1],
    [input_str, input_str, invalid_str, input_str, invalid_str, input_str, input_str, 2]
]

print(f"Unittest for: {ex_file}")

for test_i, test_params in enumerate(zip(inputs, solutions)):
    stdins, solution = test_params
    stdins = [f"{i}\n" for i in stdins]

    with subprocess.Popen([f"{python}", ex_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          stdin=subprocess.PIPE) as proc:
        try:
            outs, errs = proc.communicate(input="".join(stdins).encode(), timeout=15)
        except subprocess.TimeoutExpired:
            proc.kill()
            outs, errs = proc.communicate()
        outs = outs.decode("utf-8").replace("\r", "")
        errs = errs.decode("utf-8").replace("\r", "")

    i = outs.find(input_str)
    j = 0
    while i != -1:
        outs = outs[:i + len(input_str)] + stdins[j] + outs[i + len(input_str):]
        i = outs.find(input_str, i + 1)
        j += 1

    correct_outs = ""
    j = 0
    for s in solution[:-1]:
        if s == invalid_str:
            correct_outs += f"{s}\n"
        else:
            correct_outs += s + stdins[j]  # already includes "\n"
            j += 1
    correct_outs += f"{solution[-1]}\n"

    print()
    print("#" * 40)
    print(f"Test {test_i}")
    print("#" * 40)

    if errs:
        print(f"Some errors occurred:")
        print_outs(errs)
    else:
        if outs == correct_outs:
            print(f"\nThe output was correct and was:")
            print_outs(outs)
        else:
            print("Unexpected output:")
            print_outs(outs)
            print("Output should be:")
            print_outs(correct_outs)

    if outs != correct_outs or errs:
        points -= full_points / len(solutions)
        # due to floating point calculations it could happen that we get -0 here
        if points < 0:
            assert abs(points) < 1e-7, f"points were {points} < 0: error when subtracting points?"
            points = abs(points)
    print(f"Current points: {points:.2f}")

print(f"\nEstimated points upon submission: {points:.2f} (out of {full_points})")
print(f"This is only an estimate, see 'Instructions for submitting homework' in Moodle "
      f"for common mistakes that can still lead to 0 points.")
