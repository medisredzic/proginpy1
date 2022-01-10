"""
Author: Medis Redzic
Matr.Nr.: K11934616
Exercise: Exercise 7
"""


def fun(long_string):
    long_string = long_string.replace(' ', '')
    dict_new = {}
    for n in long_string:
        if n.isalpha():
            if n in dict_new:
                dict_new[n] += 1;
            else:
                dict_new[n] = 1;

    return dict_new
