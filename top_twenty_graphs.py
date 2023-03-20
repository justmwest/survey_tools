#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 13 13:39:32 2021

@author: justin

This script runs rsquared_of_all.py and pulls out the best twenty correlations,
then graphs them. The output files can be saved from spyder. 
"""

import setup
import rsquared_of_all
top_twenty_pairs = [i[0] for i in rsquared_of_all.annotated_list[73:113:2]]

for i in range(len(top_twenty_pairs)):
    setup.plot_data(top_twenty_pairs[i][0], top_twenty_pairs[i][1], bar=True, frequency_mode=False)