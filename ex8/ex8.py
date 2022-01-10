"""
Author: Medis Redzic
Matr.Nr.: K11934616
Exercise: Exercise 8
"""


def fun(lines):
    new_list = []
    snd_list = []
    
    if not lines:
        return 0, 0

    lines = [i for i in lines if not i.startswith('#')]

    for k in range(len(lines)):
        tmp = lines[k].split(' ')
        for n in range(len(tmp)):
            if tmp[n] not in new_list and tmp[n]:
                new_list.append(tmp[n])
            if tmp[n].lower() not in snd_list and tmp[n]:
                snd_list.append(tmp[n].lower())
    return (len(new_list), len(snd_list))