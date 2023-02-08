import numpy as np
from tile_puzzle import TilePuzzle

if __name__ == "__main__":
    print("\n\n>> Enter the initial state of the tile puzzle. It can be 8-puzzle or 15-puzzle or more (if you can wait long for the solution)")
    print(">> If your initial state is:")
    print('-------------')
    print('| 1 | 2 | 3 |')
    print('-------------')
    print('| 4 | 0 | 5 |')
    print('-------------')
    print('| 6 | 7 | 8 |')
    print('-------------')
    print("Then your input should be a row-wise 1-D vector: '1 2 3 4 0 5 6 7 8'.")
    print(">> All the numbers should be white-space separated in one single line.")
    print(">> Numbers should be non-repeating, \n and should be in the range of 0 to (N^2 - 1), where NxN is the dimension of the square matrix puzzle.\n\n")
    input_state_str = input("Initial state: ")
    is_input_valid = True

    try:
        input_numbers = [int(num) for num in input_state_str.split()]
        input_numbers_set = set(input_numbers)

        # Check for duplication
        if (len(input_numbers) != len(input_numbers_set)):
            raise Exception("Invalid Input")

        num_of_numbers = len(input_numbers)
        # Check if the number of numbers in the input is a perfect sqaure
        if (np.sqrt(num_of_numbers) - int(np.sqrt(num_of_numbers)) != 0):
            raise Exception("Invalid Input")

        # Check if the numbers are in range of 0 to (N^2 - 1), where N = sqrt(num_of_numbers)
        if not np.all((np.array(input_numbers) >= 0) & (np.array(input_numbers) < num_of_numbers)):
            raise Exception("Invalid Input")
    
    except:
        is_input_valid = False
        print("Invalid input! Try again")
    

    # We are good to go with the input
    if is_input_valid:
        tile_puzzle = TilePuzzle(tuple(input_numbers))
        tile_puzzle.solve()
