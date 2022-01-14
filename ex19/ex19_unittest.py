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
from glob import glob
import pickle


def print_outs(outs, line_token="-"):
    print(line_token * 40)
    print(outs, end="" if isinstance(outs, str) and outs.endswith("\n") else "\n")
    print(line_token * 40)


ex_file = 'ex19.py'
full_points = 5
points = full_points
output_dir = 'ex19_unittest_tmp'
os.makedirs(output_dir, exist_ok=True)

inp_filenames = sorted(glob(os.path.join("ex19_testfiles", "input*.pkl")))
out_filenames = sorted(glob(os.path.join("ex19_testfiles", "output*.txt")))
if len(inp_filenames) == 0 or len(out_filenames) == 0:
    raise FileNotFoundError("Could not find files in directory ex19_testfiles")

print(f"Unittest for: {ex_file}")

for test_i, test_params in enumerate(zip(inp_filenames, out_filenames)):
    inp_filename, out_filename = test_params
    outs = ''
    errs = ''
    state_output_file = os.path.join(output_dir, os.path.basename(inp_filename).replace('input', 'output') + '.txt')
    
    with open(inp_filename, 'rb') as pfh:
        input_state = pickle.load(pfh)
    
    try:
        from ex19 import GameOfLife
        proper_import = True
    except Exception as e:
        outs = ''
        errs = e
        points -= full_points / len(inp_filenames)
        proper_import = False
    
    if proper_import:
        try:
            def unitinit(self, config_file, state_output_file, plot_output_dir, video_output_file):
                self.state = input_state["init_state"]
                self.dead_symbol = input_state["dead_symbol"].replace(' ', '-')
                self.live_symbol = input_state["live_symbol"]
                self.state_output_file = state_output_file
                self.plot_output_dir = plot_output_dir
                self.video_output_file = video_output_file
            
            GameOfLife.__init__ = unitinit
            instance = GameOfLife(config_file="", state_output_file=state_output_file,
                                  plot_output_dir=output_dir, video_output_file=os.path.join(output_dir, "video.mp4"))
            
            if not hasattr(instance, '__write_state__'):
                outs += f'  no method __write_state__(...) found!\n'
                points -= full_points / len(inp_filenames)
            else:
                instance.__write_state__(input_state['parameter0'], input_state['parameter1'])
                
                # Check if output file was created
                if not os.path.exists(state_output_file):
                    outs += f'  did not create state output file {state_output_file}!\n'
                    points -= full_points / len(inp_filenames)
                else:
                    with open(state_output_file, 'r') as fh:
                        outcontent = fh.read()
                    with open(out_filename, 'r') as fh:
                        correct_content = fh.read()
                    if outcontent != correct_content:
                        outs += f'  content of output file not correct;\n' \
                                f'  your output:\n"{outcontent}"\n' \
                                f'  correct output:\n"{correct_content}"\n\n'
                        points -= full_points / len(inp_filenames)
            
            errs = ''
        except Exception as e:
            outs = ''
            errs = e
            points -= full_points / len(inp_filenames)

    print()
    print_outs(f"Test {test_i}", line_token="#")
    print("Function call was:")
    ls = input_state['parameter0']
    if ls is not None:
        ls = f"'{ls}'"
    ds = input_state['parameter1']
    if ds is not None:
        ds = f"'{ds}'"
    print_outs(f"game.__write_state__(live_symbol={ls}, dead_symbol={ds})\n"
               f"with game.state_output_file='{state_output_file}'")

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
