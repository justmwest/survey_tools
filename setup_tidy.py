# -*- coding: utf-8 -*-
"""
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
import os, pandas#, scipy.stats
# import matplotlib.pyplot as plt
# import numpy as np


##### Importing the messy data #####
filename = "Master_file_tidydataset_JW_2023-02-03.xlsx"
directory  =  os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'data'))
filepath = directory + "/" + filename

#sheet2 is not needed
sheet1 = pandas.read_excel(filepath, sheet_name=0, header=None)


##### Parsing the Data #####

def get_var_list():
    '''
    Returns
    -------
    var_list : list
        Just a list of variables that can be used to call from the dictionary.
    '''
    var_list = [sheet1[i][0] for i in range(0,sheet1.shape[1])] # this will be the reference list
    return var_list


def get_data_dict():
    '''
    Returns
    -------
    data_dict : Dictionary
        A dictionary containing the variables (keys) and the responses.
    '''
    excel_file = pandas.ExcelFile(filepath)
    df = excel_file.parse(excel_file.sheet_names[0])
    data_dict=df.to_dict(orient='list')
    return data_dict


def print_var_list():
    '''
    Just a way to display the column numbers with the questions.
    '''
    var_list = get_var_list()
    for i in range(0,len(var_list)):
        print(i, end=" ")
        print(var_list[i])

##### Useful lists #####

data_dict = get_data_dict()
var_list = get_var_list()


#print(sheet1.to_dict()[4])

# variable_list, question_list, question_type_list, data_type_list, value_code_list = [sheet1[i][1:] for i in [0,1,2,3,4]]
# data_array = [sheet2[:][i] for i in range(0, len(variable_list))]
# ids = data_array[0][1:]





