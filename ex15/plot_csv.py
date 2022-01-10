"""
Author -- Michael Widrich
Contact -- widrich@ml.jku.at
Date -- 01.10.2020

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

import pandas as pd
from matplotlib import pyplot as plt


def plot_csv(inputfilename: str, outputfilename: str):
    data = pd.read_csv(inputfilename, sep=',')
    fig, ax = plt.subplots()
    for label in data.columns:
        if label == 'subsequence':
            ax.plot(data[label]*100, label=label+" x100")
        else:
            ax.plot(data[label], label=label)
    ax.set(xlabel='time (days)', ylabel='counts',
           title='Base and subsequence counts')
    ax.grid()
    plt.legend()
    fig.savefig(outputfilename)
    plt.close(fig)
    del fig
    
    
if __name__ == '__main__':
    # Example usage:
    plot_csv(inputfilename="sequence_analysis.csv", outputfilename="sequence_analysis.png")
