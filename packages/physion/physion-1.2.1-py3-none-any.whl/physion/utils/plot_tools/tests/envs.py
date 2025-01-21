import os, sys, pathlib

sys.path.append('../')

import matplotlib.pylab as plt
import plot_tools as pt

import numpy as np

pt.set_style('dark')

fig, ax = plt.subplots(1)

ax.hist(np.random.randn(100))

plt.tight_layout()

plt.show()

