import matplotlib.pyplot as plt
import numpy as np 
import seaborn as sns
import pandas as pd
from mathematics import fill_missing_values

def normalize(data_list, normalize_val, skip_frame_stepsize):
    """
    This is a normalization function that can only be used on data for eventplots. 
    Since eventplot data consists of arrays containing only the indixes where an event is present,
    their length is much shorter than the raw data - but the normalization must be performed with the 
    length of the original index. The original length must be passed to this func as a list.
    The function normalizes the data to minutes.
    Note: Only works with a 60fps recording
    """
    """
    for i in range(len(data_list)):
        data_list[i] = data_list[i] / ((normalize_val[i]))
    """
    for i in range(len(data_list)):
        data_list[i] = data_list[i] / (3600/skip_frame_stepsize) # division with stepsize, to calculate with respect to a downscaled array
    return data_list
  
def eventplot(metadata, data_list, lineoffsets, save_name=str, colors = ["r", "b", "g", "v"], skip_frame_stepsize=1):
    """
    This functions takes arrays filled with "1" or "0", and finds all indices with "1" which are declared as events.
    Beforehand, the data is downscaled via a stepsize to reduce the amount of bins presented in the eventplot, so the 
    graph will be clearer. Also the data is normalized to the experiment length. Finally, the functions creates an
    eventplot containing the data, labeling it based on the input lineoffsets argument. The figure is saved as .svg
    based on the experiment metadata plus a custom information tag, such as "investigation_behavior".
    """

    # initialize figure
    plt.figure(figsize=(14,6))
    
    # reduce the dimensionality of the data to make the plots clearer
    # since a bin for each frame would not work
    for i in range(len(data_list)):
        data_list[i] = data_list[i][::skip_frame_stepsize]
 

    # for the normalization: get the length of the arrays before they get filtered for present events 
    experiment_lens = []
    for i in range(len(data_list)):
        experiment_lens.append(len(data_list[i]))
    
    # get the events (event present = 1, event not present = 0)
    for i in range(len(data_list)):
        data_list[i] = np.where(data_list[i] == 1)[0]

    # normalize the data, here the length of the arrays befor filtering is needed
    data_list = normalize(data_list, experiment_lens, skip_frame_stepsize)

    # create the plots
    for i in range(len(data_list)):
        plt.eventplot(data_list[i], lineoffsets=lineoffsets[i], label=f'Line {i+1}', color=colors[i], linewidths=0.5)
    #plt.xlim(0,1)
    plt.xlabel('Experiment length [min]')
    plt.title(f"Mouse: {metadata['mouse']}; Paradigm: {metadata['paradigm']}; Date: {metadata['date']}")
    sns.despine()
    plt.gca().set_facecolor('black')
    plt.savefig(f"./testing/{metadata['date']}_{metadata['mouse']}_{metadata['paradigm']}_{save_name}.svg", format='svg')
    plt.show()


def pieplot(metadata, data_list, save_name=str, colors=["m","y"], labels=[]):
    """
    This function can be used to create pieplots for better visualizing behavior,
    e.g. whether a mouse preferred the left, or the right cagehalf.
    Standard colors are magenta and yellow. The fig is saved as .svg based on the experiment
    metadata plus a custom information tag, such as "side_pref".
    """
    plt.figure(figsize=(6,6))
    #exp_len = len(data_list[0]) / 3600
    #print(exp_len)
    for i in range(len(data_list)):
        data_list[i] = np.nansum(data_list[i])
        print(data_list[i])       

    
    plt.pie(data_list, explode=(0.01,0.01), labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
    plt.title(f"Mouse: {metadata['mouse']}; Paradigm: {metadata['paradigm']}; Date: {metadata['date']}") 
    plt.savefig(f"./testing/{metadata['date']}_{metadata['mouse']}_{metadata['paradigm']}_{save_name}.svg", format='svg')
    plt.show()

def plot_cum_dist(metadata, arr, save_name=str, color=str):
    print(np.nansum(arr))
    plt.figure(figsize=(6,6))
    arr = arr[~np.isnan(arr)]
    cum_dist = np.cumsum(arr)
    time_points = np.arange(len(arr))
    time_points = time_points/len(time_points)*10
    print(len(time_points))

    plt.plot(time_points, cum_dist, color=color)
    plt.fill_between(time_points, 0, cum_dist, alpha=0.3, color=color)
    plt.ylim(0,(1.5*cum_dist[-1]))
    plt.xlim(0,time_points[-1])
    plt.xticks([0,time_points[-1]])
    plt.xlabel('time[min]')
    plt.ylabel('distance[m]')
    sns.despine()
    plt.title(f"Mouse: {metadata['mouse']}; Paradigm: {metadata['paradigm']}; Date: {metadata['date']}") 
    plt.savefig(f"./testing/{metadata['date']}_{metadata['mouse']}_{metadata['paradigm']}_{save_name}.svg", format='svg')
    plt.show()


def plot_distance_val(metadata, data_list=list, save_name=str, colors=list , labels=list, skip_frame_stepsize=40):
    plt.figure(figsize=(14,6))
    time_points = np.arange(len(data_list[0]))
    for i in range(len(data_list)):
        data_list[i] = fill_missing_values(data_list[i])
    for i in range(len(data_list)):
        data_list[i] = data_list[i][::skip_frame_stepsize]
    time_points = time_points[::skip_frame_stepsize]
    
    time_points = time_points/3600
    try:
        df = pd.DataFrame({'index': time_points, 'arr1': data_list[0], 'arr2': data_list[1]})
        df.dropna()
        arr1 = df['arr1']
        arr2 = df['arr2']
    except:
        df = pd.DataFrame({'index': time_points, 'arr1': data_list[0]})
        df.dropna()
        arr1 = df['arr1']
    time_points = df['index']
    
    try:
        plt.plot(time_points, arr1, color=colors[0])
        plt.plot(time_points, arr2, color=colors[1])
    except:
        plt.plot(time_points, arr1, color=colors[0])
    plt.gca().set_facecolor('black')
    plt.xlabel('Experiment length [min]')
    plt.title(f"Mouse: {metadata['mouse']}; Paradigm: {metadata['paradigm']}; Date: {metadata['date']}")
    sns.despine()
    plt.savefig(f"./testing/{metadata['date']}_{metadata['mouse']}_{metadata['paradigm']}_{save_name}.svg", format='svg')
    plt.show()

    

