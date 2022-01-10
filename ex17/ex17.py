"""
Author: Medis Redzic
Matr.Nr.: K11934616
Exercise: Exercise 17
"""

import numpy as np
import pickle

""" 
    Simple functions that extract neighbours at certain locations inside array
"""

# Diagonal neighbour


def cn_diag_d_right(x, p: tuple): return x[p[0] + 1, p[1] + 1]  # diagonal neighbour - down right
def cn_diag_d_left(x, p: tuple): return x[p[0] + 1, p[1] - 1]  # diagonal neighbour - down left
def cn_diag_u_right(x: np.ndarray, p: tuple): return x[p[0] - 1, p[1] + 1]  # diagonal neighbour - upper right
def cn_diag_u_left(x: np.ndarray, p: tuple): return x[p[0] - 1, p[1] - 1]  # diagonal neighbour - upper left

# surrounding neighbours


def cn_upper(x: np.ndarray, p: tuple): return x[p[0] - 1, p[1]]  # upper
def cn_down(x: np.ndarray, p: tuple): return x[p[0] + 1, p[1]]  # down
def cn_right(x: np.ndarray, p: tuple): return x[p[0], p[1] + 1]  # right
def cn_left(x: np.ndarray, p: tuple): return x[p[0], p[1] - 1]  # left


"""
    Function to check value and compute whether cell should be alive or dead
    
    * Return: State of the cell
"""

def check_value(value, neighbours):
    if value == 1:
        if neighbours < 2:
            return 0
        elif 1 < neighbours <= 3:
            return 1
        elif neighbours > 3:
            return 0

    if value == 0:
        if neighbours == 3:
            return 1
        else:
            return 0


"""
    Function to check cell and compute its live/dead neighbours.
    
    *Return: State of the cell
"""

def check_neighbour(state_, position: tuple):
    value = state_[position]
    neighbours = 0

    if position == (0, 0):
        neighbours += cn_right(state_, position)
        neighbours += cn_down(state_, position)
        neighbours += cn_diag_d_right(state_, position)
        return check_value(value, neighbours)

    if position == (0, position[1]) or position == (position[0], 0):
        if position == (0, len(state_[0]) - 1):
            neighbours += cn_left(state_, position)
            neighbours += cn_down(state_, position)
            neighbours += cn_diag_d_left(state_, position)
        elif position == (len(state_) - 1, 0):
            neighbours += cn_right(state_, position)
            neighbours += cn_upper(state_, position)
            neighbours += cn_diag_u_right(state_, position)
        elif position == (0, position[1]):
            neighbours += cn_right(state_, position)
            neighbours += cn_left(state_, position)
            neighbours += cn_down(state_, position)
            neighbours += cn_diag_d_right(state_, position)
            neighbours += cn_diag_d_left(state_, position)
        elif position == (position[0], 0):
            neighbours += cn_right(state_, position)
            neighbours += cn_upper(state_, position)
            neighbours += cn_down(state_, position)
            neighbours += cn_diag_u_right(state_, position)
            neighbours += cn_diag_d_right(state_, position)

        return check_value(value, neighbours)

    if position == (position[0], len(state_[0]) - 1) or position == (len(state_)-1, position[1]):
        if position == (len(state_) - 1, len(state_[0]) - 1):
            neighbours += cn_left(state_, position)
            neighbours += cn_upper(state_, position)
            neighbours += cn_diag_u_left(state_, position)
        elif position == (position[0], len(state_[0]) - 1):
            neighbours += cn_upper(state_, position)
            neighbours += cn_down(state_, position)
            neighbours += cn_left(state_, position)
            neighbours += cn_diag_u_left(state_, position)
            neighbours += cn_diag_d_left(state_, position)
        elif position == (len(state_) - 1, position[1]):
            neighbours += cn_upper(state_, position)
            neighbours += cn_left(state_, position)
            neighbours += cn_right(state_, position)
            neighbours += cn_diag_u_left(state_, position)
            neighbours += cn_diag_u_right(state_, position)

        return check_value(value, neighbours)

    neighbours += cn_left(state_, position)
    neighbours += cn_right(state_, position)
    neighbours += cn_down(state_, position)
    neighbours += cn_upper(state_, position)
    neighbours += cn_diag_u_left(state_, position)
    neighbours += cn_diag_u_right(state_, position)
    neighbours += cn_diag_d_left(state_, position)
    neighbours += cn_diag_d_right(state_, position)

    return check_value(value, neighbours)


def gen_next_state(state, scope):

    st = 0
    if scope is None:
        cropped_state = state
    else:
        for n in scope:
            if n < 0:
                st += 1
        if st == 0:
            if scope[0] == scope[2] or scope[1] == scope[3]:
                cropped_state = state
            elif scope[0] > scope[2] or scope[1] > scope[3]:
                cropped_state = state
            elif scope[0] > len(state) or scope[2] > len(state):
                cropped_state = state
            elif scope[1] > len(state[0]) or scope[3] > len(state[0]):
                cropped_state = state
            else:
                cropped_state = state[scope[0]:scope[2], scope[1]:scope[3]]
        else:
            cropped_state = state

    new_state = np.empty_like(cropped_state, dtype=np.int_)

    for i_arr, n in enumerate(cropped_state):
        for i, j in enumerate(n):
            cn = check_neighbour(cropped_state, (i_arr, i))
            new_state[i_arr, i] = cn

    return new_state