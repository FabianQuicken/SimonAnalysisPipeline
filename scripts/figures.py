import matplotlib.pyplot as plt
import numpy as np 
import seaborn as sns
import pandas as pd
from mathematics import fill_missing_values
from get_metadata import get_metadata

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
    
def prepare_data_line_plot(file_list, right_obj, left_obj, sort_for_mouse = False, mouse= str, paradigm = str):

    all_data_points = []
    mice = []
    dates = []

    for file in file_list:

        metadata = get_metadata(file)
        if sort_for_mouse:
            if paradigm in metadata["paradigm"].lower() and metadata["mouse"] == mouse:
                print(metadata["date"])
                df = pd.read_csv(file)
                df_copy = df.copy()
                data_points = []

                if "right" in metadata["paradigm"]:
                    urine_stim = df_copy[f"is_investigating_{right_obj}"]
                elif "left" in metadata["paradigm"]:
                    urine_stim = df_copy[f"is_investigating_{left_obj}"]

                mice.append(metadata["mouse"])
                dates.append(metadata["date"])

                urine_stim = np.array(urine_stim)
                print(np.nansum(urine_stim))
                total_length = len(urine_stim)
                part_size = total_length // 10

                for i in range(10):
                    start_index = i * part_size
                    end_index = (i + 1) * part_size
                    part_sum = np.nansum(urine_stim[start_index:end_index])
                    data_points.append(part_sum)

                all_data_points.append(data_points)

        else:
            if paradigm in metadata["paradigm"].lower():

                df = pd.read_csv(file)
                df_copy = df.copy()
                data_points = []

                if "right" in metadata["paradigm"]:
                    urine_stim = df_copy[f"is_investigating_{right_obj}"]
                elif "left" in metadata["paradigm"]:
                    urine_stim = df_copy[f"is_investigating_{left_obj}"]

                mice.append(metadata["mouse"])
                dates.append(metadata["date"])

                urine_stim = np.array(urine_stim)
                print(np.nansum(urine_stim))
                total_length = len(urine_stim)
                part_size = total_length // 10

                for i in range(10):
                    start_index = i * part_size
                    end_index = (i + 1) * part_size
                    part_sum = np.nansum(urine_stim[start_index:end_index])
                    data_points.append(part_sum)

                all_data_points.append(data_points)

    return all_data_points, mice, dates




def plot_multiple_line_plots(data, mice, dates, paradigm, save_path, sort_for_mouse=False, mouse=str):
    """
    Plot multiple line plots on the same diagram for given CSV files and column index.

    Parameters:
    - csv_files: List of file paths to CSV files.
    - column_index: Index of the column to extract (zero-based index).
    """


    # Create x-values (assuming 10 consecutive points)
    x_values = list(range(1, 11))  # Generate x-values from 1 to 10

    # Define color map from yellow to purple
    # colormaps for black background: viridis, plasma, cividis
    colors = plt.cm.viridis(np.linspace(0, 1, len(data)))

    # Plot line plots for each CSV file
    plt.figure(figsize=(10, 8))  # Optional: set figure size
    for i, data_points in enumerate(data):
        plt.plot(x_values, data_points, label=f'mouse:{mice[i]}; date:{dates[i]}', color=colors[i])  # Plot each line plot with a label

    # Set background color to black
    plt.gca().set_facecolor('black')  # Set background color to black

    # Add labels, title, legend, and grid
    plt.title(f'Investigation time of mice in 1 min bins, paradigm: {paradigm}')
    plt.xlabel('Minute')
    plt.ylabel('Frames with investigation')
    #plt.legend()
    
    #plt.grid(True, color="gray")  # Optional: add grid
    sns.despine()

    if sort_for_mouse:
        # Customize legend position (move legend to upper right corner)
        plt.legend(loc='upper right', bbox_to_anchor=(1.0, 1.0), labelcolor='white', facecolor="black")
        # Adjust layout to ensure all plot elements are within the figure boundaries
        plt.tight_layout()
        plt.savefig(f"{save_path}{paradigm}_mouse_{mouse}.svg", format='svg', facecolor="black")
    else:
        # Customize legend position (move legend to the right)
        plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), title='Legend', labelcolor='black')
        # Adjust layout to ensure all plot elements are within the figure boundaries
        plt.tight_layout()
        plt.savefig(f"{save_path}{paradigm}.svg", format='svg', facecolor="black")
    plt.show()
    
    

    
def plot_multiple_line_plots_chatgpt(data, paradigm, sort_for_mouse=False, mouse=str):
    """
    Plot multiple line plots on the same diagram with custom aesthetics.

    Parameters:
    - data: List of lists, each containing data points for a line plot.
    - paradigm: Name of the paradigm for plot title.
    - sort_for_mouse: Flag to sort data by mouse (default: False).
    - mouse: Mouse identifier for plot title (optional).
    
    Returns:
    - fig: Matplotlib figure object containing the plot.
    """

    # Create x-values (assuming 10 consecutive points)
    x_values = np.arange(1, 11)  # Generate x-values from 1 to 10

    # Define color map from yellow to purple
    colors = plt.cm.magma(np.linspace(0, 1, len(data)))  # Generate colors based on number of lines

    # Plot line plots for each dataset with custom colors
    fig, ax = plt.subplots(figsize=(10, 8))  # Create figure and axis
    for i, data_points in enumerate(data):
        ax.plot(x_values, data_points, label=f'CSV {i+1}', color=colors[i])  # Plot with custom color

    # Set background color to black
    ax.set_facecolor('black')  # Set background color to black

    # Add labels, title, legend, and grid
    ax.set_title(f'Investigation Time of Mice in 1-Minute Bins ({paradigm})', color='white')  # Set title and text color
    ax.set_xlabel('Minute', color='white')  # Set x-axis label and text color
    ax.set_ylabel('Frames with Investigation', color='white')  # Set y-axis label and text color

    # Customize legend position (move legend to upper right corner)
    legend = ax.legend(loc='upper right', title='Legend', title_color='white', labelcolor='white')  # Create legend
    legend.set_facecolor('black')  # Set legend background color to black
    for text in legend.get_texts():
        text.set_color('white')  # Set legend label colors

    ax.grid(True, color='gray', linestyle='--', linewidth=0.5)  # Optional: add grid with custom style
    sns.despine()

    # Return the figure object
    return fig
