"""
Author: Medis Redzic
Matr.Nr.: K11934616
Exercise: Exercise 10
"""

def fun(a, b):
    try:
        if a == 0 or b == 0:
            raise ZeroDivisionError()
        if type(a) != int or type(b) != int:
            raise ValueError
        else:
            return a / b
    except ZeroDivisionError:
        return None
    except ValueError as err:
        return type(err), f"ValueError: a ({type(a)}) or b ({type(b)}) was incompatible with division"
