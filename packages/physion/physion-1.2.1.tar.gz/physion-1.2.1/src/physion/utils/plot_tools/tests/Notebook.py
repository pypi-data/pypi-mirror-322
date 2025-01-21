# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.14.0
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %%
import sys

sys.path.append('../..')
import plot_tools as pt
pt.set_style('dark')
import matplotlib.pylab as plt

# %%
import numpy as np
fig, ax = plt.subplots(figsize=(6,2))
pt.scatter(np.random.randn(100), np.random.randn(100), ax=ax)
pt.annotate(ax, 'skjdfh', (0.5, 1), color='lightgrey')

# %% [markdown]
# ## Test Environment

# %%

def test_function():
    """
    """
    this = 0
    that = 1
    print('that\'s it', this, that)

test_function()
