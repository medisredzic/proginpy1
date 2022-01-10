"""
Author: Medis Redzic
Matr.Nr.: K11934616
Exercise: Exercise 5
"""

my_variable = input("Enter int >= 0 or 'x' to exit: ")
sumAll = 0

while my_variable != 'x':
    if my_variable.isdecimal():
        sumAll = sumAll + int(my_variable)
    else:
        print("You must enter an int >= 0 or 'x'")

    my_variable = input("Enter int >= 0 or 'x' to exit: ")

print(sumAll)

