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
import shutil
from glob import glob

import numpy as np


def print_outs(outs, line_token="-"):
    print(line_token * 40)
    print(outs, end="" if isinstance(outs, str) and outs.endswith("\n") else "\n")
    print(line_token * 40)


ex_file = 'ex18.py'
full_points = 8
points = full_points
output_dir = 'ex18_unittest_tmp'
os.makedirs(output_dir, exist_ok=True)

input_filenames = sorted(glob(os.path.join("ex18_testfiles", "input*.pkl")))
if not len(input_filenames):
    raise FileNotFoundError("Could not find files in directory ex18_testfiles")

output_paths = [os.path.join(output_dir, f'out{i:02}') for i in range(len(input_filenames))]

print(f"Unittest for: {ex_file}")

for test_i, test_params in enumerate(zip(input_filenames, output_paths)):
    input_filename, output_path = test_params
    outs = ''
    errs = ''
    
    with open(input_filename, 'rb') as f:
        input_dict = pickle.load(f)
    
    try:
        from ex18 import GameOfLife
        proper_import = True
    except Exception as e:
        outs = ''
        errs = e
        points -= full_points / len(input_filenames)
        proper_import = False
    
    if proper_import:
        try:
            os.makedirs(output_path, exist_ok=True)
            state_output_file = os.path.join(output_path, f'output_{test_i:02}.pkl')
            plot_output_dir = os.path.join(output_path, "plots")
            video_output_file = os.path.join(output_dir, "some", "temp", "subdirs", "video.mp4")

            def unittest_read_config_file(_, config_file):
                with open(config_file, 'rb') as f:
                    content_dict = pickle.load(f)
                return tuple([content_dict[k] for k in ('iteration_count', 'dead_symbol', 'live_symbol', 'init_state', 'scope')])
            
            GameOfLife.read_config_file = unittest_read_config_file
            instance = GameOfLife(config_file=input_filename, state_output_file=state_output_file,
                                  plot_output_dir=plot_output_dir, video_output_file=video_output_file)
            
            # Check if files and directories were created
            if not os.path.exists(state_output_file):
                outs += f'  did not create state output file {state_output_file}!\n'
                points -= full_points / len(input_filenames) / 11
            if not os.path.exists(plot_output_dir):
                outs += f'  did not create plot folder {plot_output_dir}!\n'
                points -= full_points / len(input_filenames) / 11
            if not os.path.exists(os.path.dirname(video_output_file)):
                outs += f'  did not create video (base) folder {video_output_file}!\n'
                points -= full_points / len(input_filenames) / 11

            attribute = 'state_output_file'
            if not hasattr(instance, attribute):
                outs += f'  missing attribute {attribute}!\n'
                points -= full_points / len(input_filenames) / 11
            else:
                out = getattr(instance, attribute)
                if state_output_file != out:
                    outs += f'  attribute {attribute} has incorrect value (should be {state_output_file} but is {out})!\n'
                    points -= full_points / len(input_filenames) / 11

            attribute = 'current_iteration'
            if not hasattr(instance, attribute):
                outs += f'  missing attribute {attribute}!\n'
                points -= full_points / len(input_filenames) / 11
            else:
                out = getattr(instance, attribute)
                if out != 0:
                    outs += f'  attribute {attribute} has incorrect value (should be 0 but is {out})!\n'
                    points -= full_points / len(input_filenames) / 11

            attribute = 'state'
            if not hasattr(instance, attribute):
                outs += f'  missing attribute {attribute}!\n'
                points -= full_points / len(input_filenames) / 11
            else:
                out = getattr(instance, attribute)
                cout = input_dict['init_state']

                if (out.dtype != cout.dtype) or np.any(cout != out):
                    outs += f'  attribute {attribute} has incorrect value (should be \n{cout} but is \n{out})!\n'
                    points -= full_points / len(input_filenames) / 11
            
            for attribute in input_dict.keys():
                if not hasattr(instance, attribute):
                    outs += f'  missing attribute {attribute}!\n'
                    points -= full_points / len(input_filenames) / 11
                else:
                    out = getattr(instance, attribute)
                    cout = input_dict[attribute]
                        
                    if isinstance(cout, np.ndarray) and ((out.dtype != cout.dtype) or np.any(cout != out)):
                        outs += f'  attribute {attribute} has incorrect value (should be \n{cout} but is \n{out})!\n'
                        points -= full_points / len(input_filenames) / 11 / 2
                    if not isinstance(cout, np.ndarray) and cout != out:
                        outs += f'  attribute {attribute} has incorrect value (should be {cout} but is {out})!\n'
                        points -= full_points / len(input_filenames) / 11 / 2
            
            errs = ''
        except Exception as e:
            outs = ''
            errs = e
            points -= full_points / len(input_filenames)

    print()
    print_outs(f"Test {test_i}", line_token="#")
    
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
