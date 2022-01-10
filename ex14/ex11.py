"""
Author: Medis Redzic
Matr.Nr.: K11934616
Exercise: Exercise 11
"""

def count_bases_and_subsequence(data_as_string: str, subsequence: str):
    data_as_list = data_as_string.split('\n')
    subs = []
    subs2 = ""
    valid_bases = ['a', 'c', 'g', 't']
    count = {'a': 0, 'c': 0, 'g': 0, 't': 0}

    for n in data_as_list:
        if n == '% DATA_END':
            break
        if not n.startswith('%') and len(n) != 0:
            temp = n.split(';')
            if float(temp[2]) > 0.07:
                subs2 += temp[1].lower()
                if temp[1].lower() in valid_bases:
                    subs.append(temp[1].lower())
            else:
                subs2 += '_'
        else:
            subs2 += '_'

    subcount = subs2.count(subsequence.lower())

    for i in subs:
        count[i] += 1

    return subcount, count
