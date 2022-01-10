"""
Author -- Andreas Schörgenhumer, Michael Widrich
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


def print_outs(outs):
	print("-" * 30)
	print(outs, end="" if outs.endswith("\n") else "\n")
	print("-" * 30)


ex_file = "ex1.py"
full_points = 2.5
points = full_points
python = sys.executable

with subprocess.Popen([f"{python}", ex_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE) as proc:
	try:
		outs, errs = proc.communicate(timeout=15)
	except subprocess.TimeoutExpired:
		proc.kill()
		outs, errs = proc.communicate()
	outs = outs.decode("utf-8").replace("\r", "")
	errs = errs.decode("utf-8").replace("\r", "")

if not outs == "10\nI read the instructions for submitting homework.\nI completed exercise 1!\n":
	points = 0
	
if errs:
	points = 0

print(f"Unittest for: {ex_file}\n")
if errs:
	print(f"Some errors occurred:")
	print_outs(errs)
else:
	print(f"\nOutput was:")
	print_outs(outs)
print(f"\nEstimated points upon submission: {points} (out of {full_points})")
print(f"This is only an estimate, see 'Instructions for submitting homework' in Moodle for common mistakes that can still lead to 0 points.")
