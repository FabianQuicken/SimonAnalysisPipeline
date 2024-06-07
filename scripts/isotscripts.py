import numpy as np


# overlayed event plot

array_gt = None
array_deg = None
array_dlc = None

# 3 arrays are read in 
# I need to check gt vs deg, gt vs dlc and deg vs dlc for overlay
# for plot I need to populate new arrays:
array_overlay_gt_dlc = np.zeros(len(array_gt))
array_overlay_gt_deg = np.zeros(len(array_gt))
array_overlay_dlc_deg = np.zeros(len(array_dlc))
array_dlc_fp = np.zeros(len(array_dlc))
array_deg_fp = np.zeros(len(array_deg))

for i in range(len(array_gt)):
    if array_gt[i] == 1 and array_dlc[i] == 1:
        array_overlay_gt_dlc[i] = 1
    else:
        array_overlay_gt_dlc[i] = 0

    if array_gt[i] == 0 and array_dlc[i] == 1:
        array_dlc_fp[i] = 1
    
    if array_gt[i] == 1 and array_deg[i] == 1:
        array_overlay_gt_deg[i] = 1
    else:
        array_overlay_gt_deg[i] = 0

    if array_dlc[i] == 1 and array_deg[i] == 1:
        array_overlay_dlc_deg[i] = 1
    else:
        array_overlay_dlc_deg[i] = 0



    

