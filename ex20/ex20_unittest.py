"""
Author -- Michael Widrich, Andreas Schörgenhumer
Contact -- schoergenhumer@ml.jku.at
updated by: Timo Bertram, 12.2021

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
import sys


def print_outs(outs, line_token="-"):
    print(line_token * 40)
    print(outs, end="" if isinstance(outs, str) and outs.endswith("\n") else "\n")
    print(line_token * 40)


ex_file = 'ex20.py'
full_points = 2
points = full_points
output_dir = 'ex20_unittest_tmp'
plot_output_dir = "ex20_testfiles"
video_output_file = os.path.join(output_dir, 'video.mp4')
os.makedirs(output_dir, exist_ok=True)

print(f"Unittest for: {ex_file}")

outs = ''
errs = ''

try:
    from ex20 import GameOfLife
    proper_import = True
except Exception as e:
    outs = ''
    errs = e
    points -= full_points
    proper_import = False

if proper_import:
    try:
        def unitinit(self, config_file, state_output_file, plot_output_dir, video_output_file):
            self.state = []
            self.dead_symbol = 'o'
            self.live_symbol = 'x'
            self.state_output_file = state_output_file
            self.plot_output_dir = plot_output_dir
            self.video_output_file = video_output_file
        
        GameOfLife.__init__ = unitinit
        instance = GameOfLife(config_file="", state_output_file=os.path.join(output_dir, "state.txt"),
                              plot_output_dir=plot_output_dir, video_output_file=video_output_file)

        if not hasattr(instance, 'make_video'):
            outs += f'  no method make_video() found!\n'
            points -= full_points
        else:
            instance.make_video()

            # Check if the video file was created
            if not os.path.exists(video_output_file):
                outs += f'  did not create output file {video_output_file}!\n'
                points -= full_points
        errs = ''
    except Exception as e:
        outs = ''
        errs = e
        points -= full_points

print()
print_outs(f"Test", line_token="#")
print("Function call was:")
print_outs(f"game.make_video()\n"
           f"with game.plot_output_dir='{plot_output_dir}'\n"
           f"     game.video_output_file='{video_output_file}'")

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
shutil.rmtree(output_dir)
