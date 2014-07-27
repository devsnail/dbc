"""
This module contain a set of decorators that are to be used when implementing
design by contract
"""

from itertools import chain
from contract_helpers import Contract, AttributeContract, ArgumentContract, getAttribute


class PreCallAllArgumentsContract(Contract):
    """
    A decorator class that applies a matcher to all arguments (including self) of
    the decorated method.
    """
    def decorate(self, function):
        def wrapper(*args, **kwargs):
            argumentIterator = chain(args, kwargs.itervalues())
            assert all(self._matcher.matches(arg) for arg in argumentIterator), \
                   "An argument does not fulfill the contract: '%s'" % str(self._matcher)
            return function(*args, **kwargs)
        return wrapper


class PreCallArgumentsContract(ArgumentContract):
    """
    A decorator class that applies a matcher to the specified arguments of the decorated method.
    The arguments are specified using either the positional index of the argument or the parameter name (keyword)
    """
    def decorate(self, function):
        def wrapper(*args, **kwargs):

            argsIter = (args[position] for position in self._argumentPositions)
            kwargsIter = (kwargs[keyword] for keyword in self._argumentKeywords)

            assert all(self._matcher.matches(arg) for arg in chain(argsIter, kwargsIter)), \
                   "An argument does not fulfill the contract: '%s'" % str(self._matcher)

            return function(*args, **kwargs)
        return wrapper


class PreCallAttributeContract(AttributeContract):
    # Disable matches for * and ** magic
    # pylint: disable=W0142
    """
    A decorator class that applies a matcher to an attribute of the object containing the method that is decorated.
    This attribute can be a member variable, but also a method. The matcher is applied before the actual call is performed
    If the attribute is a method that require some statically known arguments, these can be passed after the attribute argument
    """
    def decorate(self, function):
        def wrapper(obj, *args, **kwargs):
            assert self._matcher.matches(getAttribute(obj, self._attribute, *self._attributeArgs, **self._attribueKwArgs)), \
                   "The attribute '%s' does not fulfill the contract '%s' prior to the call. Actual value: '%s'." % \
                   (self._attribute, str(self._matcher), getAttribute(obj, self._attribute, *self._attributeArgs, **self._attribueKwArgs))
            return function(obj, *args, **kwargs)
        return wrapper


class PostCallAttributeContract(AttributeContract):
    # Disable matches for * and ** magic
    # pylint: disable=W0142
    """
    A decorator class that applies a matcher to an attribute of the object containing the method that is decorated.
    This attribute can be a member variable, but also a method. The matcher is applied after the decorated method is finished.
    If the attribute is a method that require some statically known arguments, these can be passed after the attribute argument
    """
    def decorate(self, function):
        def wrapper(obj, *args, **kwargs):
            result = function(obj, *args, **kwargs)
            assert self._matcher.matches(getAttribute(obj, self._attribute, *self._attributeArgs, **self._attribueKwArgs)), \
                   "The attribute '%s' does not fulfill the contract '%s' after the call. Actual value: '%s',"  % \
                   (self._attribute, str(self._matcher), getAttribute(obj, self._attribute, *self._attributeArgs, **self._attribueKwArgs))
            return result
        return wrapper

class PostCallResultContract(Contract):
    """
    A decorator class that applies a matcher to the result of a decorated method
    """
    def decorate(self, function):
        def wrapper(*args, **kwargs):
            result =  function(*args, **kwargs)
            assert self._matcher.matches(result), \
                   "The result does not fulfill the contract: '%s'" % str(self._matcher)
            return result
        return wrapper
