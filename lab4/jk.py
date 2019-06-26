
class Variable(object):
    
    def init(self, name, domain):
        self.name       = name
        self.domain     = domain[:]
        self.value      = None
        
    def get_name(self):
        return self.name
    
    def copy(self):
        return Variable(self.name,self.domain, self.value)

    def get_domain(self):
        return self.domain
    
    def set_value(self, value):
        self.value = value
        
    def is_asigned(self):
        if self.value != None:
            return True
        return False
    def get_value(self):
        if self.is_asigned():
            return self.value
        else:
            return None
    def reduce_domain(self, value):
        self.domain = self.domain.remove(value)

    def domain_size(self):
        return len(self.domain)

class BinaryConstraint(object):
    
    def init(self, var_i_name, var_j_name, check_func, description = None):

        self.var_i_name = var_i_name
        self.var_j_name = var_j_name
        self.check_func = check_func
        self.description = description

    def get_variable_i_name(self):

        return self.var_i_name

    def get_variable_j_name(self):

        return self.var_j_name

    def check(self, state, var_i_value = None, var_j_value = None):

        var_i = state.get_variable_by_name(self.var_i_name)
        if var_i_value == None and var_i != None:
            var_i_value = var_i.get_value()

        var_j = state.get_variable_by_name(self.var_j_name)
        if var_j_value == None and var_j != None:
            var_j_value = var_j.get_value()

        if var_i != None and var_j != None:
            return self.check_func(var_i_value, var_j_value,
                                   self.var_i_name,self.var_j_name )
        else:
            return Exception("Neither value_i or value_j is set")
    
  

class CSPState(object):

    def init(self, constraint_map, variable_map,
             variable_order,
             variable_index):
        # variable_map is a dict mapping variable name to object
        # constraint_map is a dict of variabel names to associated constraints 
        # variable_order is the order in which variables were assigned values,
        #                is variable names
        # variable_index , the position into variable_order in which we are making an
        #                assignment
        self.constraint_map = constraint_map
        self.variable_map= variable_map
        self.variable_order = variable_order
        self.variable_index = variable_index

    def copy(self):
        
        new_variable_map = {}
        
        for var_name, variable in  self.variable_map.items():
            new_variable_map[var_name] = variable.copy()

        new_state = CSPState(self.constraint_map,
                             variable_map,
                             self.variable_order,
                             self.variable_index)
        return new_state

    def get_variable_by_name(self, name):

        if name in self.variable_map:
            return self.variable_map[name]
        return None

    def get_constraints_by_name(self, variable_name):
        """
        List only constraints associated with variable_name
        (where variable_name is variable_i in the constraint)
        """
          
    def get_index(self):
        
        return self.variable_index

    def get_variable_by_index(self, index):

        var_name = self.variable_order[index]

        return get_variable_by_name[var_name]

    def set_variable_by_index(self, variable_index, variable_value):

        var = self.get_variable_by_index(variable_index)

        if var is not None:
            var.set_value(variable_value)
            self.variable_index = variable_index

    def get_variables(self):

        return self.variable_map
    def get_all_constraints(self):

        constraints = []
        for key,value in self.constraint_map.items():
            constraints +=  value
        return constraints

    def is_solution(self):
        # suppose constraint check has been done on this state
        for var in self.variable_map.values():
            if not var.is_asigned():
                return False
        return True
                    
        
def basic_constraint_checker(state, verbose=False):
    """
    Basic constraint checker used to check at every assignment
    whether the assignment passes all the constraints
    """
    constraints = state.get_all_constraints()
    for constraint in constraints:
        var_i_name = constraint.get_variable_i_name()
        var_j_name = constraint.get_variable_j_name()

        var_i = state.get_variable_by_name(var_i_name)
        var_j = state.get_variable_by_name(var_j_name)

        if not var_i.is_asigned() or not var_j.is_asigned():
            continue

        if not constraint.check(state):
            return False
    return True           

class CSP:

    """
    Top-level wrapper object that encapsulates all the
    variables and constraints of a CSP problem
    """
    def init(self, constraints, variables):

        self.constraint_map = {}
        # generate constraint map, a mapping of pair of variable names to
        # list of constraints associated to it
        for constraint in constraints:
            i = constraint.get_variable_i_name()
            j = constraint.get_variable_j_name()
            tup = (i, j)
            if tup not in self.constraint_map:
                self.constraint_map[tup] = [constraint]
            else:
                self.constraint_map[tup].append(constraint)
            
        # generate variable map, a mapping of variable names to variable object
        self.variable_map = {}
        self.variable_order = []
        for var in variables:
            self.variable_map[var.get_name()] = var
            self.variable_order.append(var.get_name())
            
    def initial_state(self):
        """
        Returns the starting state of the CSP with no variables assigned.
        """
        return CSPState(self.constraint_map, self.variable_map,
                self.variable_order,
                        -1)
    def solve(self):
        # a process assignint value to variable with satisfaction of  constraints

        state = self.initial_state()
        is_solved = False
        decision_tree = [state] # list of states with different assignment
        while len(decision_tree) != 0:
            
            state = decision_tree.pop(0)
            # contraint check on this state
            if not basic_constraint_checker(state):
                continue
            
            # is solution
            if state.is_solution():
                return state, search_root
                    
            next_variable_index = state.get_index() + 1
            next_variable = stat.get_variable_by_index(next_variable_index)

            children = []
            for value in next_variable.get_domain():
                new_state = state.copy()
                new_state.set_variable_by_index(next_variable_index)
                children.append(new_state)

            decision_tree = children + decision_tree


def simple_csp_problem():
    """
    Formulation of a simple CSP problem that attempts to find
    an assignment to 4 variables: A,B,C,D.  With the constraint that
    A < B < C < D.
    """
    variables = []
    domain = [1,2,3,4]

    variables.append(Variable("A",domain))
    variables.append(Variable("B",domain))
    variables.append(Variable("C",domain))
    variables.append(Variable("D",domain))

    constraints = []
    
    def less_than(val_a, val_b, name_a = None, name_b = None):
        return val_a < val_b

    
    constraints.append(BinaryConstraint("A", "B", less_than, "A<B" ))
    constraints.append(BinaryConstraint("B", "C", less_than, "B<C" ))
    constraints.append(BinaryConstraint("C", "D", less_than, "C<D" ))

    def not_equal(val_a, val_b, name_a = None, name_b = None):
        return val_a != val_b

    return CSP(variables, constraints)

def moose_csp_problem():
    

    # We start with the reduced domain.
    # So the constraint that McCain must sit in seat 1 is already
    # covered.


    domain = [1,2,3,4,5,6]
    variables = []
    
    variables.append(Variable("Mc", [1]))
    variables.append(Variable("O", domain))
    variables.append(Variable("B", domain))
    variables.append(Variable("P", domain))
    variables.append(Variable("M", domain))

    constraints = []
            
                
    def next_to(val_a, val_b, name_a = None, name_b = None):
        return val_a == val_b + 1 or val_a == val_b -1

    def not_next_to(val_a, val_b, name_a=None, name_b = None):
        return val_a != val_b + 1 and val_a != val_b -1

    # not two people can sit in one seat
    def not_equal(val_a, val_b, name_a = None, name_b = None):
        return val_a != val_b
    # no one can sit in two seats          

    constraints.append(BinaryConstraint("P", "Mc", next_to, "P next to Mc"))
    constraints.append(BinaryConstraint("B", "O", next_to, "B next to O"))
    constraints.append(BinaryConstraint("Mc", "O", not_next_to, "Mc not next to O"))
    constraints.append(BinaryConstraint("Mc", "B", not_next_to, "Mc not next to B"))
    constraints.append(BinaryConstraint("P", "B", not_next_to, "P not next to B"))
    constraints.append(BinaryConstraint("P", "O", not_next_to, "P not next to O"))
    constraints.append(BinaryConstraint("O", "Mc", not_next_to, "O not next to Mc"))
    constraints.append(BinaryConstraint("O", "P", not_next_to, "O not next to P"))
    constraints.append(BinaryConstraint("B", "Mc", not_next_to, "B not next to Mc"))
    constraints.append(BinaryConstraint("B", "P", not_next_to, "B not next to P"))
    constraints.append(BinaryConstraint("M", "P", not_next_to, "M not next to P"))

    constraints.append(BinaryConstraint("Mc", "O", not_equal, "Mc != O"))
    constraints.append(BinaryConstraint("O", "B", not_equal, "O != B"))
    constraints.append(BinaryConstraint("B", "P", not_equal, "B != P"))
    constraints.append(BinaryConstraint("P", "M", not_equal, "P != M"))

    return CSP(constraints,variables)
                

            

    
        
    
        
        
        
    
    
    
