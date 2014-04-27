class Expression(object):
    def check(self, value):
        raise NotImplementedError("Expression::check")

    def __str__(self):
        raise NotImplementedError("Expression::__str__")


class Condition(Expression):
    def __init__(self, variable):
        super(Condition, self).__init__()
        self._variable = variable
    
    def check(self, value):
        return self._function(value)
    
    def _function(self, value):
        raise NotImplementedError("Condition::_function")
    
    def __add__(self, condition):
        return And(self, condition)
                   
    def __or__(self, condition):
        return Or(self, condition)


class NotNone(Condition):
    def __init__(self):
        super(NotNone, self).__init__(None)
        
    def _function(self, value):
        return not value is self._variable 
    
    def __str__(self):
        return "not is None"


class Is(Condition):
    def _function(self, value):
        return self._variable is value 
    
    def __str__(self):
        return "is %s" % str(self._variable)


class Equals(Condition):
    def _function(self, value):
        return self._variable == value
    
    def __str__(self):
        return "equals %s" % str(self._variable)


class LessThan(Condition):
    def _function(self, value):
        return self._variable > value
    
    def __str__(self):
        return "less than %s" % str(self._variable)


class LessThanOrEqualTo(Condition):
    def _function(self, value):
        return self._variable >= value
    
    def __str__(self):
        return "less than or equal to %s" % str(self._variable)


class GreaterThan(Condition):
    def _function(self, value):
        return self._variable < value
    
    def __str__(self):
        return "greater than %s" % str(self._variable)


class GreaterThanOrEqualTo(Condition):
    def _function(self, value):
        return self._variable <= value
    
    def __str__(self):
        return "greater than or equal to %s" % str(self._variable)


class Function(Condition):
    def _function(self, value):
        return self._variable(value)
    
    def __str__(self):
        return "%s of" % self._variable
    

class And(Expression):
    def __init__(self, conditionA, conditionB):
        super(And, self).__init__()
        self._conditionA = conditionA
        self._conditionB = conditionB
        
    def check(self, value):
        return self._conditionA.check(value) and self._conditionB.check(value)
    
    def __str__(self):
        return "%s and %s" % (str(self._conditionA), str(self._conditionB))


class Or(Expression):
    def __init__(self, conditionA, conditionB):
        super(Or, self).__init__()
        self._conditionA = conditionA
        self._conditionB = conditionB
        
    def check(self, value):
        return self._conditionA.check(value) or self._conditionB.check(value)
    
    def __str__(self):
        return "%s or %s" % (str(self._conditionA), str(self._conditionB))


class Not(Expression):
    def __init__(self, condition):
        super(Not, self).__init__()
        self._condition = condition
        
    def check(self, value):
        return not self._condition.check(value)
    
    def __str__(self):
        return "not %s" % str(self._condition)
