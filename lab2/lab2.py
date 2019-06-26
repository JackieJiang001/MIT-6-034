# Fall 2012 6.034 Lab 2: Search
#
# Your answers for the true and false questions will be in the following form.  
# Your answers will look like one of the two below:
#ANSWER1 = True
#ANSWER1 = False

# 1: True or false - Hill Climbing search is guaranteed to find a solution
#    if there is a solution
ANSWER1 = False

# 2: True or false - Best-first search will give an optimal search result
#    (shortest path length).
#    (If you don't know what we mean by best-first search, refer to
#     http://courses.csail.mit.edu/6.034f/ai3/ch4.pdf (page 13 of the pdf).)
ANSWER2 = False

# 3: True or false - Best-first search and hill climbing make use of
#    heuristic values of nodes.
ANSWER3 = True

# 4: True or false - A* uses an extended-nodes set.
ANSWER4 = False  # whether one node will be extended, not due to it has already been
                 # extended, but due to whether the traveled path length is less than
                 # the 

# 5: True or false - Breadth first search is guaranteed to return a path
#    with the shortest number of nodes.
ANSWER5 = True

# 6: True or false - The regular branch and bound uses heuristic values
#    to speed up the search for an optimal path.
ANSWER6 = False

# Import the Graph data structure from 'search.py'
# Refer to search.py for documentation
from search import Graph

## Optional Warm-up: BFS and DFS
# If you implement these, the offline tester will test them.
# If you don't, it won't.
# The online tester will not test them.
from graphs import *

def bfs(graph, start, goal):
##    raise NotImplementedError
    path = [start]
    queue = [path]
    extended_nodes = [start]
    # add new paths to the back of the queue
    # pop the path in front of the queue
    while len(queue) > 0 :
        cur_path = queue.pop(0)
        cur_node = cur_path[-1]

        for node in graph.get_connected_nodes(cur_node):
            if node not in extended_nodes:
                extended_nodes.append( node )
                if node == goal:
                    
                    return cur_path + [node]
                else:
                    queue.append( cur_path + [node] )
##                    print 'queue=', queue
    return None

##print bfs(GRAPH3, 'S', 'G')

## Once you have completed the breadth-first search,
## this part should be very simple to complete.
def dfs(graph, start, goal):
##    raise NotImplementedError
    queue = [[start]]
    extended = [start]
    # put new paths to the front of the queue
    # pop the front path in the queue
    while len(queue) > 0:
        cur_path = queue.pop(0)
        cur_node = cur_path[-1]
        new_paths = []

        for node in graph.get_connected_nodes(cur_node):
            if node not in extended:
                extended.append(node)
                if node == goal:
                    return cur_path + [node]
                else:
                    new_paths.append(cur_path + [node])
        queue = new_paths + queue
        print 'queue= ',queue
    return None
##print dfs(GRAPH3, 'S', 'G')

## Now we're going to add some heuristics into the search.  
## Remember that hill-climbing is a modified version of depth-first search.
## Search direction should be towards lower heuristic values to the goal.
def add_to_dict(dictionary, value, key):
    if key in dictionary:
        
        dictionary[key].append(value)
    else:
        dictionary[key] = [value]

def hill_climbing(graph, start, goal):
##    raise NotImplementedError
    # sort the new paths by the distance between their terminal node to the goal
    # put new paths to the front of the queue
    # pop the front path in the queue    
    queue = [[start]]
    extended = [start]
    while len(queue) > 0:
        cur_path = queue.pop(0)
        cur_node = cur_path[-1]
        new_paths = {}
        for node in graph.get_connected_nodes(cur_node):
            if node not in extended:
                extended.append(node)
                if node == goal:
                    return cur_path + [node]
                else:
                    add_to_dict(new_paths, cur_path + [node], graph.get_heuristic(node, goal))
        new_paths_sorted = []
        for distance in sorted(new_paths):
            for path in new_paths[distance]:
                new_paths_sorted.append(path)

        queue = new_paths_sorted + queue

##print hill_climbing(GRAPH3, 'S', 'G')            
                           
        
## Now we're going to implement beam search, a variation on BFS
## that caps the amount of memory used to store paths.  Remember,
## we maintain only k candidate paths of length n in our agenda at any time.
## The k top candidates are to be determined using the 
## graph get_heuristic function, with lower values being better values.
def beam_search(graph, start, goal, beam_width):
##    raise NotImplementedError
    # sort new paths by distance between their terminate node to the goal
    # choose the first beam_width paths and add them to the back the queue
    # pop the path in front of the queue
    queue = [[start]]
    extended = [start]
    
    while len(queue) > 0:
        cur_path = queue.pop(0)
        cur_node = cur_path[-1]
        new_paths = {}
        for node in graph.get_connected_nodes(cur_node):
            if node in extended:
                continue
            else:
                extended.append(node)
                if node == goal:
                    return cur_path + [node]
                else:
                    add_to_dict(new_paths, cur_path + [node], graph.get_heuristic(node, goal))
        new_paths_sorted = []
        for distance in sorted(new_paths):
            for path in new_paths[distance]:
                if len(new_paths_sorted) < beam_width:
                    new_paths_sorted.append(path)
                else:
                    break
        queue = queue + new_paths_sorted
    return None

##print beam_search(GRAPH3, 'S', 'G',3)            

## Now we're going to try optimal search.  The previous searches haven't
## used edge distances in the calculation.

## This function takes in a graph and a list of node names, and returns
## the sum of edge lengths along the path -- the total distance in the path.
def path_length(graph, node_names):
##    raise NotImplementedError
    pathLen = 0
    for i in range(len(node_names)-1):
        pathLen += graph.get_edge(node_names[i],node_names[i+1]).length
    return pathLen
    
def branch_and_bound(graph, start, goal):
##    raise NotImplementedError
    """ to find the optimal solution (the shortest path),
        so one goal is reached doesnot mean the process is over, must make sure this path the shorter than any partial ones in the queue
    # implement branch and bound with a lower-bound estimate
    # sort the entire queue by the sum of path length and a lower bound estimate of the cost remaining
    # with least cost path in front """
    extended = set(start)
    agenda = {0:[[start]]}
    while len(agenda) > 0:
        shortest_dist = sorted(agenda)[0]
        cur_paths = agenda.pop(shortest_dist)
        # [[],[],[]]
        cur_path = cur_paths.pop(0)
        if len(cur_paths) > 0:
            for path in cur_paths:
                add_to_dict(agenda, path, shortest_dist)
                
        cur_node = cur_path[-1]
        # a path-to-goal is first reomved from the agenda
        if cur_node == goal:
            return cur_path
        old_count = len(agenda)
        for node in graph.get_connected_nodes(cur_node):
            if node in extended and node != goal:
                continue
            else:
                extended.add(node)
                path = cur_path + [node]
                add_to_dict(agenda, path, path_length(graph, path) + graph.get_heuristic(node, goal))
                
    return None
                    
##print branch_and_bound(GRAPH3, 'S', 'G')        
    
def a_star(graph, start, goal):
##  raise NotImplementedError
    # based on branch and bound, if two or more paths reach a common node,
    # delete all those paths except the one that reached the common node with
    # the minimum cost
    agenda = {0:[[start]]}
    extended = set(start)
    
    while len(agenda) > 0:
        shortest_dist = sorted(agenda)[0]
        cur_paths = agenda.pop(shortest_dist)
        cur_path = cur_paths.pop(0)
        cur_node = cur_path[-1]
        if cur_node == goal:
            return cur_path
        
        if len(cur_paths) > 0:
            for path in cur_paths:
                add_to_dict(agenda, path, shortest_dist)
                
        for node in graph.get_connected_nodes(cur_node):
            if node not in extended or node == goal:
                extended.add(node)
                path = cur_path + [node]
                add_to_dict(agenda, path, path_length(graph, path) + graph.get_heuristic(node, goal))
            else:
                path = cur_path + [node]
                new_dist_traveled = path_length(graph, path) 
                path_to_del = []
                for distant, pathList in agenda.items():
                    for path in pathList:
                        if node in path:                            
                            old_dist_traveled = path_length(graph, path[:(path.index(node)+1)])
##                            print 'new_dist_traveled',new_dist_traveled,
##                            print 'old_dist_traveled',old_dist_traveled
                            # in most cases, 'old_dist_traveled' < 'new_dist_traveled'
                            if new_dist_traveled < old_dist_traveled:
                                add_to_dict(agenda, path, new_dist_traveled + graph.get_heuristic(node, goal))
                                # remove path from agenda                          
                                pathList.remove(path)
                                agenda[distant] = pathList
                                break

    return None

print a_star(NEWGRAPH2, 'S', 'G')                


                
                                
                                
                            
                
                
            
        


## It's useful to determine if a graph has a consistent and admissible
## heuristic.  You've seen graphs with heuristics that are
## admissible, but not consistent.  Have you seen any graphs that are
## consistent, but not admissible?

def is_admissible(graph, goal):
    raise NotImplementedError

def is_consistent(graph, goal):
    raise NotImplementedError

HOW_MANY_HOURS_THIS_PSET_TOOK = ''
WHAT_I_FOUND_INTERESTING = ''
WHAT_I_FOUND_BORING = ''
