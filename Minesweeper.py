import random
import re
#Let's create a board object to represent the minesweeper game 
#This is so that we can just say "create a new board object", or
#"dig here", or "render this game for this object"
class Board:
    def __init__(self, dim_size, num_bombs):
        self.dim_size = dim_size
        self.num_bombs = num_bombs
        #Let's create the board
        #Helper Function!
        self.board = self.make_new_board() #We will plant the bombs here too
        self.assign_values_to_board()
        #Initialize a set to keep track of which locations we've uncovered
        #we'll save (row,column) tuples into this set
        self.dug = set()

    def assign_values_to_board(self):
        #Lets assign spaces a value of 0-8 representing how many bombs are next to it. 
        for r in range(self.dim_size):
            for c in range(self.dim_size):
                if self.board[r][c] == '*':
                    continue
                self.board[r][c] = self.get_num_neighboring_bombs(r, c)

    def get_num_neighboring_bombs(self, row, col):
        #We need to iterate through each neighboring position and check for bombs by suming them.
        #top lef: (row-1,col-1)
        #top middle (row-1,col)
        #top right (row-1,col+1)
        #left (row,col-1)
        #right (row,col+1)
        #bottom left (row+1,col-1)
        #bottom middle (row+1,col)
        #bottom right (row+1,col+1)

        #make sure that we dont go out of bounds

        num_neighboring_bombs = 0
        for r in range(max(0, row-1),min(self.dim_size - 1, row+1) + 1):
            for c in range(max(0, col-1), min(self.dim_size - 1, col+1) + 1):
                if r == row and c == col:
                    #this is our original location so we don't check this, just continue
                    continue
                if self.board[r][c] == '*':
                    num_neighboring_bombs += 1
        return num_neighboring_bombs

    def dig(self, row, col):
        #return True if it's a successful dig and false if bomb is dug

        #A few scenarios here: 
        #hit a bomb and we lose 
        #Don't hit a bomb and we dig recursively until we get to a bomb
        #They dig and immediately a next to a bomb so we stop

        self.dug.add((row,col)) #Keeping track of where we dug
        
        if self.board[row][col] == '*':
            return False
        elif self.board[row][col] > 0:
            return True
        
        
        #If we get here, it means this number is 0 or self.board[row][col] == 0
        for r in range(max(0, row-1),min(self.dim_size - 1, row+1) + 1):
            for c in range(max(0, col-1), min(self.dim_size - 1, col+1) + 1):
                if (r,c) in self.dug:
                    continue #Don't dig where you already dug
                self.dig(r,c)

        #if our initial dig didn't hit a bomb, we shouldn't hit a bomb here
        return True
    
    def __str__(self):
        #this is a magic function where if you call print on this object,
        #it'll print out what this function returns!
        #Let's return a string that shows the player the board

        #first we create an array that represents what the user would see behind the scenes
        visible_board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]
        for row in range(self.dim_size):
            for col in range(self.dim_size):
                if (row,col) in self.dug:
                    visible_board[row][col] = str(self.board[row][col])
                else:
                    visible_board[row][col] = ' '
        
        #put this together in a string
                string_rep = ''
        #get max column widths for printing
        widths = []
        for idx in range(self.dim_size):
            columns = map(lambda x: x[idx], visible_board)
            widths.append(
                len(
                    max(columns, key = len)
                )
            )
        
        #print the csv strings
        indices = [i for i in range(self.dim_size)]
        indices_row = '   '
        cells= []
        for idx, col in enumerate(indices):
            format = '%-' + str(widths[idx]) + "s"
            cells.append(format % (col))
        indices_row += '  '.join(cells)
        indices_row += '  \n'

        for i in range(len(visible_board)):
            row = visible_board[i]
            string_rep += f'{i} |'
            cells = []
            for idx, col in enumerate(row):
                format = '%-' + str(widths[idx]) + "s"
                cells.append(format % (col))
            string_rep += ' |'.join(cells)
            string_rep += ' |\n'

        str_len = int(len(string_rep) / self.dim_size)
        string_rep = indices_row + '-'*str_len + '\n' + string_rep + '-'*str_len 

        return string_rep

    def make_new_board(self):
        #Construct a new board based on the dim size and number of bombs
        #We should construct the list of lists here (or whatever representation you prefer,
        # but since we have a 2-D board, list of lists is most natural.)


        #Generate a new board
        board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]
        # This creates and array like this:
        #[[None, None, ..., None],
        # None, None, ..., None,
        # None, None, ..., None]]
        # We can see how this represents a board!

        #Plant the bombs
        bombs_planted = 0
        while bombs_planted < self.num_bombs:
            loc = random.randint(0, self.dim_size**2 - 1)
            row = loc // self.dim_size
            col = loc % self.dim_size

            if board[row][col] == '*':
                #This means we planted a bomb here already
                continue
            board[row][col] = '*'
            bombs_planted += 1

        return board


#Make a function to actually play the game
def play(dim_size = 10, num_bombs = 10):
    # Step 1: Create the board and plant the bombs
    board = Board(dim_size, num_bombs)
    # Step 2: Show the user the board visually and ask them where they want to dig. Let's use a (0,9) style coordinate system. A Grid.
    # Step 3a: If the location is a bomb, show the game over indication and quit.
    # Step 3b: If not a space is not a bomb, dig recursively until each square is at least next to a bomb.
    # Step 4: repeat steps 2 and 3a, 3b until there are no more squares to dig --> Win!
    
    safe = True 

    while len(board.dug) < board.dim_size ** 2 - num_bombs:
        print(board)
        user_input = re.split(',(\\s)*', input("Where would you like to dig? Input as row,col: ")) # '0,3'
        row, col = int(user_input[0]), int(user_input[-1])
        if row < 0 or row >= board.dim_size or col < 0 or col >= board.dim_size:
            print("Invalid location. Try Again.")
            continue

        #if it is valid, we need to dig at that location
        safe = board.dig(row,col)
        if not safe:
            #We dug a bomb, game over
            break #game over, rip
    
    #Two ways to end the loop, let's check them
    if safe:
        print("Congratulations! You won!")
    else:
        print("Sorry, game over!")
        #Let's reveal the whole board
        board.dug = [(r,c) for r in range(board.dim_size) for c in range(board.dim_size)]
        print(board)
if __name__ == '__main__': #Good practice to follow
    play()
