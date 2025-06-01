class HeapNode:
    def __init__(self,f,g,state,path):
        self.f = f
        self.g = g 
        self.state = state 
        self.path = path 
    


class MinHeap:
    def __init__(self,intial):
        self.heap = []
        self.heap.append(intial)

    
    def insert(self, hnode):

        self.heap.append(hnode)
        i = len(self.heap)-1
        

        while(i):
            pi = (i-1)//2

            if (self.heap[pi].f > self.heap[i].f):
                temp = self.heap[pi]
                self.heap[pi] = self.heap[i]
                self.heap[i] = temp 
                i = pi 
            else:
                break


    def delete(self):

        if len(self.heap) == 1:
            return self.heap.pop()
        
        heap_Min = self.heap[0]
        self.heap[0] = self.heap.pop()
        

        i = 0
        child = 2*i+1

        while(child<len(self.heap)):
            if(child<len(self.heap)-1):
                if(self.heap[child].f > self.heap[child+1].f):
                    child+=1
            
            if(self.heap[child].f > self.heap[i].f):
                break 
            else:
                temp = self.heap[i]
                self.heap[i] = self.heap[child]
                self.heap[child] = temp 
                i = child
                child = 2*i+1

        return heap_Min
    
    def search_node(self,state):

        for i in range(len(self.heap)):
            if(self.heap[i].state == state):
                return True
            
        return False
    

    def decrease_key(self,state,new_f,new_g,new_path):
        index = 0
        
        #find the heap node containing the state
        for i in range(len(self.heap)):
            if self.heap[i].state == state:
                index = i
                break 
        
        if(self.heap[index].f < new_f):
            return
        
        #update it
        self.heap[index].f = new_f
        self.heap[index].g = new_g 
        self.heap[index].path = new_path


        #heapify up? down?
        while(index):
            pi = (index-1)//2


            if (self.heap[pi].f > self.heap[index].f):
                temp = self.heap[pi]
                self.heap[pi] = self.heap[index]
                self.heap[index] = temp 
                index = pi 
            else:
                break
        

    

    def is_empty(self):
        return len(self.heap)==0
