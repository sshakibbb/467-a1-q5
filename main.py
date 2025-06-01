#to do
# make func to generate neighbours
# make func to compare the 3 heuristics
# find the 3rd heuristic
# implement the rest of A*

from random import randint
from copy import deepcopy
from heap import MinHeap, HeapNode

#default goal state, 0 represents empty cell
goal = [
    [0,1,2],
    [3,4,5],
    [6,7,8]
]

#compares current state to the goal state
def goal_state(state):
    return state==goal 


#heuristic one determines the number of misplaced tiles
def heuristic_one(state):
    count  = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] != goal[i][j]:
                count +=1
    
    return count 

#heuristic two determines the (concept name i forgot) distance
# it was manhattan distance
def heuristic_two(state):

    positions = {}

    for i in range(3):
        for j in range(3):
            positions[goal[i][j]] = (i,j)


    for i in range(3):
        for j in range(3):
            value = state[i][j]
            gx,gy = positions[value]

            distance = abs(gx-j) + abs(gy-i)

    return distance

#def heuristic_three(state):

# generates a valid starting state for the 8-puzzle
def gen_state():

    while(1):
        starting_state = [[],[],[]]
        numbers = [0,1,2,3,4,5,6,7,8]

        for i in range(3):
            for j in range(3):
                r_num = randint(0,len(numbers)-1)
                value = numbers.pop(r_num)
                starting_state[i][j] = value 

        if(valid_state(starting_state)):
            return starting_state


# determines if an initial starting state is valid
def valid_state(state):
    sequence = []
    inversions = 0

    for i in range(3):
        for j in range(3):
            sequence.append(state[i][j])
    
    for i in range(1,9):
        if sequence[i] < sequence[i-1]:
            inversions += 1

    return inversions % 2 == 0

def generate_neighbours(state):
    neighbours = []
    moves = { (0,1), (0,-1), (1,0), (-1,0) }

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

    while(not frontier.isempty()):
        removed_heap_node = frontier.delete()
        state = removed_heap_node.state
        path = removed_heap_node.path
        g_value = removed_heap_node.g + 1


        explored.add(str(state))

        if(goal_state(state)):
            
            return path + [str(state)]
        
        else:
            neighbour_path = path + [str(state)]

            for neighbour in generate_neighbours(state):
                if not frontier.search_node(neighbour) and str(neighbour) not in explored:
                    f_value = g_value+heuristic(neighbour)
                    hnode = HeapNode(f_value,g_value,neighbour, neighbour_path)
                    frontier.insert(hnode)

                elif frontier.search_node(neighbour):
                    f_value = g_value+heuristic(neighbour)
                    frontier.decrease_key(neighbour,f_value,g_value,neighbour_path)

    return None

def main():

    h1_avg = 0
    h1_steps = []

    h2_avg = 0
    h2_steps = []

    for i in range(100):
        initial_state = gen_state()

        h1 = a_star_search(deepcopy(initial_state),heuristic_one)
        h2 = a_star_search(deepcopy(initial_state),heuristic_two)
        #same for h3

        h1_steps.append(len(h1))
        h2_steps.append(len(h2))

        h1_avg += len(h1)
        h2_avg += len(h2)
    
    h1_avg/= 100
    h2_avg/=100





