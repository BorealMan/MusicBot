# Written by RK
# Implementation of Basic Data Structures
class Stack:
    def __init__(self):
        self.stack = []

    def Push(self, *value):
        for v in value:
            self.stack.append(v)

    def Pop(self):
        if not self.Empty():
            return self.stack.pop(-1)

    def Empty(self):
        return len(self.stack) <= 0    

class Queue:
    def __init__(self, max_size = 100):
        self.queue = []
        self.max_size = max_size

    def Enqueue(self, *value):
        for v in value:
            self.queue.append(v)

    def Dequeue(self):
        if not self.Empty():
            return self.queue.pop(0)
    
    def Empty(self):
        return len(self.queue) <= 0

    def EnqueueFront(self, *value):
        for v in reversed(value):
            self.queue.insert(0, v)

    def Clear(self):
        self.queue = []

    def Full(self):
        return self.Size() >= self.max_size
    
    def Size(self):
        return len(self.queue)


from heapq import heappush, heappop

class PriorityQueue:
    def __init__(self):
        self.heap = []

    def Enqueue(self, *value):
        for v in value:
            heappush(self.heap, v)

    def Dequeue(self):
        if not self.Empty():
            return heappop(self.heap)
    
    def Empty(self):
        return len(self.heap) <= 0

