"""
Author: Medis Redzic
Matr.Nr.: K11934616
Exercise: Exercise 16
"""

import re
import numpy as np


def read_config_file(config_file: str):

    f = open(config_file, 'r')
    filestr = f.read() # Save entire file to string so we can use regex on it.

    # Simple usage of regex to get required information
    iter_count = re.search(r'iteration_count:\s*(.*)\s*', filestr)
    dead_symb = re.search(r'dead_symbol:\s*["](.*)["]', filestr)
    live_symb = re.search(r'live_symbol:\s*["](.*)["]', filestr)
    init_state = re.search(r'init_state:\n*"([\s\S]*?)\"', filestr)
    scope = re.search(r'scope:\s*\((.*?)\)\s*\((.*?)\)', filestr)

    # Check if iter_count exists(its not None) and try to convert it to integer
    if iter_count:
        iter_count = iter_count.group(1)
        if iter_count.isnumeric():
            iter_count = int(iter_count)
        else:
            raise AttributeError('iteration_count is not an integer')
    else:
        raise AttributeError('iteration_count is missing')

    """
        Check if dead_symbol and live_symbol exist.
        If they do not exist raise AttributeError
        If they exist check whether it has more than 1 character, if it doesn't save it to variable.
    """
    if dead_symb:
        if len(dead_symb.group(1)) > 1:
            raise AttributeError('dead_symbol has more than 1 character')
        else:
            dead_symb = dead_symb.group(1)
    else:
        raise AttributeError('dead_symbol is missing')

    if live_symb:
        if len(live_symb.group(1)) > 1:
            raise AttributeError('live_symbol has more than 1 character')
        else:
            live_symb = live_symb.group(1)
    else:
        raise AttributeError

    """
        Firstly I used regex to check if only dead_symbol and live_symbol exist in init_state
        After that I looped through previously created list of init_state to check if lines are the same in length
        Then I looped through same list to check if there are any lines that are filled or not
        Afterwards I looped through init_state(which I split into list) and appened any line that is greater than 0 to new list
        Then I used a list comprehension to create list of lists where each state is one element, then I converted it to numpy
        Afterwards I created a new numpy array and replaced existing elements with 0s and 1s
    """
    if init_state:
        init_list = init_state.group(1).split('\n')

        if re.search(fr'[^{dead_symb}{live_symb}\n]'.replace('-', '\-'), init_state.group(1)):
            raise ValueError('Only dead_symbol and live_symbol are allowed')

        empty_line = 0

        for n in init_list:
            if empty_line == 0:
                empty_line = len(n)
            if empty_line > 0:
                if empty_line != len(n) and len(n) != 0:
                    raise ValueError('Non empty lines do not have same length')

        for n in init_list:
            if len(n) > 0:
                break
        else:
            raise ValueError('The number of non-empty lines is 0')

        init_state = init_state.group(1)
        init_state = init_state.split('\n')

        new_state = []
        for n in init_state:
            if len(n) > 0:
                new_state.append(n)

        new_state = [list(char) for char in new_state]
        np_init_state = np.array(new_state)
        np_int = np.array(np_init_state == live_symb, dtype=np.int_)

    else:
        raise AttributeError('init_state is missing or couldn\'t be read')

    """
        First I split results into groups using rexeg, after that I split them into 2 lists containg rows an columns
        Then I checked whether row or column contains more or less than 2 integers(elements)
        
        I had issues solving the next part for some reason, every single solution I tried would throw me some wierd errors
            so I managed to do it in a way below. I just looped over previously made lists and checked if they are integers
            and appened them to a new list.
    """
    scope_row = scope.group(1).replace(' ', '').split(',')
    scope_col = scope.group(2).replace(' ', '').split(',')

    if scope:
        if len(scope_row) != 2 or len(scope_col) != 2:
            raise AttributeError('scope_row or scope_col does not contain 2 integers')

        scopes = []

        for n in scope_row:
            if n.isnumeric():
                scopes.append(int(n))
            else:
                raise AttributeError('scope is not an integer')

        for j in scope_col:
            if j.isnumeric():
                scopes.append(int(j))
            else:
                raise AttributeError('scope is not an integer')
    else:
        raise AttributeError('scope cannot be extracted')

    return iter_count, dead_symb, live_symb, np_int, scopes

#print(read_config_file("C:\\Users\\MEDIS\\PycharmProjects\\ex16\\ex16_testfiles\\valid_05.config"))