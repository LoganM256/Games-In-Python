def find_next_empty(puzzle):
    # finds the next row, col on the puzzle that's not filled yet --> rep with -1
    # return row,col tuple (or (None,None) if there is none)
    
    # keep in mind that we are using 0-8 for our indices 
    for r in range(9):
        for c in range(9):    #range(9) is 0, 1, 2, .... 8
            if puzzle[r][c] == -1:
                return r,c
    
    return None, None    # if no spaces in the puzzle are empty (-1)

def is_valid(puzzle, guess, row, col):
    # figures out whether the guess at that row/col of the puzzle is a valid guess
    # returns true is is valid, False otherwise
    
    # let's start with the row check:
    row_vals = puzzle[row]
    if guess in row_vals:
        return False
    
    # Now the columns
    #col_vals = []
    #for i in range(9):
    #    col_vals.append(puzzle[i][col])
    col_vals = [puzzle[i][col] for i in range(9)] #list comprehension
    if guess in col_vals:
        return False
    
    # Let's check the little 3 by 3 matrix
    # This is a bit tricky, but we want to get where the 3x3 starts 
    # and iterate over the 3 values in the row/column

    row_start = (row // 3) * 3 # divides by 3 but throws away the remainder. 1 // 3 = 0, 5 // 3 = 1, ...
    col_start = (col // 3) * 3

    for r in range(row_start, row_start + 3):
        for c in range(col_start, col_start + 3):
            if puzzle[r][c] == guess:
                return False
    return True

def solve_sudoku(puzzle):
    # solve sudoku using a backtrack technique
    # our puzzle is a list of lists, where each inner list is a row in our sudoku puzzle
    # return whether a solution exists
    # mutates puzzle to be the solution (if the solution exists)

    # Step 1: choose somewhere on the puzzle to make a guess

    row, col = find_next_empty(puzzle)

    # Step 1.1: if there is nowhere left, then we're done because we only allowed valid inputs
    if row is None:
        return True
    
    # Step 2: if there is a place to put a number, then make a guess between 1 and 9
    for guess in range(1,10): #(1,10) is 1, 2, 3, 4, ... 9
        #step 3: checking if this is a valid guess
        if is_valid(puzzle, guess, row, col):
            #step 3.1: if this is valid, then place that guess on the puzzle!
            puzzle[row][col] = guess
            # now we recursively call this puzzle!
            # step 4: recursively call our function
            if solve_sudoku(puzzle):
                True
        
        #Step 5: if not valid OR if our guess does not solve the puzzle, then we need to backtrack and try a new number
        puzzle[row][col] = -1 # reset the guess

    
    #step 6: if none of the numbers that we try work, then this puzzle is unsolvable!
    return False