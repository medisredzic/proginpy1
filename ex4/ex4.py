"""
Author: Medis Redzic
Matr.Nr.: K11934616
Exercise: Exercise 4
"""

#
# Start of code block that should not be modified.
#

# The next lines will ask the user for input through the console and set the variables var1 and var2
# to the input the user typed in the console. Per default, these values will be of datatype string.
# See the assignment sheet for more details.
datatype1 = input('Select a datatype (type "int", "float" or "string" and hit enter) for var1: ')
var1 = input("Enter var1: ")
datatype2 = input('Select a datatype (type "int", "float" or "string" and hit enter) for var2: ')
var2 = input("Enter var2: ")

#
# End of code block that should not be modified.
#

# Place your code here.

if datatype1 == 'int':
    var1 = int(var1)
elif datatype1 == 'float':
    var1 = float(var1)
elif datatype1 == 'string':
    var1 = str(var1)

if datatype2 == 'int':
    var2 = int(var2)
elif datatype2 == 'float':
    var2 = float(var2)
elif datatype2 == 'string':
    var2 = str(var2)

#
# Start of code block that should not be modified.
#

operation = input('Choose an operation (type "add" or "multiply"): ')

#
# End of code block that should not be modified.
#

# Place your code here.

if operation == 'add':
    result = var1 + var2
elif operation == 'multiply':
    result = var1 * var2
else:
    result = 'unknown operation'
#
# Do not modify the code below this line.
#

# This will print the result to the console.
print(f"Result: {result}")