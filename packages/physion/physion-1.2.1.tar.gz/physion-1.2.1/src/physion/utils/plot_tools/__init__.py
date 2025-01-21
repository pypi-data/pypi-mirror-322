import os, pathlib
from matplotlib import pylab

from .src.inset import *
from .src.adjust_plots import *
from .src.colors import *
from .src.legend import *
from .src.export import *
from .src.annotations import *
from .src.figure import *
from .src.pie import *
from .src.violin import *
from .src.line import plot
from .src.bar import bar
from .src.scatter import scatter
from .src.time_freq import time_freq, time_freq_signal
from .src.morphologies import nrnvyz

def set_style(label='manuscript'):
    """
    set the matplotlib style sheet
    """
    if label in ['manuscript', 'default']:
        pylab.style.use(os.path.join(pathlib.Path(__file__).resolve().parent,
                                    'style-sheets', 'manuscript.py'))
    if label in ['dark']:
        pylab.style.use(os.path.join(pathlib.Path(__file__).resolve().parent,
                                    'style-sheets', 'dark.py'))
    else:
        pylab.style.use(os.path.join(pathlib.Path(__file__).resolve().parent,
                                    'style-sheets', 'manuscript.py'))

set_style('default')


