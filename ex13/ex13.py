"""
Author: Medis Redzic
Matr.Nr.: K11934616
Exercise: Exercise 13
"""


def get_file_metadata(data_as_string: str):

    id = ''
    date = 0
    columns = []
    start_index = -1
    end_index = -1

    exists = [0, 0, 0]

    data_as_list = data_as_string.split('\n')

    # Get header start and exit indices
    for n in range(len(data_as_list)):
        if data_as_list[n].startswith('% HEADER_START'):
            start_index = n
        if data_as_list[n].startswith('% HEADER_END'):
            end_index = n

    # Check if data_end exists in file
    for n in range(end_index, len(data_as_list)):
        if data_as_list[n].startswith('% DATA_END'):
            break
    else:
        raise AttributeError('Could not find "% DATA_END" ')

    # Check if header_start and header_end exist in file
    if start_index == -1 or end_index == -1:
        raise AttributeError('Header_start of header_end do not exist in the file')

    # Check if id, date and columns exist
    for n in range(start_index, end_index):
        if data_as_list[n].startswith('% ID: '):
            exists[0] = 1
        if data_as_list[n].startswith('% Date: '):
            exists[1] = 1
        if data_as_list[n].startswith('% Columns: '):
            exists[2] = 1

    if exists[0] != 1 or exists[1] != 1 or exists[2] != 1:
        raise AttributeError('Id, date or columns do not exist in the file')

    # Check if header has anything else except % and new line
    for i in range(end_index, 0, -1):
        if not data_as_list[i].startswith(('\n', '%')):
            raise AttributeError('Lines before HEADER_START are not empty or do not start with "%"')

    # Seperate information we need
    for n in range(start_index, end_index):
        if data_as_list[n].startswith('% ID: '):
            temp = data_as_list[n].split(' ')
            id += temp[-1]

        if data_as_list[n].startswith('% Date: '):
            temp = data_as_list[n].split(' ')
            if temp[-1].isdigit():
                date = int(temp[-1])
            else:
                raise TypeError('Date is not integer')

        if data_as_list[n].startswith('% Columns: '):
            temp = data_as_list[n].strip().replace(' ', ';')
            temp = temp.split(';')
            columns.extend(temp[-3:])

    return id, date, columns
