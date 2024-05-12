import pandas as pd
import glob
from configurations import mice, paradigms, networks, cameras
import os

def check_string_in_string(full_string, part_string):
    """
    This function checks, if a string is found in another string.
    Returns True or False.
    """
    if part_string in full_string:
        return True
    else:
        return False
    
def get_metadata(csv_file_path):
    """
    Gets the metadata of the file name, based on the naming convention. The name is split with underscores: '_'.
    The file needs to be named: 'date_camera_mousenumber_paradigm_paradigm_paradigm_....'
    Paradigm contains information about experiment number (e.g. 'V1'), habituation or experiment, urinright or urinleft.
    """
    file_name = os.path.splitext(os.path.basename(csv_file_path))[0]
    parts = file_name.split('_')
    
    date = parts [0]
    camera = parts [1]
    mouse = parts [2]

    if "DLC" in parts[5]:
        parts[5] = parts[5][:-3]
    #füge erkennung meines paradigms hinzu - wo kamera vorne steht
    if camera == "topview" or camera == "sideview":
        if "DLC" in parts[4]:
            parts[4] = parts[4][:-3]
        paradigm = parts[3] + "_" + parts[4]
    else:
        paradigm = parts[3]+"_"+parts[4]+"_"+parts[5]
    #füge erkennung meines paradigms hinzu - wo datum vorne steht
    if parts[0] == "topview" or parts[0] == "sideview":
        date = parts[3]
        camera = parts [0]
        mouse = parts [2]
        if "DLC" in parts[4]:
            paradigm = parts[1] + "_" + parts[4][:-3]
        else:
            paradigm = parts[1] + "_" + parts[4]
    return {"date": date,
            "camera": camera,
            "mouse": mouse,
            "paradigm": paradigm}


    
def get_metadata_old(csv_file_path, mice=mice, paradigms=paradigms, networks=networks, cameras=cameras):
    """
    this function saves important metadata from the filename:
    mouse, date, paradigm, networkname, camera
    returns the information as dictionary - this dic can be used to construct a pandas dataframe
    """
    metadata_list = [mice, paradigms, networks, cameras]
    output_list = ["","","",""]
    csv_file_path = csv_file_path.lower()
    for i, data in enumerate(metadata_list):
        for p in data:
            if check_string_in_string(full_string=csv_file_path, part_string=p):
                output_list[i] = p
                break
    output_list[0] = output_list[0].replace("_","") #removes the underscores from the mouse number (they are need to avoid confusion with other numbers in the filename)
    return {"Mouse": [output_list[0]],
            "Paradigm": [output_list[1]],
            "Network": [output_list[2]], 
            "Camera": [output_list[3]]}



def get_metadata_first_version(csv_file_path, mice=mice, paradigms=paradigms, networks=networks, cameras=cameras):
    """
    this was the first version of the get_metadata func
    but it is long and ugly
    """
    
    csv_file_path = csv_file_path.lower()
    mouse = ""
    paradigm = ""
    network = ""
    camera = ""
    for i in mice:
        if check_string_in_string(full_string=csv_file_path, part_string=i):
            mouse = i
            mouse = mouse.replace("_","")
            break
    for i in paradigms:
        if check_string_in_string(full_string=csv_file_path, part_string=i):
            paradigm = i
            break
    for i in networks:
        if check_string_in_string(full_string=csv_file_path, part_string=i):
            network = i
            break
    for i in cameras:
        if check_string_in_string(full_string=csv_file_path, part_string=i):
            camera = i
            break
    return {"Mouse": [mouse],"Paradigm": [paradigm],"Network": [network], "Camera": [camera]}

def get_metadata_second_version(csv_file_path, mice=mice, paradigms=paradigms, networks=networks, cameras=cameras):
    """
    this was the first version of the get_metadata func
    but it could still be better
    """
    metadata_list = [mice, paradigms, networks, cameras]
    output_list = ["","","",""]
    csv_file_path = csv_file_path.lower()
    for i in range(len(metadata_list)):
        for p in range(len(metadata_list[i])):
            if check_string_in_string(full_string=csv_file_path, part_string=(metadata_list[i])[p]):
                output_list[i] = (metadata_list[i])[p]
                break
    output_list[0] = output_list[0].replace("_","") #removes the underscores from the mouse number (they are need to avoid confusion with other numbers in the filename)
    return {"Mouse": [output_list[0]],
            "Paradigm": [output_list[1]],
            "Network": [output_list[2]], 
            "Camera": [output_list[3]]}









