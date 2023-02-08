# N-Puzzle Problem
#### This is the N-Puzzle problem where N = (MxM - 1) and M > 2
- The numbers from 1 to N and an empty tile(or zero) are placed randomly in a 2-D MxM matrix (tiles) and the goal is to move the empty tile to attain a target position (here, numbers arranged row-wise in increasing order with the last cell empty)

#### This solution uses simple breadth first search(BFS) algorithm to find the path to the target state

##### Following are the instructions to run the code:
- Make sure you have the following files in the same directory location:
   1) solve_tile_puzzle.py
   2) tile_puzzle.py
   3) msgs.txt
- In the terminal where you can run python scripts go to the directory where the above files are located
- Make sure you have numpy installed. *[help](https://docs.scipy.org/doc/numpy/user/install.html)*
- Type: **$ python solve_tile_puzzle.py**
- Input should be a row-wise 1-D vector.
- All the numbers should be white-space separated in one single line.
- Numbers should be non-repeating and should be in the range of 0 to N.

   For example, if the initial state for a 8-puzzle problem is:
   
   1 2 3
   
   4 0 5 
   
   6 7 8
   
   then input = '1 2 3 4 0 5 6 7 8'.
   

