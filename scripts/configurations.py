
# do you know how many pixels a cm has in your camera view? 
# for topview simons setup = 34.77406
# for frizis philadelphia topview setup = 8.21875 
pixel_per_cm=8.21875 

mice = ("_1_", "_2_", "_95_", "_104_", "_105_", "_117_")
networks = ("resnet50_dlc1feb20shuffle1_300000", "notavailableyet")
paradigms = ("habituation_urinright", "experiment_urinright", "habituation_urinleft", "experiment_urinleft",
             "habituation1", "habituation2", "habituation3", "habituation4", "habituation5", "habituation6")
cameras = ("top", "side, topview, sideview")
dlc_petridish_layout_simon = ("nose_x", "nose_y", "nose_likelihood",
                  "left_ear_x", "left_ear_y", "left_ear_likelihood",
                  "right_ear_x", "right_ear_y", "right_ear_likelihood",
                  "lateral_left_x", "lateral_left_y", "lateral_left_likelihood",
                  "center_x", "center_y", "center_likelihood",
                  "lateral_right_x", "lateral_right_y", "lateral_right_likelihood",
                  "tailbase_x", "tailbase_y", "tailbase_likelihood",
                  "left_dish_x", "left_dish_y", "left_dish_likelihood",
                  "right_dish_x", "right_dish_y", "right_dish_likelihood",
                  "topleft_x", "topleft_y", "topleft_likelihood",
                  "topright_x", "topright_y", "topright_likelihood",
                  "bottomleft_x", "bottomleft_y", "bottomleft_likelihood",
                  "bottomright_x", "bottomright_y", "bottomright_likelihood"
                  )
                  
dlc_petridish_layout_fabi = ("leftear_x", "leftear_y", "leftear_likelihood",
                        "rightear_x", "rightear_y", "rightear_likelihood",
                        "snout_x", "snout_y", "snout_likelihood",
                        "centroid_x", "centroid_y", "centroid_likelihood",
                        "lateralleft_x", "lateralleft_y", "lateralleft_likelihood",
                        "lateralright_x", "lateralright_y", "lateralright_likelihood",
                        "tailbase_x", "tailbase_y", "tailbase_likelihood",
                        "topleft_x", "topleft_y", "topleft_likelihood",
                        "topright_x", "topright_y", "topright_likelihood",
                        "bottomright_x", "bottomright_y", "bottomright_likelihood",
                        "bottomleft_x", "bottomleft_y", "bottomleft_likelihood",
                        "leftpetridish_x", "leftpetridish_y", "leftpetridish_likelihood",
                        "rightpetridish_x", "rightpetridish_y", "rightpetridish_likelihood"
                        )

dlc_mighty_snicket_layout_simon = ("nose_x", "nose_y", "nose_likelihood",
                  "left_ear_x", "left_ear_y", "left_ear_likelihood",
                  "right_ear_x", "right_ear_y", "right_ear_likelihood",
                  "lateral_left_x", "lateral_left_y", "lateral_left_likelihood",
                  "center_x", "center_y", "center_likelihood",
                  "lateral_right_x", "lateral_right_y", "lateral_right_likelihood",
                  "tailbase_x", "tailbase_y", "tailbase_likelihood",
                  "left_snicket_x", "left_snicket_y", "left_snicket_likelihood",
                  "right_snicket_x", "right_snicket_y", "right_snicket_likelihood",
                  "topleft_x", "topleft_y", "topleft_likelihood",
                  "topright_x", "topright_y", "topright_likelihood",
                  "bottomleft_x", "bottomleft_y", "bottomleft_likelihood",
                  "bottomright_x", "bottomright_y", "bottomright_likelihood"
                  )

dlc_petridish_layout_frizi = ("leftear_x", "leftear_y", "leftear_likelihood",
                        "rightear_x", "rightear_y", "rightear_likelihood",
                        "snout_x", "snout_y", "snout_likelihood",
                        "centroid_x", "centroid_y", "centroid_likelihood",
                        "lateralleft_x", "lateralleft_y", "lateralleft_likelihood",
                        "lateralright_x", "lateralright_y", "lateralright_likelihood",
                        "tailbase_x", "tailbase_y", "tailbase_likelihood",
                        "tailend_x", "tailend_y", "tailend_likelihood",
                        "leftpetrileft_x", "leftpetrileft_y", "leftpetrileft_likelihood",
                        "leftpetriright_x", "leftpetriright_y", "leftpetriright_likelihood",
                        "leftpetritop_x", "leftpetritop_y", "leftpetritop_likelihood",
                        "leftpetribottom_x", "leftpetribottom_y", "leftpetribottom_likelihood",
                        "rightpetrileft_x", "rightpetrileft_y", "rightpetrileft_likelihood",
                        "rightpetriright_x", "rightpetriright_y", "rightpetriright_likelihood",
                        "rightpetritop_x", "rightpetritop_y", "rightpetritop_likelihood",
                        "rightpetribottom_x", "rightpetribottom_y", "rightpetribottom_likelihood",
                        "cagetopleft_x", "cagetopleft_y", "cagetopleft_likelihood",
                        "cagetopright_x", "cagetopright_y", "cagetopright_likelihood",
                        "cagebottomleft_x", "cagebottomleft_y", "cagebottomleft_likelihood",
                        "cagebottomright_x", "cagebottomright_y", "cagebottomright_likelihood"
                        )

dlc_new_setup = ("nose_x", "nose_y", "nose_likelihood",
                        "head_x", "head_y", "head_likelihood",
                        "spine1_x", "spine1_y", "spine1_likelihood",
                        "spine2_x", "spine2_y", "spine2_likelihood",
                        "centroid_x", "centroid_y", "centroid_likelihood",
                        "spine3_x", "spine3_y", "spine3_likelihood",
                        "spine4_x", "spine4_y", "spine4_likelihood",
                        "tail1_x", "tail1_y", "tail1_likelihood",
                        "tail2_x", "tail2_y", "tail2_likelihood",
                        "tail3_x", "tail3_y", "tail3_likelihood",
                        "snicket_x", "snicket_y", "snicket_likelihood"
                        )