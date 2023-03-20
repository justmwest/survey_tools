#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 16 13:54:47 2022

@author: justin

This is a script to look at the average age of people with a given position, 
broken down by gender.


"""

# from var_class import var
from setup_tidy import var_list, data_dict
from retrieval_functions import unique_responses
from dictionaries import str_to_int
from retrieval_functions import count_responses

# counts of C will be the output. i.e.: (a1, b1): c
a_col = 4
b_col = 8
c_col = 7


# Now get the values
def pull_vals(col):
    temp=var_list[col]
    return data_dict[temp]

# assigned globally because I'm not sure what else to do in this situation.
a_ls, b_ls, c_ls = [pull_vals(i) for i in [a_col, b_col, c_col]]

# now return values of AGE for each position and gender.
a_unis, b_unis = [unique_responses(i) for i in [a_ls,b_ls]]

def count_em_up(a_col, b_col, c_col):
    a_ls, b_ls, c_ls = [pull_vals(i) for i in [a_col, b_col, c_col]]
    a_unis, b_unis = [unique_responses(i) for i in [a_ls,b_ls]]
    out_dict={}
    for uni_a in a_unis:
        for uni_b in b_unis: # for each position cycle through the genders.
            
            
            for a, b, c in zip(a_ls, b_ls, c_ls): # Then run through all values looking for double matches.
                if a == uni_a and b == uni_b:
                    new_key = (a,b)
                    new_val = c
                    
                    if new_key in out_dict.keys():
                        out_dict[new_key].append(new_val)
                    else:
                        out_dict[new_key] = [new_val] # for the first one create a list. For all the rest, add an item.
    return out_dict
                
# Now clean the groups up
def clean_em_up(master_dict):
    clean_dict = {}
    for key,value in master_dict.items():
        new_val = str_to_int(value, passthrough=True, ignore_zero=True, override=4)
        if type(new_val) == '30+':
            continue
        else:
            clean_dict[key] = new_val
    return clean_dict
    

# Now calculate the stats in each group.
def stats(data, label):
    print(label)
    print(count_responses(data))


        
    # print(data)
    # if all(isinstance(item, int) for item in data) and len(data)>9:
    #     average = sum(data)/len(data)
    #     print(f'average = {average}. min = {min(data)}. max = {max(data)}. range = {max(data) - min(data)}')
    #     print(f'n = {len(data)}')

    
    
def main():
    # print(count_em_up()) # This seems to work.
     
    
    
    master_dict = count_em_up(a_col, b_col, c_col)
    clean_dict = clean_em_up(master_dict)
    # print(clean_dict)
    for key,value in clean_dict.items():
        stats(value,key)
        #print(value)
        
    
    pass








if __name__ == '__main__':
    main()