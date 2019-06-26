from classify import *
import math

##
## CSP portion of lab 4.
##
from csp import BinaryConstraint, CSP, CSPState, Variable,\
    basic_constraint_checker, solve_csp_problem

# Implement basic forward checking on the CSPState see csp.py

def forward_checking(state, verbose=False):
    # Before running Forward checking we must ensure
    # that constraints are okay for this state.

    basic = basic_constraint_checker(state, verbose)

    if not basic:
        return False

    # so far, all the assigned values satisfied the constraints
    # in this state, some variable has been assigned, what we need to
    # to do is check domain of the remaining unassigned variables
    print "Before Check: state = " , state.vd_table()
    new_state = state.copy()
    current_var_name = new_state.get_current_variable_name() 
    constraints = new_state.get_constraints_by_name(current_var_name)
    print "current variable :", current_var_name
    for constraint in constraints:
        print constraint
        var_j_name =constraint.get_variable_j_name()
        var_j = new_state.get_variable_by_name(var_j_name)
        domain = var_j.get_domain()
        for value in domain:
            var_j.set_value(value)
            if constraint.check(new_state):
                continue
            elif var_j.domain_size()> 1:
                var_j.reduce_domain(value)
            else:
                return False
    print "After Check: state = " , state.vd_table()
    return True
              
    # Add your forward checking logic here.
    

# Now Implement forward checking + (constraint) propagation through
# singleton domains.
def forward_checking_prop_singleton(state, verbose=False):
    # Run forward checking first.
    fc_checker = forward_checking(state, verbose)
    if not fc_checker:
        return False
    
    # Add your propagate singleton logic here.
    new_state = state.copy()
    varibles = new_state.get_all_variables()
    # list of variables whose domain size is one
    singletons = []  
    
    for variable in varibles:
        if variable.domain_size() == 1:
           singletons.append(variable)

    visited_singletons = []

    for var in singletons:
        
        if var not in visited_singletons:
            visited_singletons.append(var)
   
            var.set_value(var.get_domain()[0])
            constaints = new_state.get_constraints_by_name(var.get_name())
            for constraint in constaints:
                var_j_name = constraint.get_variable_j_name()
                var_j = new_state.get_variable_by_name(var_j_name)
                domain = var_j.get_domain()
                for value in domain:
                    var_j.set_value(value)
                    if constraint.check(new_state):
                        continue
                    elif var_j.domain_size() > 1:
                        var_j.reduce_domain(value)
                    else:
                        return False
                if var_j.get_domain() == 1:
                    singletons.append(var_j)
    return True
                 
        

## The code here are for the tester
## Do not change.
from moose_csp import moose_csp_problem
from map_coloring_csp import map_coloring_csp_problem

def csp_solver_tree(problem, checker):
    problem_func = globals()[problem]
    checker_func = globals()[checker]
    answer, search_tree = problem_func().solve(checker_func)
    return search_tree.tree_to_string(search_tree)

##
## CODE for the learning portion of lab 4.
##

### Data sets for the lab
## You will be classifying data from these sets.
senate_people = read_congress_data('S110.ord')
senate_votes = read_vote_data('S110desc.csv')

house_people = read_congress_data('H110.ord')
house_votes = read_vote_data('H110desc.csv')

last_senate_people = read_congress_data('S109.ord')
last_senate_votes = read_vote_data('S109desc.csv')


### Part 1: Nearest Neighbors
## An example of evaluating a nearest-neighbors classifier.
senate_group1, senate_group2 = crosscheck_groups(senate_people)
##evaluate(nearest_neighbors(hamming_distance, 1), senate_group1, senate_group2, verbose=1)

## Write the euclidean_distance function.
## This function should take two lists of integers and
## find the Euclidean distance between them.
## See 'hamming_distance()' in classify.py for an example that
## computes Hamming distances.

def euclidean_distance(list1, list2):
    # this is not the right solution!
##    return hamming_distance(list1, list2)

    assert isinstance(list1, list)
    assert isinstance(list2, list)
    assert len(list1) == len(list2)
    
    dist = 0
    for i in range(len(list1)):
        dist += (list1[i] - list2[i])**2
    return math.sqrt(dist)
        
#Once you have implemented euclidean_distance, you can check the results:
##evaluate(nearest_neighbors(euclidean_distance, 1), senate_group1, senate_group2,verbose=1)

## By changing the parameters you used, you can get a classifier factory that
## deals better with independents. Make a classifier that makes at most 3
## errors on the Senate.

my_classifier = nearest_neighbors(hamming_distance, 1)
#evaluate(my_classifier, senate_group1, senate_group2, verbose=1)

### Part 2: ID Trees
##print CongressIDTree(senate_people, senate_votes, homogeneous_disorder)

## Now write an information_disorder function to replace homogeneous_disorder,
## which should lead to simpler trees.

def information_disorder(yes, no):
    # -N/T*log(N/T,2) - P/T*log(P/T,2) 
    yes_disorder = disorder_value(yes)
    no_disorder = disorder_value(no)
    total_len = len(yes) + len(no)    
    disorder = (len(yes)/float(total_len)) * yes_disorder + (len(no)/float(total_len)) * no_disorder
    
    return disorder

def disorder_value(legislators):
    # legislator is list of parties
    # let Republican to be R
    # let Democrat to be D
    # let Independent to be I
    R_sum = 0
    D_sum = 0
    I_sum = 0
    T = len(legislators)
    score = 0
    for leg in legislators:
        if leg == 'Republican':
            R_sum += 1
        elif leg == 'Democrat':
            D_sum += 1
        else:
            I_sum = 1
    score = N_log(R_sum/float(T)) +  N_log(D_sum/float(T)) + N_log(I_sum/float(T))
    return score
    
def N_log(num):
    if num == 0:
        return 0
    return -1 * math.log(num, 2) * num
  

##print information_disorder(['Democrat','Democrat','Democrat'], ['Republican','Republican','Republican'])
##print information_disorder(['Democrat','Republican'], ['Republican','Democrat'])

##print CongressIDTree(senate_people, senate_votes, information_disorder)
print evaluate(idtree_maker(senate_votes, homogeneous_disorder), senate_group1, senate_group2)

## Now try it on the House of Representatives. However, do it over a data set
## that only includes the most recent n votes, to show that it is possible to
## classify politicians without ludicrous amounts of information.

def limited_house_classifier(house_people, house_votes, n, verbose = False):
    house_limited, house_limited_votes = limit_votes(house_people,
    house_votes, n)
    house_limited_group1, house_limited_group2 = crosscheck_groups(house_limited)

    if verbose:
        print "ID tree for first group:"
        print CongressIDTree(house_limited_group1, house_limited_votes,
                             information_disorder)
        print
        print "ID tree for second group:"
        print CongressIDTree(house_limited_group2, house_limited_votes,
                             information_disorder)
        print
        
    return evaluate(idtree_maker(house_limited_votes, information_disorder),
                    house_limited_group1, house_limited_group2)

                                   
## Find a value of n that classifies at least 430 representatives correctly.
## Hint: It's not 10.
N_1 = 1000
rep_classified = limited_house_classifier(house_people, house_votes, N_1)
print rep_classified
## Find a value of n that classifies at least 90 senators correctly.
N_2 = 2000
senator_classified = limited_house_classifier(senate_people, senate_votes, N_2)
print senator_classified
## Now, find a value of n that classifies at least 95 of last year's senators correctly.
N_3 = 100
old_senator_classified = limited_house_classifier(last_senate_people, last_senate_votes, N_3)
print old_senator_classified

## The standard survey questions.
HOW_MANY_HOURS_THIS_PSET_TOOK = ""
WHAT_I_FOUND_INTERESTING = ""
WHAT_I_FOUND_BORING = ""


## This function is used by the tester, please don't modify it!
def eval_test(eval_fn, group1, group2, verbose = 0):
    """ Find eval_fn in globals(), then execute evaluate() on it """
    # Only allow known-safe eval_fn's
    if eval_fn in [ 'my_classifier' ]:
        return evaluate(globals()[eval_fn], group1, group2, verbose)
    else:
        raise Exception, "Error: Tester tried to use an invalid evaluation function: '%s'" % eval_fn

    
