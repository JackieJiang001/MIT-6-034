from production import AND, OR, NOT, PASS, FAIL, IF, THEN, \
     match, populate, simplify, variables
from zookeeper import ZOOKEEPER_RULES

# This function, which you need to write, takes in a hypothesis
# that can be determined using a set of rules, and outputs a goal
# tree of which statements it would need to test to prove that
# hypothesis. Refer to the problem set (section 2) for more
# detailed specifications and examples.

# Note that this function is supposed to be a general
# backchainer.  You should not hard-code anything that is
# specific to a particular rule set.  The backchainer will be
# tested on things other than ZOOKEEPER_RULES.


def backchain_to_goal_tree(rules, hypothesis):
##    raise NotImplementedError
    goal_tree = OR(hypothesis)
    for rule in rules:
        consequce = rule.consequent()[0]
        bindings = match(consequce, hypothesis)
        sub_tree = []
        if bindings is not None and len(bindings) > 0:            
            antecedent = rule.antecedent()
            
            for elem in antecedent:
                new_hypothesis = populate(elem, bindings)
                pop_elem = backchain_to_goal_tree(rules, new_hypothesis)
                sub_tree.append(simplify(pop_elem))
                
            if isinstance(antecedent, AND):
                sub_tree = AND(sub_tree)
            elif isinstance(antecedent, OR):
                sub_tree = OR(sub_tree)
        if len(sub_tree)>0:
            goal_tree.append(sub_tree)            
    return goal_tree
                
            

        

# Here's an example of running the backward chainer - uncomment
# it to see it work:
print backchain_to_goal_tree(ZOOKEEPER_RULES, 'opus is a penguin')
