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
    if np.isnan(x1):
        distance = np.nan
    elif np.isnan(x2):
        distance = np.nan
    else:
        distance = np.sqrt((x2-x1)**2 + (y2-y1)**2)
        
    return distance

def fill_missing_values(array):
    """
    Replacing np.nans with a linear interpolation. Takes and returns an array.
    """
    nan_indices = np.isnan(array)
    array[nan_indices] = np.interp(np.flatnonzero(nan_indices), np.flatnonzero(~nan_indices), array[~nan_indices])
    return array

def punkt_in_viereck(punkt, eckpunkte):
    x, y = punkt

    # Überprüfen, ob der Punkt links oder rechts von der Fläche liegt
    if x < min(eckpunkte[0][0], eckpunkte[1][0], eckpunkte[2][0], eckpunkte[3][0]) or \
       x > max(eckpunkte[0][0], eckpunkte[1][0], eckpunkte[2][0], eckpunkte[3][0]):
        return False

    # Überprüfen, ob der Punkt über oder unter der Fläche liegt
    elif y < min(eckpunkte[0][1], eckpunkte[1][1], eckpunkte[2][1], eckpunkte[3][1]) or \
       y > max(eckpunkte[0][1], eckpunkte[1][1], eckpunkte[2][1], eckpunkte[3][1]):
        return False


    # Überprüfen, ob der Punkt innerhalb der Fläche liegt
    # Verwendung der "ray-casting"-Methode
    n = len(eckpunkte)
    inside = False
    # get topleft corner coordinates
    p1x, p1y = eckpunkte[0]
    # repeat the loop 5 times
    for i in range(n + 1):
        # uses module to wrap around the coordinates
        # e.g. 0 % 4 = 0, 1 % 4 = 1, 4 % 4 = 0
        # in first iteration p1x,p1y = p2x, p2y but this is then skipped
        # in the last iteration p1x, p1y is eckpunkte[3] amd p2x,p2y is eckpunkte[0] (complete wrap around)
        p2x, p2y = eckpunkte[i % n]
        # following 2 lines check if point is between y-coordinates of polygon
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                # the following line checks if x is smaller than the right most x of polygon
                if x <= max(p1x, p2x):
                    # if the polygon is not aligned to the coordinate system axes, non-horizontal intersections are 
                    # calculated next
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y

    return inside

