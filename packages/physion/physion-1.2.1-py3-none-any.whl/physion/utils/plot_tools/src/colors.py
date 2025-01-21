from matplotlib.cm import viridis, viridis_r, copper, copper_r, cool, jet,\
    PiYG, binary, binary_r, bone, Pastel1, Pastel2, Paired, Accent, Dark2, Set1, Set2,\
    Set3, tab10, tab20, tab20b, tab20c

import matplotlib.colors as mpl_colors

def get_linear_colormap(color1='blue', color2='red'):
    return mpl_colors.LinearSegmentedColormap.from_list('mycolors',[color1, color2])

