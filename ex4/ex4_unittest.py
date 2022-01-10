"""
Author -- Andreas Schörgenhumer, Sebastian Lehner
Contact -- schoergenhumer@ml.jku.at
Date -- 08.10.2021

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
import itertools


def print_outs(outs):
	print("-" * 30)
	print(outs, end="" if outs.endswith("\n") else "\n")
	print("-" * 30)


ex_file = "ex4.py"
full_points = 5
points = full_points
python = sys.executable

datatype1s = ["float"]
value1s = ["4", "-3.8", "+1e-2"]
datatype2s = ["float"]
value2s = ["2", "-3"]
operations = ["multiply"]
inputs = list(itertools.product(datatype1s, value1s, datatype2s, value2s, operations))
solutions = ["8.0", "-12.0", "-7.6", "11.399999999999999", "0.02", "-0.03"]

datatype1s = ["int"]
value1s = ["4"]
datatype2s = ["int"]
value2s = ["2", "-3"]
operations = ["add", "multiply"]
inputs += list(itertools.product(datatype1s, value1s, datatype2s, value2s, operations))
solutions += ["6", "8", "1", "-12"]

datatype1s = ["string"]
value1s = ["4", "-3.8", "+1e-2", "Ex4"]
datatype2s = ["int"]
value2s = ["3"]
operations = ["multiply"]
inputs += list(itertools.product(datatype1s, value1s, datatype2s, value2s, operations))
solutions += ["444", "-3.8-3.8-3.8", "+1e-2+1e-2+1e-2", "Ex4Ex4Ex4"]

datatype1s = ["string"]
value1s = ["joined"]
datatype2s = ["string"]
value2s = ["Text"]
operations = ["add", "subtract"]
inputs += list(itertools.product(datatype1s, value1s, datatype2s, value2s, operations))
solutions += ["joinedText", "unknown operation"]

print(f"Unittest for: {ex_file}")

for test_i, test_params in enumerate(zip(inputs, solutions)):
	stdins, solution = test_params
	stdins = [f"{i}\n" for i in stdins]
	
	with subprocess.Popen([f"{python}", ex_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE) as proc:
		try:
			outs, errs = proc.communicate(input="".join(stdins).encode(), timeout=15)
		except subprocess.TimeoutExpired:
			proc.kill()
			outs, errs = proc.communicate()
		outs = outs.decode("utf-8").replace("\r", "")
		errs = errs.decode("utf-8").replace("\r", "")
	outs = outs.replace('Select a datatype (type "int", "float" or "string" and hit enter) for var1: ',
						f'Select a datatype (type "int", "float" or "string" and hit enter) for var1: {stdins[0]}')
	outs = outs.replace("Enter var1: ", f"Enter var1: {stdins[1]}")
	outs = outs.replace('Select a datatype (type "int", "float" or "string" and hit enter) for var2: ',
						f'Select a datatype (type "int", "float" or "string" and hit enter) for var2: {stdins[2]}')
	outs = outs.replace("Enter var2: ", f"Enter var2: {stdins[3]}")
	outs = outs.replace('Choose an operation (type "add" or "multiply"): ',
						f'Choose an operation (type "add" or "multiply"): {stdins[4]}')
	correct_outs = f'Select a datatype (type "int", "float" or "string" and hit enter) for var1: {stdins[0]}' \
				   f'Enter var1: {stdins[1]}Select a datatype (type "int", "float" or "string" and hit enter) for var2: {stdins[2]}' \
				   f'Enter var2: {stdins[3]}Choose an operation (type "add" or "multiply"): {stdins[4]}Result: {solution}\n'
	
	print()
	print("#" * 30)
	print(f"Test {test_i}")
	print("#" * 30)
	
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
			assert abs(points) < 1e-7, f"points were {points} < 0, so there appears to be an error when subtracting points"
			points = abs(points)
	print(f"Current points: {points:.2f}")

print(f"\nEstimated points upon submission: {points:.2f} (out of {full_points})")
print(f"This is only an estimate, see 'Instructions for submitting homework' in Moodle for common mistakes that can still lead to 0 points.")
