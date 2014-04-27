"""
This module contain a set of decorators that are to be used when implementing
design by contract
"""

from itertools import chain
from runtime import Runtime


def PreCallAllArgumentsContract(condition):
    """
    A decorator that applies a condition to all arguments (including self) of
    the decorated method.

    @note: This decorator has no effect if
    Runtime.getInstance().getVariable("UseContracts") is False
    @param condition: A L{Expression} object to test on all arguments
    @type condition: L{Expression}

    @return: The decorated function
    @rtype: C{function}
    """
    def decorator(function):
        if usingContracts():
            def inner(*args, **kwargs):
                argumentIterator = chain(args, kwargs.itervalues())
                assert all(condition.check(arg) for arg in argumentIterator), \
                       "An argument does not fulfill the contract: '%s'" % str(condition)
                return function(*args, **kwargs)
            return inner
        return function
    return decorator


def PreCallArgumentsContract(condition, argumentPositions = (), argumentKeywords = ()):
    """
    A decorator that applies a condition to the specified arguments of the decorated method.
    The arguments are specified using either the positional index of the argument or the parameter name (keyword)

    @note: This decorator has no effect if Runtime.getInstance().getVariable("UseContracts") is False

    @param condition: A L{Expression} object to test on some argument(s).
    @type condition: L{Expression}
    @param argumentPositions: The indices (positions) of the arguments, in the argument list, to test.
    @type argumentPositions: iterator<int>
    @param argumentKeywords: The names of the arguments, in the named argument list, to test.
    @type argumentKeywords: iterator<string>

    @return: The decorated function
    @rtype: C{function}
    """
    def decorator(function):
        if usingContracts():
            def inner(*args, **kwargs):

                argsIter = (args[position] for position in argumentPositions)
                kwargsIter = (kwargs[keyword] for keyword in argumentKeywords)

                assert all(condition.check(arg) for arg in chain(argsIter, kwargsIter)), \
                       "An argument does not fulfill the contract: '%s'" % str(condition)

                return function(*args, **kwargs)
            return inner
        return function
    return decorator


def _getAttribute(obj, attributeName, *args, **kwargs):
    attribute = getattr(obj, attributeName)
    return attribute(*args, **kwargs) if callable(attribute) else attribute


def PreCallFieldContract(condition, attribute, *fieldArgs, **fieldKWArgs):
    # Disable check for * and ** magic
    # pylint: disable=W0142
    """
    A decorator that applies a condition to an attribute of the object containing the method that is decorated.
    This attribute can be a member variable, but also a method. The condition is applied before the actual call is performed
    If the attribute is a method that require some statically known arguments, these can be passed after the attribute argument

    @note: This decorator has no effect if Runtime.getInstance().getVariable("UseContracts") is False
    @param condition: A L{Expression} object to test on all arguments
    @type condition: L{Expression}
    @param attribute: The name of the attribute. Can be either a field or a method.
    @type attribute: C{string}

    @return: The decorated function
    @rtype: C{function}
    """
    def decorator(function):
        if usingContracts():
            def inner(self, *args, **kwargs):
                assert condition.check(_getAttribute(self, attribute, *fieldArgs, **fieldKWArgs)), \
                       "The field '%s' does not fulfill the contract '%s' prior to the call. Actual value: '%s'." % (attribute, str(condition), _getAttribute(self, attribute, *fieldArgs, **fieldKWArgs))
                return function(self, *args, **kwargs)
            return inner
        return function
    return decorator


def PostCallFieldContract(condition, field, *fieldArgs, **fieldKWArgs):
    # Disable check for * and ** magic
    # pylint: disable=W0142
    """
    A decorator that applies a condition to an attribute of the object containing the method that is decorated.
    This attribute can be a member variable, but also a method. The condition is applied after the decorated method is finished.
    If the attribute is a method that require some statically known arguments, these can be passed after the attribute argument

    @note: This decorator has no effect if Runtime.getInstance().getVariable("UseContracts") is False
    @param condition: A L{Expression} object to test on all arguments
    @type condition: L{Expression}
    @param attribute: The name of the attribute. Can be either a field or a method.
    @type attribute: C{string}

    @return: The decorated function
    @rtype: C{function}
    """
    def decorator(function):
        if usingContracts():
            def inner(self, *args, **kwargs):
                result = function(self, *args, **kwargs)
                assert condition.check(_getAttribute(self, field, *fieldArgs, **fieldKWArgs)), \
                       "The field '%s' does not fulfill the contract '%s' after the call. Actual value: '%s',"  % (field, str(condition), _getAttribute(self, field, *fieldArgs, **fieldKWArgs))
                return result
            return inner
        return function
    return decorator

def PostCallResultContract(condition):
    """
    A decorator that applies a condition to the result of a decorated method

    @note: This decorator has no effect if Runtime.getInstance().getVariable("UseContracts") is False
    @param condition: A L{Expression} object to test on all arguments
    @type condition: L{Expression}

    @return: The decorated function
    @rtype: C{function}
    """
    def decorator(function):
        if usingContracts():
            def inner(*args, **kwargs):
                result =  function(*args, **kwargs)
                assert condition.check(result), \
                       "The result does not fulfill the contract: '%s'" % str(condition)
                return result
            return inner
        return function
    return decorator


def usingContracts():
    #Used to completely remove the decorator from the call stack to simplify debugging
    #Implement this pattern on all annoying decorators(such as tracer and measure)
    return Runtime().getVariable("DisableContracts") is None
