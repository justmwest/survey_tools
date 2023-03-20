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

# First I need to pull in the columns
gen_col = 4
kids_col = 8
prt_col = 19


# Now get the values
def pull_vals(col):
    temp=var_list[col]
    return data_dict[temp]
gen, age, pos = [pull_vals(i) for i in [gen_col, age_col, pos_col]]

# now return values of AGE for each position and gender.
gen_unis, pos_unis = [unique_responses(i) for i in [gen,pos]]

def count_em_up():
    out_dict={}
    for g,a,p in zip(gen,age,pos):
        pass
    
    for uni_p in pos_unis:
        for uni_g in gen_unis: # for each position cycle through the genders.
            
            
            for a, g, p in zip(age,gen,pos): # Then run through all values looking for double matches.
                if p == uni_p and g == uni_g:
                    if (p,g) in out_dict.keys():
                        out_dict[p,g].append(a)
                    else:
                        out_dict[p,g] = [a] # for the first one create a list. For all the rest, add an item.
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
    
    if len(data)>9:
        print(label)
    # print(data)

        average = sum(data)/len(data)
        print(f'average = {average}. min = {min(data)}. max = {max(data)}. range = {max(data) - min(data)}')
        print(f'n = {len(data)}')

    
    
def main():
    # print(count_em_up()) # This seems to work.
     
    
    
    master_dict = count_em_up()
    clean_dict = clean_em_up(master_dict)
    # print(clean_dict)
    for key,value in clean_dict.items():
        stats(value,key)
        
    
    pass








if __name__ == '__main__':
    main()