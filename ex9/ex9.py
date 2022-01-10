"""
Author: Medis Redzic
Matr.Nr.: K11934616
Exercise: Exercise 9
"""
def fun2(flist):
    new_list = []
    for i in range(flist[0]):
        new_list.append(flist[i + 1])

    return new_list

def fun(data):
    new_list = []
    for n in range(len(data)):
        new_list.append(fun2(data[n]))

    return [i for s in new_list for i in s]
