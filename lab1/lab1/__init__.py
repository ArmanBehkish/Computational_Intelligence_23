import enum
from itertools import count
import logging
import random
from gx_utils import *
from heapq import heappush
from typing import Callable
import statistics
# import queues 

logging.basicConfig(format="%(message)s", level=logging.INFO)

N = 1000
NUMBERS = {x for x in range(N)}


def problem(N, seed=None):
    random.seed(seed)
    return [
        list(set(random.randint(0, N - 1) for n in range(random.randint(N // 5, N // 2))))
        for n in range(random.randint(N, N * 5))
    ]

class State:
    def __init__(self, list_numbers:set):
        self.lists_ = list_numbers.copy()
    def add(self,item):
        self.lists_.add(item)
        return self
    def __hash__(self):
        #return hash(bytes(self.lists_))
        return hash(str(self.lists_))
    def __eq__(self, other):
        #return bytes(self.lists_) == bytes(other.lists_)
        return str(self.lists_) == str(other.lists_)
    def __lt__(self, other):
        #return bytes(self.lists_) < bytes(other.lists_)
        return str(self.lists_) < str(other.lists_)
    def __str__(self):
        return str(self.lists_)
    def __repr__(self):
        return repr(self.lists_)
    def copy_data(self):
        return self.lists_.copy()
    def get_weight(self,ref_lists):
        return len([x for n in self.lists_ for x in ref_lists[n]])
    def get_items(self,ref_lists):
        return set([x for n in self.lists_ for x in ref_lists[n]])


def goal_test(current_state:State,ref_lists):
    """get all the members of the lists in the current_state and check if it covers N"""

    current_numbers = {x for n in current_state.lists_ for x in ref_lists[n]}
    return current_numbers == NUMBERS

def valid_actions(current_state:State,ref_lists):
    """returns set of indexes not currently added to this state"""
    return {indx for indx,_ in enumerate(ref_lists) if indx not in current_state.lists_}

def result(current_state,action):
    next_state=State(current_state.copy_data()).add(action)
    return next_state

def search(initial_state:State, ref_lists,priority_function:Callable):
    frontier = PriorityQueue()
    state = initial_state
    state_count = 0
    while state is not None and not goal_test(state,ref_lists):
        for a in valid_actions(state,ref_lists):
            new_state = result(state,a)
            if new_state not in frontier:
                frontier.push(new_state,p=priority_function(new_state))
            elif new_state in frontier:
                pass
        if frontier:
            state = frontier.pop()
            state_count+=1
        else:
            state = None

    logging.info(f"Found a solution with cost: {state.get_weight(ref_lists)} and {state_count} number of visited states, last state: {state}")
        
def heuristic(state:State,ref_lists,N):
    remained = NUMBERS - state.get_items(ref_lists)
    return len(remained) + random.randint(0,len(remained)//2)


if __name__ == "__main__":
    ref_lists = problem(N,seed=42)
    #print(ref_lists)
    initial_state = State(set())

    # #Breath_first
    # search(initial_state, ref_lists,priority_function=lambda state: state.get_weight(ref_lists))

    # #Depth_first
    # search(initial_state, ref_lists,priority_function=lambda state: -state.get_weight(ref_lists))

    # #Heuristic
    search(initial_state, ref_lists,priority_function=lambda state: heuristic(state,ref_lists, N))

    #A*
    #search(initial_state, ref_lists,priority_function=lambda state: heuristic(state,ref_lists, N) + state.get_weight(ref_lists))





# N=10, breath-first, Found a solution with cost: 10 and 88173 number of visited states, last state: {0, 11, 35, 15}
# N=20, breath-first, Found a solution with cost: 23 and 71303 number of visited states, last state: {0, 11, 18, 19, 30} 
# Found a solution with cost: 10 and 90379 number of visited states, last state: {0, 8, 2, 38}
# Found a solution with cost: 35 and 8 number of visited states, last state: {16, 34, 18, 6, 10, 28, 29, 47}  "-"
# Found a solution with cost: 39 and 9 number of visited states, last state: {34, 6, 10, 16, 18, 20, 24, 28, 29}
#search(initial_state, ref_lists,priority_function=lambda state: heuristic(state,ref_lists, N))






