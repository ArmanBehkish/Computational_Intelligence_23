# queues.py
# from the RealPython Tutorial "https://realpython.com/queue-in-python/" 
from heapq import heappop, heappush

# ...

class PriorityQueue:
    def __init__(self):
        self._elements = []

    def enqueue_with_priority(self, value, priority):
        heappush(self._elements, (priority,value))

    def dequeue(self):
        return heappop(self._elements)

    def get_elements(self):
        return [x for x in self.get_elements[1]]