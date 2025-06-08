
from random import randint
from copy import deepcopy
from heap import MinHeap, HeapNode

#default goal state, 0 represents empty cell
#will be used in comparisons for the A* search
goal = [
    [0,1,2],
    [3,4,5],
    [6,7,8]
]

# used to convert states to immutable object to store within set (explored)
def state_to_tuple(state):
    return tuple(tuple(row) for row in state)


#compares current state to the goal state
def goal_state(state):
    return state==goal 

#converts a state to 1D representation for easier comparison
def convert_to_1D(state):
    list = []
    for row in state:
        for element in row:
            list.append(element)
    
    return list

#heuristic one determines the number of misplaced tiles
def heuristic_one(state):
    count  = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] != goal[i][j]:
                count +=1
    
    return count 

# heuristic two implements the manhattan distance

def heuristic_two(state):

    # position is dictionary that stores (x,y) coordinate of every puzzle piece
    positions = {}
    distance = 0
    for i in range(3):
        for j in range(3):
            positions[goal[i][j]] = (j,i)


    for i in range(3):
        for j in range(3):
            # for every tile, get the manhattan distance and add to total
            value = state[i][j]
            gx,gy = positions[value]

            distance += abs(gx-j) + abs(gy-i)

    
    return distance

#def heuristic_three(state):

# generates a valid starting state for the 8-puzzle
def gen_state():

    while(1):
        #empty 3x3 matrix with set of tiles for the puzzle, 0 represents blank
        starting_state = [ [],[],[] ]
        numbers = [0,1,2,3,4,5,6,7,8]

        for i in range(3):
            for j in range(3):
                #generate random number from 0 to length of numbers array 
                #the numbers array contains the tiles that havent been added to starting state
                r_num = randint(0,len(numbers)-1)
                value = numbers.pop(r_num)
                starting_state[i].append(value) 

        #checks if a state is valid before returning
        #only half of the 9! possible states are solvable (inversions)
        if(valid_state(starting_state)):
            return starting_state


# determines if an initial starting state is valid
def valid_state(state):
    sequence = []
    inversions = 0

    #flattens the state into a 1D array to check for inversions
    for i in range(3):
        for j in range(3):
            if(state[i][j]!=0):
                sequence.append(state[i][j])
    
    #counts number of tiles with value less than current
    #if this sum is not divisible by 2, state is unsolvable 
    for i in range(len(sequence)):
        for j in range(i+1,len(sequence)):
            if sequence[i] > sequence[j]:
                inversions += 1

    return inversions % 2 == 0



def generate_neighbours(state):
    neighbours = []
    #four possible moves for a blank space, not all are valid depending on state
    moves = [ (0,1), (0,-1), (1,0), (-1,0) ]

    #determines (x,y) position of blank tile
    for i in range(3):
        for j in range(3):
            if(state[i][j]==0):
                x,y = j,i

    #iterates over every move tuple 
    for move in moves:
        temp_state = deepcopy(state)

        #applies transformation to the coordinates
        new_x = x + move[1]
        new_y = y + move[0]

        #if the transformation is invalid (outside of the 3x3 grid), it is skipped
        if(0<= new_y < 3 and 0<= new_x < 3):
            temp = temp_state[y][x]
            temp_state[y][x] = temp_state[new_y][new_x]
            temp_state[new_y][new_x] = temp

            #valid transformations are added to the neighbour state array which is then return
            neighbours.append(temp_state)


    return neighbours


def a_star_search(initial_state, heuristic):

    #frontier is a min heap with f(n) as key value
    #start_node is the node heap will be initialized with
    #explored is a set containing tuple representation of state
    start_node = HeapNode(heuristic(initial_state),0,initial_state,[])
    frontier = MinHeap(start_node)
    explored = set()

    while(not frontier.is_empty()):
        #remove heap node with minimum f(n) value
        removed_heap_node = frontier.delete()

        #determine state,path, g value of the next level
        #the current g value is incremented by 1 and will be used
        #as g value for neighbour states
        state = removed_heap_node.state
        path = removed_heap_node.path
        g_value = removed_heap_node.g + 1


        #convert current state to a tuple
        state_tup = state_to_tuple(state)

        #if state already exists in explored, it wasnt a goal state, can skip to next iteration
        if state_tup in explored:
            continue

        explored.add(state_tup)
        
        #determines if the current state is goal state
        if(goal_state(state)):
            
            #returns the path to the current state and the number of nodes explored
            #an explored node is one whose neighbours were generated
            return path + [state_tup], len(explored)
        
        else:
            #path of neighbour states
            neighbour_path = path + [state_tup]

            for neighbour in generate_neighbours(state):
                neighbour_tup = state_to_tuple(neighbour)

                #if the neighbour has been explored, dont add to heap
                #go to next neighbour
                if neighbour_tup in explored:
                    continue 

                #if not in explored and not in heap, add it as a new heap node
                if not frontier.search_node(neighbour):
                    
                    f_value = g_value+heuristic(neighbour)
                    hnode = HeapNode(f_value,g_value,neighbour, neighbour_path)
                    frontier.insert(hnode)

                #if in the heap decrease the key
                #the decrease key method ensures new f-value is less than current before calling heapify
                elif frontier.search_node(neighbour):
                    f_value = g_value+heuristic(neighbour)
                    frontier.decrease_key(neighbour,f_value,g_value,neighbour_path)

    #if search fails return none
    return None, None

#main function, tests the heuristics and summarizes results
def main():

    h1_avg_expands = 0
    h1_avg_steps = 0

    h2_avg_expands = 0
    h2_avg_steps = 0

    h3_avg_expands = 0
    h3_avg_steps = 0

    for i in range(100):
        initial_state = gen_state()

        h1s,h1e = a_star_search(deepcopy(initial_state), heuristic_one)
        h2s,h2e = a_star_search(deepcopy(initial_state), heuristic_two)
        #same for h3

        h1_avg_expands += h1e
        h1_avg_steps += len(h1s)

        h2_avg_expands += h2e
        h2_avg_steps += len(h2s)
    
    h1_avg_expands /=100
    h1_avg_steps /=100

    h2_avg_expands /=100
    h2_avg_steps /=100 

    h3_avg_expands /=100
    h3_avg_steps /=100 
    print(f"""
H1 avg steps = {h1_avg_steps}
H1 avg expands = {h1_avg_expands}
H2 avg steps = {h2_avg_steps}
H2 avg expands = {h2_avg_expands}

""")


""""""

#call to main, generates results
#will take some time plz wait
main()
