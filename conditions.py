class Matcher(object):
    def matches(self, value):
        raise NotImplementedError("Matcher::matches")

    def __str__(self):
        raise NotImplementedError("Matcher::__str__")


class Condition(Matcher):
    def __init__(self, variable):
        super(Condition, self).__init__()
        self._variable = variable

    def matches(self, value):
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


class And(Matcher):
    def __init__(self, conditionA, conditionB):
        super(And, self).__init__()
        self._conditionA = conditionA
        self._conditionB = conditionB

    def matches(self, value):
        return self._conditionA.matches(value) and self._conditionB.matches(value)

    def __str__(self):
        return "%s and %s" % (str(self._conditionA), str(self._conditionB))


class Or(Matcher):
    def __init__(self, conditionA, conditionB):
        super(Or, self).__init__()
        self._conditionA = conditionA
        self._conditionB = conditionB

    def matches(self, value):
        return self._conditionA.matches(value) or self._conditionB.matches(value)

    def __str__(self):
        return "%s or %s" % (str(self._conditionA), str(self._conditionB))


class Not(Matcher):
    def __init__(self, condition):
        super(Not, self).__init__()
        self._condition = condition

    def matches(self, value):
        return not self._condition.matches(value)

    def __str__(self):
        return "not %s" % str(self._condition)
