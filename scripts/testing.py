import glob
from tqdm import tqdm
import time
import pandas as pd
import numpy as np
import shutil
import matplotlib.pyplot as plt


from likelihood_filter import likelihood_filtering_nans, likelihood_filtering

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




def calc_interior_zone_polygon(df, bodypart=str):
    "Normally, the nose should be used because it indicates the orientation of the mouse best."
    data = df.copy()
    print(f"\nGet time spent of {bodypart} at cage edges...")
    print(f"Filtering {bodypart} for position calculation...")
    data = likelihood_filtering_nans(df=data, 
                                likelihood_row_name=bodypart+"_likelihood")
    bodypart_x = data[bodypart+"_x"]
    bodypart_y = data[bodypart+"_y"]

    print("Filtering for good corner prediction...")
    corners = ["topleft", "topright", "bottomleft", "bottomright"]
    for corner in corners:
        data = likelihood_filtering(df=data, 
                                    likelihood_row_name=f"{corner}_likelihood",
                                    filter_val=0.99)
    topleft_x = data["topleft_x"]
    topleft_y = data["topleft_y"]
    topright_x = data["topright_x"]
    topright_y = data["topright_y"]
    bottomleft_x = data["bottomleft_x"]
    bottomleft_y = data["bottomleft_y"]
    bottomright_x = data["bottomright_x"]
    bottomright_y = data["bottomright_y"]

    bodypart_x = np.array(bodypart_x)
    bodypart_y = np.array(bodypart_y)
    topleft_x = np.array(topleft_x)[0]
    topleft_y = np.array(topleft_y)[0]
    topright_x = np.array(topright_x)[0]
    topright_y = np.array(topright_y)[0]
    bottomleft_x = np.array(bottomleft_x)[0]
    bottomleft_y = np.array(bottomleft_y)[0]
    bottomright_x = np.array(bottomright_x)[0]
    bottomright_y = np.array(bottomright_y)[0]

    #original_corners = [(topleft_x, topleft_y), (topright_x, topright_y), (bottomleft_x,bottomleft_y), (bottomright_x, bottomright_y)]
    scaling_factor = 0.1

    topleft_x += (topright_x - topleft_x) * scaling_factor
    topleft_y += (bottomleft_y - topleft_y) * scaling_factor
    topright_x -= (topright_x - topleft_x) * scaling_factor
    topright_y += (bottomright_y - topright_y) * scaling_factor
    bottomleft_x += (bottomright_x - bottomleft_x) * scaling_factor
    bottomleft_y -= (bottomleft_y - topleft_y) * scaling_factor
    bottomright_x -= (bottomright_x - bottomleft_x) * scaling_factor
    bottomright_y -= (bottomright_y - topright_y) * scaling_factor

    scaled_corners = [(bottomleft_x,bottomleft_y), (bottomright_x, bottomright_y), (topright_x, topright_y), (topleft_x, topleft_y)]

    return (bodypart_x, bodypart_y), scaled_corners

def calc_edge_time(nose_coords=tuple, scaled_corner_coords=list):
    """
    nose_coords should be a tuple of two list containing x and y coordinates, respectively.
    scaled_orner_coords should be a list containing tuples of the scaled corner coordinates
    """
    nose_x = nose_coords[0]
    nose_y = nose_coords[1]
    edge_time = np.zeros(len(nose_x))

    for i in range(len(nose_x)):
        inside = punkt_in_viereck(punkt=(nose_x[i], nose_y[i]), eckpunkte=scaled_corner_coords)
        if not inside:
            edge_time[i] = 1
    return edge_time





path_parameters = f"./datasets/testing/processed/bodyparts/*.csv"
#path_parameters_done = f"testing/processed/parameters/done/"
file_list_parameters = glob.glob(path_parameters)
print(file_list_parameters)

corner_coords_test = [(400,1000),(1700,1000),(1700,300),(400,300)]
nose_coords_test = ([1600],[500])


for file in tqdm(file_list_parameters):
    print(f"Working on file: {file}")
    time.sleep(0.2)
    parameters_df = pd.read_csv(file)
    nose_coords, scaled_corner_coords = calc_interior_zone_polygon(df=parameters_df, bodypart="nose")
    edge_time = calc_edge_time(nose_coords, scaled_corner_coords)
    #edge_time = calc_edge_time(nose_coords_test, corner_coords_test)
    print(sum(edge_time)) 

    
   