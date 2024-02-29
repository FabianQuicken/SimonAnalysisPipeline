# -*- coding: utf-8 -*-
"""
Created on Thu Feb 29 08:13:00 2024

@author: fabia
"""

import numpy as np

# calculate euclidean distance

def euklidean_distance(x1, y1, x2, y2):
    """
    This func returns the euklidean distance between two points.
    (x1, y1) and (x2, y2) are the cartesian coordinates of the points.
    """

    distance = np.sqrt((x2-x1)**2 + (y2-y1)**2)
    return distance

print(euklidean_distance(2,2,1,1))