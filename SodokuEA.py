# SODOKU EVOLUTIONARY ALGORITHM  

from random import choice, random, seed
import time 

### EVOLUTIONARY ALGORITHM ###

def evolve():
    currentbest = [] # The current best individual.
    population = create_pop() # Creates population
    fitness_population = evaluate_pop(population) # Evaluates population
    for gen in range(NUMBER_GENERATION):
        mating_pool = select_pop(population, fitness_population) # creates mating pool
        offspring_population = crossover_pop(mating_pool) # Crossover
        population = mutate_pop(offspring_population) # Mutated population
        fitness_population = evaluate_pop(population) # Evaluate fitness
        best = best_pop(population, fitness_population) # Finds the best value in current value
        best_ind, best_fit = best[0], best[1] 
        print("#%3d" % gen, "fit: %3d" % best_fit) # Print out best fir
        print_sudoku(best_ind) # Print best grid
        if currentbest != []: # If there is a current best grid
            if best_fit < currentbest[1]: # If it is a better fit
                currentbest = best # Update current best
        else:
            currentbest = best # Set current best  if there isn't one
        if best_fit == 0: # If solution found
            break # Exit loop

    return currentbest # Return current best

### POPULATION-LEVEL OPERATORS ###

def create_pop():
    return [ create_ind() for _ in range(POPULATION_SIZE) ] # Creates a population (list of individuals). 

def evaluate_pop(population):
    return [ evaluate_ind(individual) for individual in population ] # Creates a list of the fitness of each individual in the population.

def select_pop(population, fitness_population):
    sorted_population = sorted(zip(population, fitness_population), key = lambda ind_fit: ind_fit[1]) # Zips the population with its fitness. Then sorts them based on lowest fitness.
    return [ individual for individual, fitness in sorted_population[:int(POPULATION_SIZE * TRUNCATION_RATE)] ]

def crossover_pop(population):
    return [ crossover_ind(choice(population), choice(population)) for _ in range(POPULATION_SIZE) ] # Crossover function.

def mutate_pop(population):
    return [ mutate_ind(individual) for individual in population ] # Mutates each individual in population.

def best_pop(population, fitness_population):
    return sorted(zip(population, fitness_population), key = lambda ind_fit: ind_fit[1])[0] # Returns the best in the population.

### INDIVIDUAL-LEVEL OPERATORS: REPRESENTATION & PROBLEM SPECIFIC ###

alphabet = [1,2,3,4,5,6,7,8,9] # List of possible values.

def importgrid(filename):
    f = open(filename, "r") # Opens file
    rowcount = 1 # Counts current row
    grid = [] # Output grid
    for row in f: # for each row
        if rowcount != 4: 
            if rowcount != 8:
                # Rows aren't the gaps
                thisrow = []
                for letter in row:
                    if letter not in str(alphabet): # If not a value
                        if letter == ".": # If it is blank space
                            thisrow.append(0) # put a 0
                    else:
                        thisrow.append(int(letter)) # Is value then add it

                grid.append(thisrow) # Add to grid

        rowcount += 1 # Increment row
    
    return grid # Return grid

def create_ind():
    newgrid = [] # New grid
    for row in grid:
        already = set(row) # Numbers already in row
        if 0 in already:
            already.remove(0) # Remove 0 if it in row
        possnumber = [x for x in alphabet if x not in already] # Calculates all possible numbers from numbers not already in the row.
        newrow = []
        for number in row:
            if number == 0: #if number is a 0
                number = choice(possnumber) # Replace it with a possible number.
            newrow.append(number)
        newgrid.append(newrow)
    return newgrid # Returns new grid (individual in population)

def evaluate_ind(individual):
    sum = 0
    
    # rows
    for row in individual:
        numbersinrow = [] # Create list of numbers in row
        for number in row:
            if number in numbersinrow: # if number already in row
                sum += 1 # Add 1
            else:
                numbersinrow.append(number) # add to list of number in row
    
    # columns
    for i in range(0,9):
        column = [] # Create list of numbers in column
        for j in range(0,9):
            column.append(individual[j][i])
        numbersincol = []
        for number in column:
            if number in numbersincol: # if number already in column
                sum += 1 # Add 1
            else:
                numbersincol.append(number) # add to list of number in column

    #subgrids
    for a in range(0,3):
        for b in range(0,3):
            subgrid = [] # Create list of numbers in sub grid
            for c in range(0,3):
                for d in range(0,3):
                    subgrid.append(individual[c+3*a][d+3*b])
            numbersingrid = []
            for number in subgrid:
                if number in numbersingrid: # if number already in sub grid
                    sum += 1 # Add 1
                else:
                    numbersingrid.append(number) # add to list of number in sub grid
        
    return sum

def crossover_ind(individual1, individual2):
    newgrid = []
    for i in range(len(grid)):
        newrow = [choice(ch_pair) for ch_pair in zip(individual1[i], individual2[i])] # Generates a new row of different digits
        newgrid.append(newrow) # Adds it to new grid

    return newgrid # Return new grid

def mutate_ind(individual):
    for h in range(len(individual)): # For each row
        row = individual[h]
        already = set(grid[h]) # values in original grid
        possnumber = [x for x in alphabet if x not in already] # Numbers that aren't in original grid
        
        if possnumber != []: # If there is a list of possible numbers
            for _ in row: # For each letter
                if random() < MUTATION_RATE/(len(individual)*len(row)): # If 1/81 chance
                    # Will change a random letter
                    success = False
                    while success == False:
                        randomnumber = int(random() * len(row)) # random position in row
                        if individual[h][randomnumber] != grid[h][randomnumber]: # Check its not from starting grid
                            individual[h][randomnumber] = choice(possnumber) # Change to possible number
                            success = True # Makes sure an item is updated

    return individual

def print_sudoku(board):
    # Prints the sudoku board
    print("-"*37)
    for i, row in enumerate(board):
        print(("|" + " {}   {}   {} |"*3).format(*[x if x != 0 else " " for x in row]))
        if i == 8:
            print("-"*37)
        elif i % 3 == 2:
            print("|" + "---+"*8 + "---|")
        else:
            print("|" + "   +"*8 + "   |")

### PARAMERS VALUES ###

NUMBER_GENERATION = 200
POPULATION_SIZE = 10000
TRUNCATION_RATE = 0.55
MUTATION_RATE = 1.0

### MAIN ###

seed()
grid = importgrid('Grid1.ss')
t0 = time.time() # Start timer
best = evolve()
t1 = time.time() # End timer
timetaken = t1-t0 # Finds time taken
print("Running finished. Time taken: " + str(timetaken) + " seconds.")
print("Best fit: " + str(best[1]))
print_sudoku(best[0])






