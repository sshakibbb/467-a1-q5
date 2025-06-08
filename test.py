from copy import deepcopy
from random import randint

class HeapNode:
    def __init__(self, f, g, state, path):
        self.f = f  # total cost = g + h
        self.g = g  # cost so far
        self.state = state  # state as list of lists
        self.path = path    # list of states (tuples) leading here

class MinHeap:
    def __init__(self):
        self.heap = []
        self.pos_map = {}  # state_tuple -> index in heap for quick lookup
    
    def _swap(self, i, j):
        self.pos_map[self._state_tuple(self.heap[i].state)] = j
        self.pos_map[self._state_tuple(self.heap[j].state)] = i
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    def _state_tuple(self, state):
        return tuple(tuple(row) for row in state)

    def _heapify_up(self, idx):
        while idx > 0:
            parent = (idx -1)//2
            if self.heap[parent].f > self.heap[idx].f:
                self._swap(parent, idx)
                idx = parent
            else:
                break

    def _heapify_down(self, idx):
        size = len(self.heap)
        while True:
            left = 2*idx + 1
            right = 2*idx + 2
            smallest = idx

            if left < size and self.heap[left].f < self.heap[smallest].f:
                smallest = left
            if right < size and self.heap[right].f < self.heap[smallest].f:
                smallest = right
            
            if smallest != idx:
                self._swap(idx, smallest)
                idx = smallest
            else:
                break

    def insert(self, node):
        state_tup = self._state_tuple(node.state)
        self.heap.append(node)
        idx = len(self.heap) - 1
        self.pos_map[state_tup] = idx
        self._heapify_up(idx)

    def delete_min(self):
        if not self.heap:
            return None
        min_node = self.heap[0]
        last_node = self.heap.pop()
        del self.pos_map[self._state_tuple(min_node.state)]
        if self.heap:
            self.heap[0] = last_node
            self.pos_map[self._state_tuple(last_node.state)] = 0
            self._heapify_down(0)
        return min_node

    def contains(self, state):
        return self._state_tuple(state) in self.pos_map

    def decrease_key(self, state, new_f, new_g, new_path):
        state_tup = self._state_tuple(state)
        if state_tup not in self.pos_map:
            return
        idx = self.pos_map[state_tup]
        node = self.heap[idx]
        if new_f < node.f:
            node.f = new_f
            node.g = new_g
            node.path = new_path
            self._heapify_up(idx)

    def is_empty(self):
        return len(self.heap) == 0


goal = [
    [0,1,2],
    [3,4,5],
    [6,7,8]
]

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



def state_to_tuple(state):
    return tuple(tuple(row) for row in state)

def goal_state(state):
    return state == goal

def heuristic_one(state):
    # Misplaced tiles (excluding blank)
    count = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] != 0 and state[i][j] != goal[i][j]:
                count += 1
    return count

def heuristic_two(state):
    # Manhattan distance
    positions = {}
    for i in range(3):
        for j in range(3):
            positions[goal[i][j]] = (i, j)
    dist = 0
    for i in range(3):
        for j in range(3):
            val = state[i][j]
            if val != 0:
                goal_i, goal_j = positions[val]
                dist += abs(goal_i - i) + abs(goal_j - j)
    return dist

def generate_neighbours(state):
    neighbours = []
    moves = [(0,1),(0,-1),(1,0),(-1,0)]

    # Find blank
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                x, y = j, i

    for dx, dy in moves:
        nx, ny = x + dx, y + dy
        if 0 <= nx < 3 and 0 <= ny < 3:
            new_state = deepcopy(state)
            new_state[y][x], new_state[ny][nx] = new_state[ny][nx], new_state[y][x]
            neighbours.append(new_state)
    return neighbours

def a_star_search(initial_state, heuristic):
    start_node = HeapNode(heuristic(initial_state), 0, initial_state, [state_to_tuple(initial_state)])
    frontier = MinHeap()
    frontier.insert(start_node)
    explored = set()

    while not frontier.is_empty():
        current = frontier.delete_min()
        cur_state_tup = state_to_tuple(current.state)

        if cur_state_tup in explored:
            continue
        explored.add(cur_state_tup)

        if goal_state(current.state):
            return current.path, len(explored)

        for neighbor in generate_neighbours(current.state):
            neighbor_tup = state_to_tuple(neighbor)
            if neighbor_tup in explored:
                continue

            g_new = current.g + 1
            f_new = g_new + heuristic(neighbor)
            new_path = current.path + [neighbor_tup]

            if not frontier.contains(neighbor):
                frontier.insert(HeapNode(f_new, g_new, neighbor, new_path))
            else:
                frontier.decrease_key(neighbor, f_new, g_new, new_path)

    return None, None


if __name__ == "__main__":
    # Example scrambled initial state
    exp = 0
    pl = 0
    for i in range(100):

        initial = gen_state()

        path, expanded = a_star_search(initial, heuristic_one)
        pl += len(path)-1
        exp += expanded
    
    print(exp/100)
    print(pl/100)
        
