import unittest

from matchers import Is, Not, GreaterThan, LessThan, NotNone
from contracts import PreCallArgumentsContract, PostCallResultContract, \
    PreCallAllArgumentsContract, PreCallAttributeContract, PostCallAttributeContract


class ContractsTest(unittest.TestCase):

    def testArgumentNotNoneContract_OkCase(self):
        obj = TestThing()
        obj.setValueAndString_NoNone(1, "1")
        self.assertEquals("1", obj.getString())
        self.assertEquals(1, obj.getValue())

    def testArgumentNotNoneContract_ErrorCases(self):
        obj = TestThing()
        self.assertRaises(AssertionError, lambda : obj.setValueAndString_NoNone(None, ""))
        self.assertRaises(AssertionError, lambda : obj.setValueAndString_NoNone(None, None))
        self.assertRaises(AssertionError, lambda : obj.setValueAndString_NoNone(1, None))

    def testPositionalNotNoneContract_OkCase(self):
        obj = TestThing()
        obj.setValueAndString_PositionalValueNotNone(1, None)
        obj.setValueAndString_PositionalValueNotNone(1, "1")
        self.assertEquals("1", obj.getString())
        self.assertEquals(1, obj.getValue())

    def testPositionalNotNoneContract_ErrorCases(self):
        obj = TestThing()
        self.assertRaises(AssertionError, lambda : obj.setValueAndString_PositionalValueNotNone(None, ""))
        self.assertRaises(AssertionError, lambda : obj.setValueAndString_PositionalValueNotNone(None, None))

    def testKeywordNotNoneContract(self):
        obj = TestThing()
        obj.setValueAndString_KeywordValueNotNone(value=1, string="1")
        obj.setValueAndString_KeywordValueNotNone(value=1, string=None)
        self.assertRaises(AssertionError, lambda : obj.setValueAndString_KeywordValueNotNone(value=None, string=""))
        self.assertRaises(AssertionError, lambda : obj.setValueAndString_KeywordValueNotNone(value=None, string=None))

    def testReturnValueIsNotNone(self):
        obj = TestThing()
        value = 99
        obj.setValueNotNone(value)
        self.assertEquals(value, obj.getValue())
        obj.setValueNoCheck(None)
        self.assertRaises(AssertionError, obj.getValue)

    def testSetValueGreaterThan0(self):
        obj = TestThing()
        value = 99
        obj.setValueGreaterThan0(value)
        self.assertEquals(value, obj.getValue())
        self.assertRaises(AssertionError, lambda: obj.setValueGreaterThan0(-5))
        self.assertRaises(AssertionError, lambda: obj.setValueGreaterThan0(None))

    def testSetValueLessThan10(self):
        obj = TestThing()
        value = 4
        obj.setValue_NotNoneLessThan10(value)
        self.assertEquals(value, obj.getValue())
        self.assertRaises(AssertionError, lambda: obj.setValue_NotNoneLessThan10(111))
        self.assertRaises(AssertionError, lambda: obj.setValue_NotNoneLessThan10(None))

    def testDecValue(self):
        obj = TestThing()
        obj.setValueNotNone(2)
        self.assertEquals(1, obj.decValueGreaterThen0())
        self.assertEquals(0, obj.decValueGreaterThen0())
        self.assertRaises(AssertionError, obj.decValueGreaterThen0)

    def testIncValueWithCallableAttribute(self):
        obj = TestThing()
        obj.setValueNotNone(8)
        self.assertEquals(9, obj.incValueLessThan10())
        self.assertEquals(10, obj.incValueLessThan10())
        self.assertRaises(AssertionError, obj.incValueLessThan10)

    def testSetValueToNone(self):
        obj = TestThing()
        obj.setValueNotNone(8)
        self.assertRaises(AssertionError, obj.setValueNotNone, None)


class TestThing(object):
    def __init__(self):
        self._value = 0
        self._string = ""

    @PostCallResultContract(Not(Is(None)))
    def getValue(self):
        return self._value

    @PreCallAllArgumentsContract(Not(Is(None)))
    def setValueAndString_NoNone(self, value, string):
        self._value = value
        self._string = string

    def setString(self, string):
        self._string = string

    def getString(self):
        return self._string

    def getValuePlusXMinusY(self, x, y):
        return self._value + x - y

    @PostCallAttributeContract(NotNone(), "_value")
    def setValueNotNone(self, value):
        self.setValueNoCheck(value)

    def setValueNoCheck(self, value):
        self._value = value

    @PreCallAttributeContract(GreaterThan(0), "_value")
    def decValueGreaterThen0(self):
        self._value -= 1
        return self._value

    @PreCallAttributeContract(LessThan(10), "getValuePlusXMinusY", 5, y=5) # callable attribute
    def incValueLessThan10(self):
        self._value += 1
        return self._value

    @PreCallArgumentsContract(GreaterThan(0), argumentPositions = [1])
    def setValueGreaterThan0(self, value):
        self.setValueNoCheck(value)

    @PreCallArgumentsContract(Not(Is(None)), argumentPositions = [1])
    @PreCallArgumentsContract(LessThan(10), argumentPositions = [1])
    def setValue_NotNoneLessThan10(self, value):
        self.setValueNoCheck(value)

    @PreCallArgumentsContract(Not(Is(None)), argumentPositions = [1])
    def setValueAndString_PositionalValueNotNone(self, value, string):
        self.setValueNoCheck(value)
        self._string = string

    @PreCallArgumentsContract(Not(Is(None)), argumentKeywords = ["value"])
    def setValueAndString_KeywordValueNotNone(self, value, string):
        self.setValueNoCheck(value)
        self._string = string
