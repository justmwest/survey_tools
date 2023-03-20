#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 11 17:46:02 2022

@author: Justin

plotting functions
so far has just been copied from setup.py.

"""
from setup_tidy import var_list, data_dict
from dictionaries import str_to_int, get_dict
import matplotlib.pyplot as plt
from retrieval_functions import count_responses

# set up auxiliary plotting functions
def plot_bar(input1, input2=None, width=0.4, frequency_mode=False, ignore_zero=True):
    '''
    Parameters
    ----------
    input_data : Int, Str.
        Describes the variable number you want to plot.
    input_data2 : TYPE, optional
        Describes the variable number you want to plot. The default is None.
        If left out, the function will only plot one.

    Returns
    -------
    A bar chart that can be used as a substitute for the default scatter.
    notes: check here: https://www.geeksforgeeks.org/plotting-multiple-bar-charts-using-matplotlib-in-python/
    TODO: Does something weird with numeric data. xticks show up only at populated values,
    which makes for weird cases like VAR15. 
    TODO: Make ignore zero option.
    TODO: figure out how to return a key from a value for xlabels. 
        
    '''
    # check number of inputs
    if input2 == None:
        input_list = [input1]
    else:
        input_list = [input1, input2]
    
    # Get variables, data, and dictionaries
    input_var_list = [var_list[i] for i in input_list]
    input_data_list = [data_dict[i] for i in input_var_list]
    counts_dict_list = [count_responses(i) for i in input_data_list]
    new_dict_list = [str_to_int(i) for i in counts_dict_list]
    legend_dict_list = [get_dict(i) for i in input_data_list] # was imported for labels.
    
    # assemble the data
    bar_data = []
    for index in range(0,len(input_list)):
        
        # Frequency Mode
        # I don't have frequency mode on count_responses yet
        # if frequency_mode:
        #     input_dict = retrieval_functions.count_responses(tmp_input, frequency_mode=True)
        # else:
        #     input_dict = retrieval_functions.count_responses(tmp_input)
        
        # Ignore Zero
        # if ignore_
        
        # should be a dict with ints for keys and int or float for values
        new_dict = new_dict_list[index]
        
        # Make the key x and the value y.
        # Ignore zero should go here.
        input_x , input_y = [[],[]]
        for key in list(new_dict.keys()):
            input_x.append(key)
            input_y.append(new_dict[key])
            

        
        bar_data.append([input_x , input_y])
        
    # print(bar_data)
    
    # Set up labels

    
    # set up plots
    if input2 == None:
        
        xdata, ydata = bar_data[0]
        
        plt.bar(xdata, ydata, width, label = input_var_list[0])

        # x labels
        # There's an issue here where the keys that have the same numeric value are combined
        # e.g., N/A and nan are both converted to zero. So the labels are longer than the data.
        # But then how to robustly get labels?
        # I need to convert str back to int. Which is ridiculous. Numeric labels for now.
        # Would work if I could return a key from a value. 
        legend_keys = list(legend_dict_list[0].keys())
        legend_values = list(legend_dict_list[0].values())
        
        # Hacky way to return first key for value
        xlabels = []
        have_been_checked=[]
        for numeric_x_index in range(0,len(xdata)): # For every value in xdata,
            for value_index in range(0,len(legend_values)): # Check every legend_dict value for a match,
                if legend_values[value_index] == xdata[numeric_x_index]: 
                    if legend_values[value_index] not in have_been_checked: # but only if it's not already there.
                        have_been_checked.append(legend_values[value_index]) 
                        xlabels.append(legend_keys[value_index])
        # print(xlabels)
        plt.xticks(xdata, xlabels, rotation=45, ha='right')
        
        plt.title(input_var_list[0])
        
    else:
        plt.bar([x-width/2 for x in bar_data[0][0]], bar_data[0][1], width, label = input_var1)
        plt.bar([x+width/2 for x in bar_data[1][0]], bar_data[1][1], width, label = input_var2)
        if input_dict1 == input_dict2:
            plt.xticks(bar_data[0][0], [input_dict1[i] for i in bar_data[0][0]], rotation=45, ha='right')
        plt.title(input_var1+"\n"
                  +input_var2)
        
    if frequency_mode==True:
        plt.ylabel('Frequency (counts/responses)')
    else:
        plt.ylabel('Counts')
    return plt.show()
   

### Testing Area ###
# plot_bar(73)

# for i in range(0,len(var_list)):
#     try:
#         plot_bar(i)
#         print(str(i)+" worked!")
#     except:
#         print(str(i)+" did not work!")
####################
    
def plot_simple(x, y, xlabels=None, ylabel=None, title=None, width=0.4):
    '''
    a plotting function that is more malleable.
    
    x and y are lists of values. x can be list of strings.
    xlabels must be list of strings. 
    ylabels must be str.
    title must be str. 
    width adjusts bar width as a fraction of the space between two centers.
    
    returns plt.show()
    '''
    
    plt.bar(x, y, width, label = title)
    plt.xticks(x, xlabels, rotation=45, ha='right')
    plt.ylabel(ylabel)
    plt.title(title)
    return plt.show()
            
# Plot the data
def plot_data(input1, input2=None, bar=False, frequency_mode=False):
    '''
    Parameters
    ----------
    input_data : Int, Str.
        Describes the variable number you want to plot.
    input_data2 : Int, Str, optional
        Describes the variable number you want to plot. The default is None.
        If left out, the function will only plot one.
    bar: bool
        defines whether or not to use the auxiliary bar chart function to plot.

    Returns
    -------
    A scatter plot with the data. 
    Next:It would be cool to make this return violin plots or swarm plots,
    Though it won't get around the issue that there's only data points at discrete values. 
    How best to show this kind of data? Bars?

    '''
    input_var1, input_var2 = [get_var(input1), get_var(input2)]
    
    if bar == True:
        if frequency_mode == True:
            plot_bar(input_var1, input_var2, frequency_mode=True)
        else:
            plot_bar(input_var1, input_var2)
    else:
        if input_var2 != None:
            plt.scatter(get_data(input1), get_data(input2))
            plt.title(input_var1+" vs. "+input_var2)
            plt.xlabel(variable_dict[input_var1][0])
            plt.ylabel(variable_dict[input_var2][0])
        else:
            plt.plot(ids, get_data(input_var1))
            plt.title(input_var1+" - "+variable_dict[input_var1][0])
        plt.show()