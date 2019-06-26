
class Expression:
    pass

class Sum(list, Expression):

    def __expr__(self):

        return "Sum(%s)" % list.__repr__(self)

    def simplify(self):

        terms = self.flatten()
        
        


    def flatten(self):
        res = []
        for item in self:
            if isinstance(item, Sum):
                res += list(item)
            else:
                res.append(item)

        return Sum(res)
        
        
