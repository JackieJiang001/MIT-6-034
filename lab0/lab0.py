# This is the file you'll use to submit most of Lab 0.

# Certain problems may ask you to modify other files to accomplish a certain
# task. There are also various other files that make the problem set work, and
# generally you will _not_ be expected to modify or even understand this code.
# Don't get bogged down with unnecessary work.


# Section 1: Problem set logistics ___________________________________________

# This is a multiple choice question. You answer by replacing
# the symbol 'fill-me-in' with a number, corresponding to your answer.

# You get to check multiple choice answers using the tester before you
# submit them! So there's no reason to worry about getting them wrong.
# Often, multiple-choice questions will be intended to make sure you have the
# right ideas going into the problem set. Run the tester right after you
# answer them, so that you can make sure you have the right answers.

# What version of Python do we *recommend* (not "require") for this course?
#   1. Python v2.3
#   2. Python v2.5 or Python v2.6
#   3. Python v3.0
# Fill in your answer in the next line of code ("1", "2", or "3"):

ANSWER_1 = '2'


# Section 2: Programming warmup _____________________________________________

# Problem 2.1: Warm-Up Stretch

def cube(x):
##    raise NotImplementedError
    return x**3

def factorial(x):
##    raise NotImplementedError
    if x < 0:
        raise Exception('factorial: input must be non-negative')
    if x == 0:
        return 1
    else:
        return x * factorial(x-1)
##print factorial(5)

def count_pattern(pattern, lst):
##    raise NotImplementedError
##    count = 0
##    for i in range(len(lst)):
##        if lst[i] == pattern[0]:
##            isPattern = True
##            for j in range(1,len(pattern)):
##                # make sure tuple index not out of range
##                if i + j < len(lst):                 
##                    if lst[i+j] != pattern[j]:
##                        isPattern = False
##                        break
##                else:
##                    isPattern = False
##                    
##            if isPattern:
##                count += 1
##    return count
    count = 0
    pLen = len(pattern)
    for i in range(len(lst)):
        if lst[i:(i+pLen)] == pattern:
            count += 1
    return count

            
pattern = [1, [2,3]]
lst = [1, [2,3], 2, 3, 1, [2,3,4],1]
##print count_pattern(pattern, lst)
    

# Problem 2.2: Expression depth

def depth(expr):
##    raise NotImplementedError
    dep = 0
    if isinstance(expr,(list,tuple)):
        dep += 1
    else:
        return dep
        
    max_dep = 0
    for sub_expr in expr:
        sub_dep = depth(sub_expr)
        if max_dep ==0 or max_dep < sub_dep:
            max_dep = sub_dep
    return dep + max_dep

##print depth('x')
##print depth(('expt', 'x', 2))
##print depth(('+', ('expt', 'x', 2), ('expt', 'y', 2)))
##print depth(('/', ('expt', 'x', 5), ('expt', ('-', ('expt', 'x', 2), 1), ('/', 5, 2))))
# Problem 2.3: Tree indexing

def tree_ref(tree, index):
##    raise NotImplementedError
    index = list(index)
    sub_tree = tree
    while len(index) > 0:
        sub_index = index.pop(0)
        sub_tree = sub_tree[sub_index]
    return sub_tree


tree = (((1, 2), 3), (4, (5, 6)), 7, (8, 9, 10))
index = (0,)
print tree_ref(tree, index)


# Section 3: Symbolic algebra

# Your solution to this problem doesn't go in this file.
# Instead, you need to modify 'algebra.py' to complete the distributer.

from algebra import Sum, Product, simplify_if_possible
from algebra_utils import distribution, encode_sumprod, decode_sumprod

# Section 4: Survey _________________________________________________________

# Please answer these questions inside the double quotes.

# When did you take 6.01?
WHEN_DID_YOU_TAKE_601 = ""

# How many hours did you spend per 6.01 lab?
HOURS_PER_601_LAB = ""

# How well did you learn 6.01?
HOW_WELL_I_LEARNED_601 = ""

# How many hours did this lab take?
HOURS = ""
