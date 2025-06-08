#to do
# make func to generate neighbours
# make func to compare the 3 heuristics
# find the 3rd heuristic
# implement the rest of A*

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

# heuristic two determines the (concept name i forgot) distance
# it was manhattan distance
def heuristic_two(state):

    positions = {}
    distance = 0
    for i in range(3):
        for j in range(3):
            positions[goal[i][j]] = (j,i)


    for i in range(3):
        for j in range(3):
            value = state[i][j]
            gx,gy = positions[value]

            distance += abs(gx-j) + abs(gy-i)

    return distance

#def heuristic_three(state):

# generates a valid starting state for the 8-puzzle
def gen_state():

    while(1):
        starting_state = [ [],[],[] ]
        numbers = [0,1,2,3,4,5,6,7,8]

        for i in range(3):
            for j in range(3):
                r_num = randint(0,len(numbers)-1)
                value = numbers.pop(r_num)
                starting_state[i].append(value) 

        if(valid_state(starting_state)):
            return starting_state


# determines if an initial starting state is valid
def valid_state(state):
    sequence = []
    inversions = 0

    for i in range(3):
        for j in range(3):
            if(state[i][j]!=0):
                sequence.append(state[i][j])
    
    for i in range(len(sequence)):
        for j in range(i+1,len(sequence)):
            if sequence[i] > sequence[j]:
                inversions += 1

    return inversions % 2 == 0



def generate_neighbours(state):
    neighbours = []
    moves = [ (0,1), (0,-1), (1,0), (-1,0) ]

    for i in range(3):
        for j in range(3):
            if(state[i][j]==0):
                x,y = j,i


    for move in moves:
        temp_state = deepcopy(state)

        new_x = x + move[1]
        new_y = y + move[0]

        if(0<= new_y < 3 and 0<= new_x < 3):
            temp = temp_state[y][x]
            temp_state[y][x] = temp_state[new_y][new_x]
            temp_state[new_y][new_x] = temp

            neighbours.append(temp_state)


    return neighbours


def a_star_search(initial_state, heuristic):

    start_node = HeapNode(heuristic(initial_state),0,initial_state,[])
    frontier = MinHeap(start_node)
    explored = set()

    while(not frontier.is_empty()):
        removed_heap_node = frontier.delete()
        state = removed_heap_node.state
        path = removed_heap_node.path
        g_value = removed_heap_node.g + 1


        #explored.add(str(state))
        state_tup = state_to_tuple(state)
        explored.add(state_tup)
        

        if(goal_state(state)):
            
            #return path + [str(state)], len(explored)
            return path + [state_tup], len(explored)
        
        else:
            #neighbour_path = deepcopy(path) + [str(state)]
            neighbour_path = deepcopy(path) + [state_tup]

            for neighbour in generate_neighbours(state):
                neighbour_tup = state_to_tuple(neighbour)

                #if not frontier.search_node(neighbour) and str(neighbour) not in explored:
                if not frontier.search_node(neighbour) and not neighbour_tup in explored:
                #if not frontier.search_node(neighbour) and not neighbour in explored:
                    
                    f_value = g_value+heuristic(neighbour)
                    hnode = HeapNode(f_value,g_value,neighbour, neighbour_path)
                    frontier.insert(hnode)

                elif frontier.search_node(neighbour):
                    f_value = g_value+heuristic(neighbour)
                    frontier.decrease_key(neighbour,f_value,g_value,neighbour_path)

    return None, None

def main():

    h1_avg_expands = 0
    h1_avg_steps = 0

    h2_avg_expands = 0
    h2_avg_steps = 0

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
    print(f"""
H1 avg steps = {h1_avg_steps}
H1 avg expands = {h1_avg_expands}
H2 avg steps = {h2_avg_steps}
H2 avg expands = {h2_avg_expands}

""")


""""""
initial_state = gen_state()

h1s,h1e = a_star_search(initial_state, heuristic_one)

print(len(h1s))
print(h1e)
