import copy
import os
from queue import PriorityQueue
import random
import time

def clearConsole():
    """Clears the terminal."""
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    else:
        command = 'clear' # Users on MacOS
    os.system(command)

class State:
    def __init__(self, grid, g, laststate):
        """Class Initialiser.
        
        Keyword arguments:
        grid -- the (typically 3x3) grid that is found at the current state.
        g -- the g value for the state.
        laststate -- the parent state of the current state.
        """
        self.grid = grid # Grid (Typically 3 x 3)
        self.f = g + heuristic(grid) # f = g + h
        self.g = g # Number of nodes traversed to get to node
        self.h = heuristic(grid) # Heuristic calculated by chosen method
        self.ls = laststate # Last State visited
    
    def __lt__(self, other):
        """Used for comparisons."""
        return False # Causes errors otherwise


def setupgrid(input):
    """Sets up the grids for the start and target states.
        
    Keyword arguments:
    input - a list of values to be placed into the grid.
    """
    grid = [[0 for i in range(cols)] for j in range(rows)]
    for a in range(cols):
        for b in range(rows):
            grid[a][b] = input[(a*cols+b)] # makes grid of size cols x rows with input from a list.

    return grid

def printgrid(grid):
    """Prints the grid.
        
    Keyword arguments:
    grid -- the grid to be printed.
    """
    for row in grid:
        print(row) # Prints the grid in a nicer format
    print()

def printfgh(state):
    """Prints the info about the given state.
        
    Keyword arguments:
    state -- the state.
    """
    printgrid(state.grid) # print grid
    print("f(n): " + str(state.f)) # print f value
    print("g(n): " + str(state.g)) # print g value
    print("h(n): " + str(state.h)) # print h value

def inputh():
    correcth = False
    while correcth == False:
        # Let user choose heuristic
        print("Please choose a heuristic method: ")
        print("0. Misplaced Squares")
        print("1. Manhattan Distance")
        print("2. Double Misplaced Squares (Not Admissable)")
        h = int(input())
        if h in range (0,3):
            correcth = True
    return h

def heuristic(grid):
    """Finds the h value for a given grid.
        
    Keyword arguments:
    grid -- the grid to find the h value for.
    """
    if h == 0:
        return hms(grid) # Misplaced Squares
    elif h == 1:
        return hmd(grid) # Manhattan Distance
    elif h == 2:
        return hms(grid)*2 # Double Misplaced Squares
    else:
        return 0  # Otherwise No Heuristic

def hms(grid):
    """Finds the Misplaced Squares heuristic value for a given grid.
        
    Keyword arguments:
    grid -- the grid to find the Misplaced Squares heuristic value for.
    """
    counter = cols * rows # Maximum number of tiles in the correct place
    for i in range(cols):
        for j in range(rows):
            if grid[i][j] == targetgrid[i][j]: # If tile in correct place
                if grid[i][j] == 0 or targetgrid[i][j] == 0: # Makes sure it's a tile and not the gap.
                    continue
                else:
                    counter -= 1 # Remove 1 from counter of tiles out of place
    return counter

def hmd(grid):
    """Finds the Manhattan Distance heuristic value for a given grid.
        
    Keyword arguments:
    grid -- the grid to find the Manhattan Distance heuristic value for.
    """
    counter = 0
    for i in range ((cols*rows)):
        for j in range(cols):
            for k in range(rows):
                if grid[j][k] == i:
                    a, b = j,k # position of values in grid
                if targetgrid[j][k] == i:
                    c,d = j,k # position of values are supposed to be

        offby = (abs(c-a) + abs(d-b)) # calculate the Manhattan distance of the value 
        counter += offby # increase the counter by value's Manhattan distance

    return counter

def usersetgrid(cols, rows):
    """Lets the user create a grid.
        
    Keyword arguments:
    cols -- the number of columns.
    rows -- the number of rows.
    """
    usergrid = [] # List to be put into grid
    for i in range(cols*rows):
        correctdigit = False # False until a valid digit is entered
        while correctdigit == False:
            ui = int(input("Please enter number for position " + str(i+1) + ": ")) # Asks for user input
            possiblev = range((cols*rows)) # Calculates valid values
            if ui in possiblev: # If user input is possible
                if ui not in usergrid: # If not already in grid
                    usergrid.append(ui) # Added to grid
                    correctdigit = True # Valid input set to true
                else:
                    print(str(ui) + " is not a valid input. Already in grid.") # Tells user input is invalid
            else:
                print(str(ui) + " is not a valid input. Out of range.") # Tells user input is invalid

    input("To continue, please press enter...")

    return usergrid # Returns list to be put into grid


def getgriddiction(grid, rows, cols):
    """Creates a dictionary showing the position of each key value in a grid.
        
    Keyword arguments:
    grid -- the grid.
    rows -- the number of rows.
    cols -- the number of columns.
    """

    tilepositions = {}
    for i in range(rows*cols):
        rowcount = 0
        for row in grid:
            if i in row:
                ipos = row.index(i)
                tilepositions[i] = rowcount * 3 +ipos
            rowcount += 1

    return tilepositions


def calculatepossible(startgrid, targetgrid, rows, cols, debug):
    """Gets the position of each value in a grid.
        
    Keyword arguments:
    startgrid -- the starting grid.
    targetgrid -- the target grid.
    rows -- the number of rows.
    cols -- the number of columns.
    debug -- boolean for DEBUG mode.
    """

    startgpos = getgriddiction(startgrid, rows, cols) # Generates starting position dictionary
    targetgpos = getgriddiction(targetgrid, rows, cols) # Generates target position dictionary
    collisions = 0 # Number of inversions
    position = 0  # Pointer of current position

    for a in range(rows):
        for b in range(cols):
            currenttile = startgrid[a][b] # Works through starting grid getting the tile at each position.
            if currenttile != 0:
                #print("Current Tile: " + str(currenttile))
                for c in range(rows):
                    for d in range(cols):
                        checktile = startgrid[c][d] #  Gets tile to check against
                        if checktile != 0:
                            #print("Check Tile: " + str(checktile) + " Position: " + str(position) + " CTpos: " + str(startgpos[checktile]) + " TGpos: " + str(targetgpos[checktile]))
                            if startgpos[checktile] > position: # If the check tile is behind current tile
                                #print(str(checktile) + " compared with " + str(targetgpos[currenttile]))
                                if checktile < targetgpos[currenttile]: 
                                    collisions += 1 # If inversion +1 to number of inversions
            position += 1
    
    if debug:
        print("Number of inversions: " + str(collisions))
    
    if collisions % 2 == 0:
        return True # If even, return True
    else:
        return False # If odd, return False



def possiblemoves(puzzlegrid):
    """Finds the possible moves from a given grid.
        
    Keyword arguments:
    puzzlegrid -- the grid to find the children nodes of.
    """
    moves = [] # List of possible children from current grid
    # Creates 4 deepcopies of the current grid (doesn't work with shallow copies)
    movegrid1 = copy.deepcopy(puzzlegrid)
    movegrid2 = copy.deepcopy(puzzlegrid)
    movegrid3 = copy.deepcopy(puzzlegrid)
    movegrid4 = copy.deepcopy(puzzlegrid)
    
    for i in range(cols):
        for j in range(rows):
            if puzzlegrid[i][j] == 0:
                a, b = i,j # Find position of the 0


    if a != 0: # If a is not minimum
        movegrid1[a][b] = puzzlegrid[a-1][b]
        movegrid1[a-1][b] = 0
        # Swap with tile to the left
        moves.append(movegrid1.copy())
        
    if a != (rows-1): # If a is not maximum
        movegrid2[a][b] = puzzlegrid[a+1][b]
        movegrid2[a+1][b] = 0
        # Swap with tile to the right
        moves.append(movegrid2.copy())
        
    if b != 0: # If b is not minimum
        movegrid3[a][b] = puzzlegrid[a][b-1]
        movegrid3[a][b-1] = 0
        # Swap with tile above
        moves.append(movegrid3.copy())
        
    if b != (rows-1): # If b is not maximum
        movegrid4[a][b] = puzzlegrid[a][b+1]
        movegrid4[a][b+1] = 0
        # Swap with tile below
        moves.append(movegrid4.copy())
        
    return moves # Return children list

def printcurrentinfo(startgrid, targetgrid, h):
    """Prints the current starting grid, target grid, and heuristic.
        
    Keyword arguments:
    startgrid -- the starting grid.
    targetgrid -- the target grid.
    h -- the heurstic choice
    """
    print("Start grid: ")
    print()
    printgrid(startgrid) # Print starting grid
    print()
    print("Target grid: ")
    print()
    printgrid(targetgrid) #  Print target grid
    # Displays Heuristic
    print("Heuristic: ")
    print()
    if h == 0:
        print("Misplaced Squares") 
    elif h == 1:
        print("Manhattan Distance")
    elif h == 2:
        print("Double Misplaced Squares (Not Admissable)")
    else:
        print("NO HEURISTIC!")
    print()

    input("Please press enter to continue...") # Press enter to continue


def customise(cols, rows, debug, startgrid, targetgrid, h):
    """Opens the customisation menu for users to customise program parameters and grid.
        
    Keyword arguments:
    cols -- the number of columns.
    rows -- the number of rows.
    debug -- boolean to whether DEBUG mode is activated.
    startgrid -- the starting grid.
    targetgrid -- the target grid.
    h -- currently selected heuristic.
    """
    donecustomising = False # Set to False whilst user doesn't want to quit
    while donecustomising == False:
        clearConsole() # Clear
        print("Customisation Menu:")
        print("1. Enable DEBUG view.")
        print("2. Change Heuristic.")
        print("3. Enter a Start Grid.")
        print("4. Enter a Target Grid.")
        print("5. Randomly Generate a 3x3 Start Grid")
        print("6. Change Grid Dimensions. (EXPERIMENTAL - MAY NOT WORK)")
        print("7. Back")
        userchoice = input() #User makes choice
        if userchoice == '1':
            debug = True # Enables DEBUG mode. (for testing)
            print("DEBUG mode enabled, will print current node information when program is run from the main menu.")
            print()
            input("To return to the customisation menu, please press enter...")
            
        elif userchoice == '2':
            h = inputh()
            print()
            input("To return to the customisation menu, please press enter...")

        elif userchoice == '3':
            print('Current start grid:')
            printgrid(startgrid) # Prints current starting grid
            startgrid = setupgrid(usersetgrid(cols, rows)) # Sets up grid using setupgrid() and usersetgrid()
                
        elif userchoice == '4':
            print('Current target grid:')
            printgrid(targetgrid) # Prints current target grid
            targetgrid = setupgrid(usersetgrid(cols, rows)) # Sets up grid using setupgrid() and usersetgrid()
            
        elif userchoice == '5':
            orderedlist = [0,1,2,3,4,5,6,7,8]
            possiblegrid = False
            while possiblegrid == False:
                random.shuffle(orderedlist)
                startgrid = setupgrid(orderedlist) # Randomly generates a starting grid
                possiblegrid = calculatepossible(startgrid, targetgrid, rows, cols, False) 
            print("New Start Grid: ")
            printgrid(startgrid) # Print new starting grid
            print()
            input("To return to the customisation menu, please press enter...")
        
        elif userchoice == '6':
            size = int(input("Enter grid size: ")) # choose size of grid

            cols, rows = (size, size) # Sets grid to square (just for simplicity)
            print("Set up starting grid:")
            startgrid = setupgrid(usersetgrid(cols, rows)) # Sets up grid using setupgrid() and usersetgrid()
            print("Set up target grid:")
            targetgrid = setupgrid(usersetgrid(cols, rows)) # Sets up grid using setupgrid() and usersetgrid()
        
        elif userchoice == '7':
            donecustomising = True # Lets user leave this menu
    
    return cols, rows, debug, startgrid, targetgrid, h #returns the values that may have been customised
            
rows, cols = (3,3) # Rows and Columns (by default 3 x 3)
debug = False # If DEBUG mode is set to True, the program will print information about each node.
quitter = False # Set to False whilst user doesn't want to quit
clearConsole()

print("Welcome to the 8 Tile Puzzle A* Search.")
print()
print("Before we begin...")
general = input("Would you like to choose the start and target grids? Enter '1' if so (any other input will result in using the example grid). ")
if general == '1':
    print("Enter start grid: ")
    startgrid = setupgrid(usersetgrid(cols, rows)) # Sets up grid using setupgrid() and usersetgrid()
    print("Enter target grid: ")
    targetgrid = setupgrid(usersetgrid(cols, rows)) # Sets up grid using setupgrid() and usersetgrid()
else:
    startgrid = setupgrid([7,2,4,5,0,6,8,3,1]) # Default starting grid (set to example from specification)
    targetgrid = setupgrid([0,1,2,3,4,5,6,7,8]) # Default target grid (how the puzzle normally works)
h = inputh()
printcurrentinfo(startgrid, targetgrid, h)

# MAIN MENU SECTION
while quitter == False:
    routes = PriorityQueue() # Open list
    donemoves = [] # Closed list
    moves = [] # List of children nodes from the node
    distance = 0 # Number of moves to the point
    clearConsole()
    if (rows, cols) == (3,3):
        ispossible = calculatepossible(startgrid, targetgrid, rows, cols, debug)
    else:
        ispossible = True
    print("Welcome to the 8 Tile Puzzle A* Search.")
    print()
    print("Menu:")
    print("1. Run")
    print("2. View Current Information")
    print("3. Customise")
    print("4. Quit")
    userchoice = input() # User enters their choice

    if userchoice == '1':
        if ispossible == True:
            t0 = time.time() # Start timer
            print("Running, this may take some time:") # May take up to 20 minutes
            puzzlegrid = State(startgrid, 0, []) # Creates start state
            while puzzlegrid.grid != targetgrid: # While solution not found.
                moves = possiblemoves(puzzlegrid.grid) # Generates possible child nodes of the current state
                for move in moves: # For each move
                    route = State(move,distance,puzzlegrid) # Create a State object from the grid and its g and h values
                    # Check if node is in closed list.
                    if route.grid not in donemoves:
                        routes.put((route.f, route)) # If not, add to priority queue.
                nextmove = routes.get()[1] # Returns the state from the next node.
                donemoves.append(nextmove.grid) # Adds grid to closed list
                puzzlegrid = nextmove # Updates current state
                distance = puzzlegrid.g + 1 # Increment distance
                if debug == True:
                    printfgh(puzzlegrid) # If DEBUG mode, print node information
                if routes.empty():
                    print("Solution Impossible...") # If there are no more possible moves, then finding a solution is impossible.
                    break

            t1 = time.time() # End timer

            #grid printing
            if puzzlegrid.grid == targetgrid:
                print(True)
                solution = []
                node = puzzlegrid 
                while node != startgrid: # Recursion to find parent nodes.
                    if node == []:
                        # Base case
                        break
                    else:
                        solution.append(node.grid) # Add node to path
                        node = node.ls # Find node's parent

                solution.reverse() # Reverse path so it is order of traversal
                i = 0
                for grid in solution:
                    print(str(i) + ")")
                    printgrid(grid) # Print steps
                    i += 1

            print()
            timetaken = t1-t0 # Finds time taken.
            print("Running finished. Time taken: " + str(timetaken) + " seconds. (" + str(timetaken/60) + " minutes)")
        else:
            print("Not mathematically possible to reach solution. Please try a different starting grid.")
        input("To return to the menu, please press enter...")
    
    elif userchoice == '2':
        printcurrentinfo(startgrid, targetgrid, h)
            
    elif userchoice == '3':
        cols, rows, debug, startgrid, targetgrid, h= customise(cols, rows, debug, startgrid, targetgrid, h) # Go to customisation menu

    elif userchoice == '4':
        quitter = True # Ends program

    
