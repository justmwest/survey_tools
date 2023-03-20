#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 17:50:23 2022

@author: justin
"""

import numpy as np
import random

# This dictionary returns a numeric value when a string is called
# Use the form gender_dict["Female"]
gender_dict = {
    "Female" : 1,
    "female" : 1,
    "Male" : 2,
    "male" : 2,
    "Non-binary" : 3,
    "Prefer not to say" : 4,
    "Other" : 5,
    "nan" : 0,
    np.nan : 0
    }

partnership_dict = {
    'Partner' : 1,
    'Single' : 2,
    np.nan : 0
    }

yes_no_dict = {
    "Yes" : 1,
    "No" : 2,
    "Not sure" : 0,
    "Not Applicable" : 0,
    "Prefer not to say" : 0,
    'nan' : 0,
    np.nan : 0
    }

agree_disagree_dict = {
    'Strongly Disagree (very untrue about me)' : 1,
    'Strongly disagree' : 1, 
    'Disagree (somewhat untrue about me)' : 2,
    'Disagree' : 2,
    'Neither agree nor disagree' : 3,
    'Agree (somewhat true about me)' : 4,
    'Agree' : 4,
    'Strongly Agree (very true about me)' : 5,
    'Strongly agree' : 5,
    'Not Applicable' : 0,
    np.nan : 0
    }

age_dict={
    '¨36' : 36,
    '30+' : 0,
    'not important ' : 0,
    'na' : 0, 
    'Prefer not to say' : 0,
    2 : 0,
    120 : 0,
    359 : 0,
    123 :0,
    355 : 0,
    np.nan : 0
    }

age_category_dict = {
    '≥41' : 5, 
    '> 41' : 5,
    '36-40' :4,
    '36 - 40' : 4, 
    '35-41' : 4, 
    '31-35' : 3, 
    '31 - 35' : 3, 
    '26-30' : 2, 
    '26 - 30' : 2, 
    '≤25' : 1, 
    '< 25' : 1,
    np.nan : 0
    }


# Make a mega dictionary containing all keys and values
dicts = [agree_disagree_dict, yes_no_dict, partnership_dict, gender_dict, age_dict, age_category_dict]
master_dict = {}
for dictionary in dicts:
    for key in list(dictionary.keys()):
        master_dict[key] = dictionary[key]
        
        
### Functions ###
def get_dict(input_list, user_choice=True, override=None):
    '''
    Input: a list of data as strings.
    if exact match not found one can select from a list, or
    if user_choice is false, the first match is selected.
    override allows the user to select the dictionary manually (position as int)
    Output: the corresponding data in numerical form.
    '''
    # Sample x random responses from data
    # if len(input_list) > 100:
    #     n_random = int(len(input_list)*0.2)
    #     random_numbers = [random.choice(range(0,len(input_list))) for i in range(0,n_random)] # generate x random indices in list
    #     test_list = [input_list[i] for i in random_numbers]
    # else:
    #     test_list = input_list # for short lists we use the whole list
    if override is not None:
        return dicts[override]
    
    test_list = input_list

    # check the responses against the keys
    dict_found = False
    potential_dict_found = False
    potential_dict_list=[]

    for query_dict in dicts:
        bool_list = []
        for item in test_list:
            if item in list(query_dict.keys()):
                bool_list.append(True)
            else:
                bool_list.append(False)
                
        dict_found = all(bool_list)
        potential_dict_found = any(bool_list)
        
        if dict_found:
            return query_dict
        elif potential_dict_found:
            potential_dict_list.append(query_dict)

    
    if len(potential_dict_list) > 1:
        if not user_choice: 
            print("dictionaries.get_dict found multiple possible matches. Choosing the first one.")
            print(f'Potential match: {potential_dict_list[0]}')
            return potential_dict_list[0]
        else: 
            for i in enumerate(potential_dict_list):
                print(i)
            selection = int(input("Use which dictionary?: "))
            return potential_dict_list[selection]
        
    elif len(potential_dict_list) > 0:
        return potential_dict_list[0]

    else:
        # this used to return the input list, but some functions NEED a dict.
        # print("Dictionary not found! Returning empty dict.")
        # print("First 5 items: "+str(input_list[0:5]))
        return {} 




def str_to_int(to_be_converted, ignore_zero=False, passthrough=False, user_choice=True, override=None):
    '''
    Input: a list or dict (containing keys that are) of strings 
    ignore_zero returns a list that omits values of zero.
    passthrough returns a list where items with no key are left in the list. 
    passthrough currently only works with lists.
    
    Output: a list or dict (depending on input) of ints.
    
    
    '''
    
    input_type = type(to_be_converted)
    
    if all(to_be_converted) == int:
        print("dictionaries.str_to_int detected input of ints. No conversion needed.")
        return to_be_converted
    
    if input_type == list:
        if override is not None:
            ref_dict=get_dict(to_be_converted,override=override)
        else:
            ref_dict = get_dict(to_be_converted, user_choice=user_choice)
        out_list = []
        
        for item in to_be_converted:
            
            if item in ref_dict: # First check if the item is in the dictionary.
                new_value = ref_dict[item]
                if ignore_zero:
                    if new_value == 0:
                        continue
                    else:
                        out_list.append(new_value)
                else:
                    out_list.append(new_value)
                
                
            elif passthrough: # if passthrough true and item not in dict, keep it.
                new_value = item
                if ignore_zero:
                    if item == 0 or item in zero_list:
                        continue
                    else:
                        out_list.append(new_value)
                else:
                    out_list.append(new_value)
                
            else: # If the item's not there and passthrough is off, just skip this one.
                continue
            
        return out_list

    elif input_type == dict:
        in_keys = list(to_be_converted.keys())
        if override is not None:
            ref_dict = get_dict(in_keys,override=override)
        else:
            ref_dict = get_dict(in_keys)
        
        out_dict = {}
        for i in range(0, len(in_keys)):
            in_value = to_be_converted[in_keys[i]]
            new_key = ref_dict[in_keys[i]]
            
            # Issue: only latest of duplicated keys is saved. Will therefore combine values for duplicated keys.
            # In this case, only the first instance of the value will be chosem as they
            if new_key in list(out_dict.keys()):
                tmp_value = out_dict[new_key]
                out_dict[new_key] = tmp_value + in_value
                
            else:
                out_dict[new_key] = in_value
        
        return out_dict
    else:
        print("dictionaries.str_to_int only takes lists or dicts, what type is your input? Returning input.")
        return to_be_converted
    

zero_list = ["Not Applicable", 0, "Not sure", "N/A", "Prefer not to say", 'nan', np.nan]


### Testing ###

# import setup_tidy
# import numpy as np
# data_dict = setup_tidy.get_data_dict()
# var_list = setup_tidy.get_var_list()
# variable_number = 73
# data_for_testing = data_dict[var_list[variable_number]]
# results = str_to_int(data_for_testing)
# # print(results[0:10])

# def the_gauntlet():

#     for i in range(0,len(var_list)):
#         try:
#             str_to_int(data_dict[var_list[i]])
#             print(str(i)+" worked")
#         except:
#             print(str(i)+" failed")
#         print(var_list[i])
#         print()
# the_gauntlet()
        
################    
    
    
    
    


# Next steps set up a dictionary (or dictionaries) where the variable_list
# value can be passed to return the question, type etc. 

# variable_dict = {}
# for i in range(1,len(variable_list)+1):
#     variable_dict[variable_list[i]] = [question_list[i], question_type_list[i], data_type_list[i], value_code_list[i]]
# # print(variable_dict["VAR00"])

# data_dict = {}
# for i in range(0, len(variable_list)):
#     data_dict[data_array[i][0]] = data_array[i][1:]
# # print(data_dict["ID"])





# academic_dict = {
#     'A Swedish academic, or' : 1, 
#     'An international academic in Sweden ' : 2
#     }

# numeric_dict = [i for i in range(0,1000)]



# # assigning var dicts
# yes_no_vars = []
# for key in variable_dict:
#     if variable_dict[key][3] == '1 = Yes\n2 = No\n0 = Not sure' or \
#         variable_dict[key][3] == '1 = Yes\n2 = No' or \
#         variable_dict[key][3] == '1 = Yes\n2 = No\n0 = Prefer not to say' or \
#         variable_dict[key][3] == '1 = Yes\n2 = No\n0 = Not Applicable':
#         yes_no_vars.append(key)

# gender_vars = []
# for key in variable_dict:
#     if variable_dict[key][3] == \
#         '1 = Female\n2 = Male\n3 = Non-binary\n4 = Prefer not to say':
#         gender_vars.append(key)
        
# agree_disagree_vars = []
# for key in variable_dict:
#     if variable_dict[key][3] == \
#         '1 = Strongly Disagree (very untrue about me)\n2 = Disagree (somewhat untrue about me)\n3 = Neither agree nor disagree\n4 = Agree (somewhat true about me)\n5 = Strongly Agree (very true about me)\n0 = Not Applicable':
#         agree_disagree_vars.append(key)

# academic_vars = []
# for key in variable_dict:
#     if variable_dict[key][3] == \
#         '1 = A Swedish academic, or\n2 = An international academic in Sweden ':
#         academic_vars.append(key)
            
# numeric_vars = []
# for key in variable_dict:
#     if variable_dict[key][1] == \
#         'Numeric - Field':
#         numeric_vars.append(key)