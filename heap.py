#heap node that will be used in min heap
#node will contain the f value, the g value (level)
#the state it represents and the path from initial to current
class HeapNode:
    def __init__(self,f,g,state,path):
        self.f = f
        self.g = g 
        self.state = state 
        self.path = path 
    


class MinHeap:
    def __init__(self,intial):
        #the heap will be implemented with an array
        self.heap = []

        #dictionary will be used with tuple representation of state for fast index lookup
        self.state_pos = {} 
        
        self.heap.append(intial)
        self.state_pos[self._state_tuple(intial.state)] = 0
    
    #helper method used to swap heap nodes and their index value in dictionary
    def _swap(self, i, j):
        self.state_pos[self._state_tuple(self.heap[i].state)] = j
        self.state_pos[self._state_tuple(self.heap[j].state)] = i
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    #converts a state to its tuple representation
    def _state_tuple(self, state):
        return tuple(tuple(row) for row in state)

    
    #inserts a heap node into the min heap
    def insert(self, hnode):

        self.heap.append(hnode)
        #heap node added to end of array at index len-1
        i = len(self.heap)-1
        self.state_pos[self._state_tuple(hnode.state)] = i

        #will run till i = 0, the node at index 0 has no parent
        while(i):
            #parent is at index (i-1)//2
            pi = (i-1)//2

            #min heap logic, if the parent key is greater than child, swap, and continue from parent index
            #otherwise break as heap property is maintained
            if (self.heap[pi].f > self.heap[i].f):
                
                self._swap(pi,i)

                i = pi 

            else:
                break


    def delete(self):

        #if only one node in array, pop it and remove the dictionary key
        if len(self.heap) == 1:
            del self.state_pos[self._state_tuple(self.heap[0].state)]
            return self.heap.pop()
        
        #if not the last node, replace the first element (min key value) with the last element
        heap_Min = self.heap[0]
        self.heap[0] = self.heap.pop()
        #update the value of state in dictionary
        del self.state_pos[self._state_tuple(self.heap[0].state)]
        

        i = 0
        child = 2*i+1

        #while the current index node has a child
        while(child<len(self.heap)):
            #if it has two children, choose index of smallest key value child
            if(child<len(self.heap)-1):
                if(self.heap[child].f > self.heap[child+1].f):
                    child+=1
            
            #if parent key is <= child key, min heap property valid, break
            if(self.heap[child].f > self.heap[i].f):
                break 
            else:
                #otherwise swap the parent and child and continue from chil
                self._swap(i,child)
                i = child
                child = 2*i+1

        #return min key node
        return heap_Min
    
    def search_node(self,state):

        #determine if a state exists in heap
        #converts it to tuple representation for fast look up
        return self._state_tuple(state) in self.state_pos
    


    def decrease_key(self,state,new_f,new_g,new_path):
        
        #convert to tuple representation, if state doesn't exist in heap error and return
        state_tup = self._state_tuple(state)

        if state_tup not in self.state_pos:
            return
        
        #find index of state in heap
        index = self.state_pos[state_tup]

        #if the current f(n) value is less than new, no need to update key as the path isnt more efficient
        if(self.heap[index].f < new_f):
            return

        #if it is lower, update the f value, g value, and path
        self.heap[index].f = new_f
        self.heap[index].g = new_g 
        self.heap[index].path = new_path 

        #heapify up if new f value is < parent
        while(index):
            pi = (index-1)//2


            if (self.heap[pi].f > self.heap[index].f):
                
                self._swap(index,pi)
                index = pi 
            else:
                break
        

    #returns true if the heap array is empty
    def is_empty(self):
        return len(self.heap)==0
