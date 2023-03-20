#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 14 22:11:18 2022

@author: Justin
"""

# import setup_tidy
from setup_tidy import data_dict, var_list
from dictionaries import str_to_int, get_dict
from retrieval_functions import count_responses, count_by_year
from plotting_functions import plot_simple



# data_dict = setup_tidy.get_data_dict()
# var_list = setup_tidy.get_var_list() # import the list of variables

class var:
    def __init__(self, column_number):
        '''
        Column number is the column number in the tidy data.
        
        Would be nice to add a dict_selection variable to tell get_dict which dictionary to choose (4 for column 5 (age))
        '''
        self.column_number=column_number # Not sure if this is the best way but I need it for counts_by_year
        self.var = var_list[column_number] # returns the question as str
        
        self.values = data_dict[self.var] # raw data
        
        # Needs fix for column 5
        # self.int_values = str_to_int(self.values) # raw data converted to int
        
        # self.counts = count_responses(self.values)
        # self.int_counts=count_responses(self.int_values)
        self.legend = get_dict(self.values)
        
        

        
    def count(self, ignore_zero=False, frequency_mode=False, by_year=False, int_mode=False, xonly=False, yonly=False, combine_zero=False):
        '''
        Returns counts for self with various options.
        ignore_zero means values of zero will not be counted.
        frequency_mode means values will be returned as fractions of the total counts.
        int_mode means that they keys will be int instead of strings.
        xonly and yonly return lists. xonly takes precedence as they are mutually exclusive.
        '''
        
        if int_mode:
            tmp_values = self.int_values
        else: 
            tmp_values = self.values
        
        tmp_dict = count_responses(tmp_values, ignore_zero=ignore_zero, frequency_mode=frequency_mode, combine_zero=combine_zero)
        
        if xonly:
            return list(tmp_dict.keys())
        elif yonly:
            return list(tmp_dict.values())
        else:
            return tmp_dict
       
        
    def count_by_year(self, ignore_zero=False):
        '''
        Simple function to call count by year.
        TODO: add frequency mode.
        '''
        return count_by_year(self.column_number, ignore_zero=ignore_zero)    
        
        
        
        
    def plot(self, ignore_zero=False, frequency_mode=False):
        '''
        Plots instance of var.
        inputs ignore zero and frequency mode are bools that are described in var.count
        returns a basic plot.
        
        '''
        
        x = self.count(ignore_zero=ignore_zero, frequency_mode=frequency_mode, int_mode=True, xonly=True)
        y = self.count(ignore_zero=ignore_zero, frequency_mode=frequency_mode, int_mode=True, yonly=True)
        xlabels = self.count(ignore_zero=ignore_zero, frequency_mode=frequency_mode, int_mode=False, xonly=True, combine_zero=True)
        
        if frequency_mode:
            if ignore_zero:
                ylabel = 'Frequency (counts/non-zero responses)'
            else:
                ylabel = 'Frequency (counts/responses)'
        else:
            ylabel = 'Counts'
        
        title = self.var
        
        plot_simple(x, y, xlabels=xlabels, ylabel=ylabel, title=title)
        
        
### Test area ###

# temp = var(74)
# temp.plot()
        