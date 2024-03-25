import matplotlib.pyplot as plt
import numpy as np 
import seaborn as sns

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
    based on the experiment metadata.
    """

    # initialize figure
    plt.figure(figsize=(14,6))
    
    # reduce the dimensionality of the data to make the plots clearer
    # since a bin for each frame would not work
    for i in range(len(data_list)):
        print(len(data_list[i]))
        data_list[i] = data_list[i][::skip_frame_stepsize]
        print(len(data_list[i]))

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


def pieplot(metadata, data_list, save_name=str, colors=[], labels=[]):
    
    plt.figure(figsize=(6,6))
    exp_len = len(data_list[0]) / 3600
    print(exp_len)
    for i in range(len(data_list)):
        data_list[i] = np.nansum(data_list[i])
        print(data_list[i])       

    
    plt.pie(data_list, explode=(0.01,0.01), labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
    plt.title(f"Mouse: {metadata['mouse']}; Paradigm: {metadata['paradigm']}; Date: {metadata['date']}") 
    plt.savefig(f"./testing/{metadata['date']}_{metadata['mouse']}_{metadata['paradigm']}_{save_name}.svg", format='svg')
    plt.show()
