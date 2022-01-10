"""
Author: Medis Redzic
Matr.Nr.: K11934616
Exercise: Exercise 6
"""


"""def fun(long_string):
    new_string = long_string.split()

    new_string = [i for i in new_string if i != 'end']
    new_string = [i for i in new_string if i != 'exit']
    new_string = ';'.join(new_string)

    return new_string.upper()"""

    
"""def fun(long_string):
    my_string = long_string
    remove_end = [' end ', ' end', 'end ']
    remove_exit = [' exit ', ' exit', 'exit ']
    for end in remove_end:
        my_string = my_string.replace(end, ' ')
    for exit in remove_exit:
        my_string = my_string.replace(exit, ' ')
    my_string = ' '.join(my_string.split())
    my_string = my_string.replace(" ", ";")
    return my_string.upper()"""
    
def fun(my_string):
    word_list = my_string.split(' ')
    print(word_list)
    for word in word_list:
        #print(word)
        if word == 'end' or word == "exit" or word == ' ':
            print(word)
            word_list.remove(word)
        else:
            word_list[word_list.index(word)] = word.upper()
    return ';'.join(word_list).upper()


#print(fun('this is a long test exit string'))

