import matplotlib.pyplot as plt
import numpy as np 

def normalize(data_list):
    for data in data_list:
        data = (data / len(data))
    return data_list
  
def eventplot(data_list=list,, lineoffsets=list, metadata):
    plt.figure(figsize=(10,6))
    for data in data_list:
        data = np.where(data == 1)[0]
    data_list = normalize(data)
