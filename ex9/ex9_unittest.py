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


def print_outs(outs):
    print("-" * 40)
    print(outs, end="" if isinstance(outs, str) and outs.endswith("\n") else "\n")
    print("-" * 40)


ex_file = "ex9.py"
full_points = 2
points = full_points

inputs = [
    [[3, 1, 2, 3],
     [1, 4, 5, 6, 7],
     [2, 8, 9, 10]],
    [],
    [[0]],
    [[0, 1, 2]],
    [[1, 1],
     [1, 2]],
    [[3, 1, 2, 3],
     [2, 2, 3, 4],
     [2, 3, 4, 5]]
]
solutions = [
    [1, 2, 3, 4, 8, 9],
    [],
    [],
    [],
    [1, 2],
    [1, 2, 3, 2, 3, 3, 4]
]

print(f"Unittest for: {ex_file}")

for test_i, (input_, solution) in enumerate(zip(inputs, solutions)):
    try:
        from ex9 import fun

        outs = fun(input_)
        errs = ""
    except Exception as e:
        outs = ""
        errs = e

    print()
    print("#" * 40)
    print(f"Test {test_i}")
    print("#" * 40)

    if errs:
        print(f"Some errors occurred:")
        print_outs(errs)
    else:
        if outs == solution:
            print(f"\nThe output was correct and was:")
            print_outs(outs)
        else:
            print("Unexpected output:")
            print_outs(outs)
            print("Output should be:")
            print_outs(solution)

    if outs != solution or errs:
        points -= full_points / len(solutions)
        # due to floating point calculations it could happen that we get -0 here
        if points < 0:
            assert abs(points) < 1e-7, f"points were {points} < 0: error when subtracting points?"
            points = abs(points)
    print(f"Current points: {points:.2f}")

print(f"\nEstimated points upon submission: {points:.2f} (out of {full_points})")
print(f"This is only an estimate, see 'Instructions for submitting homework' in Moodle "
      f"for common mistakes that can still lead to 0 points.")