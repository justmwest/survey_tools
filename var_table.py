#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 13 21:09:34 2021

@author: Justin

This script is for printing out a variable 'cheat sheet' in a legible format.
not finished.
"""

import setup
from tabulate import tabulate

table = []
for key in setup.variable_dict:
    table.append(key)
print(tabulate(table))