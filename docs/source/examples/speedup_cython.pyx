"""

The Cython code for `find_four`.
Here is the procedure to integrate this into the IPython Notebook
in a first iPython cell you type
    
    %load_ext cythonmagic

Then in another cell you write on the first line

    %%cython
    
then the actual code

"""


import numpy as np
cimport numpy as np

"""
The next array represents starting tiles and directions in which to
search for four connected pieces. It has been obtained with

>>> print np.array(
    [[[i,0],[0,1]] for i in range(6)]+
    [ [[0,i],[1,0]] for i in range(7)]+
    [ [[i,0],[1,1]] for i in range(1,3)]+
    [ [[0,i],[1,1]] for i in range(4)]+
    [ [[i,6],[1,-1]] for i in range(1,3)]+
    [ [[0,i],[1,-1]] for i in range(3,7)]).flatten()
"""

cdef int *POS_DIR = [ 0,  0,  0,  1,  1,  0,  0,  1,  2,  0,
        0,  1,  3,  0,  0,  1,  4, 0,  0,  1,  5,  0,  0,  1,
        0,  0,  1,  0,  0,  1,  1,  0,  0,  2, 1,  0,  0,  3, 
        1,  0,  0,  4,  1,  0,  0,  5,  1,  0,  0,  6,  1, 0,
        1,  0,  1,  1,  2,  0,  1,  1,  0,  0,  1,  1,  0,  1,
        1,  1,  0,  2,  1,  1,  0,  3,  1,  1,  1,  6,  1, -1,
        2,  6,  1, -1,  0,  3,  1, -1,  0,  4,  1, -1,  0,  5,
        1, -1,  0,  6,  1, -1]

cpdef int find_four(np.ndarray[int, ndim=2] board, int current_player):
    
    cdef int i, streak, pos_i, pos_j , dir_i, dir_j
    
    for i in range(25):
        
        pos_i = POS_DIR[4*i+0]
        pos_j = POS_DIR[4*i+1]
        dir_i = POS_DIR[4*i+2]
        dir_j = POS_DIR[4*i+3]
        
        streak = 0
        
        while (0 <= pos_i <= 5) and (0 <= pos_j <= 6):
            if board[pos_i][pos_j] == current_player:
                streak += 1
                if streak == 4:
                    return 1
            else:
                streak = 0
            pos_i = pos_i + dir_i
            pos_j = pos_j + dir_j
        
    return 0


