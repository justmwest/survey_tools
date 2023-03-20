# -*- coding: utf-8 -*-
"""


Spyder Editor

This is a temporary script file.

This is the installation instruction file.
I first installed anaconda then made a new environment called survey
Then opened spyder

The path is to this file is /Volumes/1TB\ WD\ Elements/Documents/NJF/Survey\ Results\setup.py
The excel files containing the survey data are in this same directory.

Setup
Since this is a new environment, trying, say import matplotlib, will not work. 
The modules are not installed.
To install them you cannot simply pip install matplotlib from here.
But you *can* run it from the console.
run:    pip install matplotlib, numpy, pandas, openpyxl, scipy (not sure if it works in sequence like this)
Then restart the console.
Now we can get to work.

Errors:
    Missing optional dependency 'openpyxl'.  Use pip or conda to install openpyxl.
        Got this error when trying to use pandas.read_excel for the first time. Added to the install list above.
"""
##### Important packages #####
import os, pandas, scipy.stats
import matplotlib.pyplot as plt
import numpy as np


##### Importing the messy data #####
directory  =  os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'data'))
filename = "pydata.xlsx"
filepath = directory + "/" + filename

sheet1, sheet2 = [pandas.read_excel(filepath, sheet_name=i, header=None) for i in [0, 1]]


##### Parsing the Data #####
# sheet[columns][rows]

variable_list, question_list, question_type_list, data_type_list, value_code_list = [sheet1[i][1:] for i in [0,1,2,3,4]]
data_array = [sheet2[:][i] for i in range(0, len(variable_list))]
ids = data_array[0][1:]

# Next steps set up a dictionary (or dictionaries) where the variable_list
# value can be passed to return the question, type etc. 

variable_dict = {}
for i in range(1,len(variable_list)+1):
    variable_dict[variable_list[i]] = [question_list[i], question_type_list[i], data_type_list[i], value_code_list[i]]
# print(variable_dict["VAR00"])

data_dict = {}
for i in range(0, len(variable_list)):
    data_dict[data_array[i][0]] = data_array[i][1:]
# print(data_dict["ID"])

yes_no_dict = {
    "Yes" : 1,
    "No" : 2,
    "Not sure" : 0,
    "Not Applicable" : 0,
    "Prefer not to say" : 0
    }

gender_dict = {
    "Female" : 1,
    "Male" : 2,
    "Non-binary" : 3,
    "Prefer not to say" : 4
    }

agree_disagree_dict = {
    'Strongly Disagree (very untrue about me)' : 1,
    'Disagree (somewhat untrue about me)' : 2,
    'Neither agree nor disagree' : 3,
    'Agree (somewhat true about me)' : 4,
    'Strongly Agree (very true about me)' : 5,
    'Not Applicable' : 0
    }

academic_dict = {
    'A Swedish academic, or' : 1, 
    'An international academic in Sweden ' : 2
    }

numeric_dict = [i for i in range(0,1000)]



# assigning var dicts
yes_no_vars = []
for key in variable_dict:
    if variable_dict[key][3] == '1 = Yes\n2 = No\n0 = Not sure' or \
        variable_dict[key][3] == '1 = Yes\n2 = No' or \
        variable_dict[key][3] == '1 = Yes\n2 = No\n0 = Prefer not to say' or \
        variable_dict[key][3] == '1 = Yes\n2 = No\n0 = Not Applicable':
        yes_no_vars.append(key)

gender_vars = []
for key in variable_dict:
    if variable_dict[key][3] == \
        '1 = Female\n2 = Male\n3 = Non-binary\n4 = Prefer not to say':
        gender_vars.append(key)
        
agree_disagree_vars = []
for key in variable_dict:
    if variable_dict[key][3] == \
        '1 = Strongly Disagree (very untrue about me)\n2 = Disagree (somewhat untrue about me)\n3 = Neither agree nor disagree\n4 = Agree (somewhat true about me)\n5 = Strongly Agree (very true about me)\n0 = Not Applicable':
        agree_disagree_vars.append(key)

academic_vars = []
for key in variable_dict:
    if variable_dict[key][3] == \
        '1 = A Swedish academic, or\n2 = An international academic in Sweden ':
        academic_vars.append(key)
            
numeric_vars = []
for key in variable_dict:
    if variable_dict[key][1] == \
        'Numeric - Field':
        numeric_vars.append(key)

# functions

def get_var(variable_number):
    '''
    Parameters
    ----------
    variable_number : Int or Str
        Takes an int or str input number and converts it to VAR00 format.

    Returns
    -------
    Str in the format VAR00.
    '''
    # Covert to string
    if type(variable_number) == int:
        str_number = str(variable_number)
    elif type(variable_number) == str:
        str_number = variable_number
    elif variable_number == None:
        #print("Error: NoneType")
        return None
    else:
        print("Error: type of query is not str or int.")
    
    # Convert to var format
    if len(str_number) == 1:
        var_str = "VAR0"+str_number
    elif len(str_number) == 2:
        var_str = "VAR"+str_number
    else:
        var_str = str_number
        #print("Error: query is too long or already formatted. Must be one or two digits")
    # print(var_str)
    return var_str

def get_info(variable_number):
    '''

    Parameters
    ----------
    variable_number : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    '''
    var_query = get_var(variable_number)
    print(variable_dict[var_query])
    
def get_dict(variable_number, inverted = False):
    '''
    Parameters
    ----------
    variable_number : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    '''
    var_query = get_var(variable_number)
    tmp_dict = {}
    
    if var_query in yes_no_vars:
        tmp_dict = yes_no_dict
    elif var_query in agree_disagree_vars:
        tmp_dict = agree_disagree_dict
    elif var_query in gender_vars:
        tmp_dict = gender_dict
    elif var_query in academic_vars:
        tmp_dict = academic_dict
    elif var_query in numeric_vars:
        tmp_dict = numeric_dict
    else:
        return None
    
    if inverted == True and var_query not in numeric_vars:
        inv_dict = {v: k for k, v in tmp_dict.items()}
        return inv_dict
    else:
        return tmp_dict
    
def get_data(variable_number, numeric=True):
    '''
    Parameters
    ----------
    variable_number : Int or Str
        This function looks up the question associated with the variable number
        and returns the data for that question.

    Returns
    -------
    Data from sheet 2.
    
    TODO: I want to add a gender option here. Get data from males, females, nonbinary etc.

    '''
    var_query = get_var(variable_number)
    tmp_dict = get_dict(var_query)
    if tmp_dict == None: numeric = False
    
    # Find the question
    for i in variable_list:
        if i == var_query:
            if numeric == True:
                question = variable_dict[var_query][0]
                converted_data = []
                unconverted_data = data_dict[question]
                for datum in unconverted_data:
                    converted_data.append(tmp_dict[datum])
                return converted_data
            else:
                question = variable_dict[var_query][0]
            # print(question)
                return data_dict[question]
    
def get_count(variable_number, frequency_mode=False):
    '''
    Parameters
    ----------
    variable_number : str, int
        Describes the variable number that  you want data for.

    Returns
    -------
    A list of occurrences for each numeric value.
    Example:
        legend: [0,1,2,3,4,5] (this is the order of responses)
        output: [351, 120, 96, 4, 6] (not sorted by size, but by response value)
        freq. mode: [0.68, 0.25, 0.10, 0.05, 0.01] (this should add up to 1 but I'm lazy)
    '''
    var_query = get_var(variable_number)
    data_list = get_data(var_query)
    occurence_dict = {}
    for value in data_list:
        if value in occurence_dict:
            occurence_dict[value] += 1
        else:
            occurence_dict[value] = 1
    
    # set up frequencies if requested
    if frequency_mode == True:
        frequency_dict = {}
        for i in occurence_dict:
            frequency_dict[i] = occurence_dict[i]/len(data_list)
        output_dict = frequency_dict
    else:
        output_dict = occurence_dict
    
    # sort the keys in ascending order
    sorted_dict = {}
    for i in sorted(output_dict):
        sorted_dict[i] = output_dict[i]
    return sorted_dict
    
    
# set up auxiliary plotting functions
def plot_bar(input1, input2=None, width=0.4, frequency_mode=False):
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
    '''
    input_var1, input_var2 = [get_var(input1), get_var(input2)]
    input_dict1, input_dict2 = [get_dict(input_var1,True), get_dict(input_var2,True)]
    
    # check number of inputs
    if input2 == None:
        input_list = [input1]
    else:
        input_list = [input1, input2]
    
    # assemble the data
    bar_data = []
    for tmp_input in input_list:
        if frequency_mode == True:
            input_dict = get_count(tmp_input, frequency_mode=True)
        else:
            input_dict = get_count(tmp_input)
        input_x , input_y = [[],[]]
            
        for i in input_dict:
            input_x.append(i)
            input_y.append(input_dict[i])
        bar_data.append([input_x , input_y])
    
    # set up plots
    if input2 == None:  
        plt.bar(bar_data[0][0], bar_data[0][1], width, label = input_var1)
        plt.xticks(bar_data[0][0], [input_dict1[i] for i in bar_data[0][0]], rotation=45, ha='right')
        plt.title(input_var1+" - "+variable_dict[input_var1][0])
        
    else:
        plt.bar([x-width/2 for x in bar_data[0][0]], bar_data[0][1], width, label = input_var1)
        plt.bar([x+width/2 for x in bar_data[1][0]], bar_data[1][1], width, label = input_var2)
        if input_dict1 == input_dict2:
            plt.xticks(bar_data[0][0], [input_dict1[i] for i in bar_data[0][0]], rotation=45, ha='right')
        plt.title(input_var1+" - "+variable_dict[input_var1][0]+"\n"
                  +input_var2+" - "+variable_dict[input_var2][0])
        
    if frequency_mode==True:
        plt.ylabel('Frequency (counts/responses)')
    else:
        plt.ylabel('Counts')
    plt.show()
    
    
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



def get_r_squared(input1, input2=None, verbose=False):
    '''
    Parameters
    ----------
    input1 : int or str
        describes the var number
    input2 : TYPE, optional
        describes the var number. The default is None.

    Returns
    -------
    prints the r squared value of the correlation between inputs 1 and 2

    '''
    input_var1, input_var2 = [get_var(input1), get_var(input2)]
    data1, data2 = [np.array(get_data(i)).astype(float) for i in [input1, input2]]
    stats = scipy.stats.linregress(data1, data2)
    if verbose == True:
        print(input_var1+" vs. "+input_var2)
        print("r^2 = "+str(stats[2]))
    return stats[2]


# Sandbox


# show all the plots    
# for i in variable_list:
#     try:
#         plot_data(get_data(i))
#     except:
#         print("Error on "+get_var(i))

