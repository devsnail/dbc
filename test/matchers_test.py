import unittest

from conditions import Is, Not, Equals, LessThan, GreaterThan, NotNone, \
                       LessThanOrEqualTo, GreaterThanOrEqualTo, Function


class ContractsTest(unittest.TestCase):
    def testIs(self):
        condition = Is("String")
        self.assertTrue(condition.matches("String"))
        self.assertFalse(condition.matches("AnotherString"))
        self.assertFalse(condition.matches(None))
        self.assertFalse(condition.matches("Strings".rstrip("s")))

    def testEquals(self):
        condition = Equals("String")
        self.assertTrue(condition.matches("String"))
        self.assertFalse(condition.matches("AnotherString"))
        self.assertFalse(condition.matches(None))
        self.assertTrue(condition.matches("Strings".rstrip("s")))

    def testLessThan(self):
        condition = LessThan(10)
        self.assertTrue(condition.matches(4))
        self.assertFalse(condition.matches(10))
        self.assertFalse(condition.matches(1000000000000000000000000000000000000000))
        self.assertTrue(condition.matches(9))
        self.assertTrue(condition.matches(-100000000000000000000000000000000000000000))

    def testLessThanOrEqualTo(self):
        condition = LessThanOrEqualTo(10)
        self.assertTrue(condition.matches(4))
        self.assertTrue(condition.matches(10))
        self.assertFalse(condition.matches(1000000000000000000000000000000000000000))
        self.assertTrue(condition.matches(9))
        self.assertTrue(condition.matches(-100000000000000000000000000000000000000000))

    def testGreaterThan(self):
        condition = GreaterThan(10)
        self.assertTrue(condition.matches(13))
        self.assertFalse(condition.matches(10))
        self.assertFalse(condition.matches(-1000000000000000000000000000000000000000))
        self.assertTrue(condition.matches(11))
        self.assertTrue(condition.matches(100000000000000000000000000000000000000000))

    def testGreaterThanOrEqualTo(self):
        condition = GreaterThanOrEqualTo(10)
        self.assertTrue(condition.matches(13))
        self.assertTrue(condition.matches(10))
        self.assertFalse(condition.matches(-1000000000000000000000000000000000000000))
        self.assertTrue(condition.matches(11))
        self.assertTrue(condition.matches(100000000000000000000000000000000000000000))

    def testAnd(self):
        condition = GreaterThan(10) + LessThan(20)
        self.assertTrue(condition.matches(11))
        self.assertFalse(condition.matches(10))
        self.assertTrue(condition.matches(19))
        self.assertFalse(condition.matches(20))

    def testOr(self):
        condition = GreaterThan(20) | LessThan(10)
        self.assertTrue(condition.matches(9))
        self.assertFalse(condition.matches(10))
        self.assertTrue(condition.matches(21))
        self.assertFalse(condition.matches(20))
        self.assertFalse(condition.matches(15))

    def testNot(self):
        condition = Not(Equals("String"))
        self.assertFalse(condition.matches("String"))
        self.assertTrue(condition.matches("AnotherString"))

    def testNotIsNone(self):
        condition = Not(Is(None))
        self.assertTrue(condition.matches("NotNone"))
        self.assertFalse(condition.matches(None))

    def testNotNone(self):
        condition = NotNone()
        self.assertTrue(condition.matches("NotNone"))
        self.assertFalse(condition.matches(None))

    def testFunctionWithLambda(self):
        condition = Function(lambda x: x > 10)
        self.assertTrue(condition.matches(13))
        self.assertFalse(condition.matches(10))
        self.assertFalse(condition.matches(-1000000000000000000000000000000000000000))
        self.assertTrue(condition.matches(11))
        self.assertTrue(condition.matches(100000000000000000000000000000000000000000))

    def testFunctionWithMethod(self):
        condition = Function(self._greaterThan10)
        self.assertTrue(condition.matches(13))
        self.assertFalse(condition.matches(10))
        self.assertFalse(condition.matches(-1000000000000000000000000000000000000000))
        self.assertTrue(condition.matches(11))
        self.assertTrue(condition.matches(100000000000000000000000000000000000000000))

    def _greaterThan10(self, value):
        return value > 10

    def testFunctionWithFunction(self):
        condition = Function(_greaterThan10)
        self.assertTrue(condition.matches(13))
        self.assertFalse(condition.matches(10))
        self.assertFalse(condition.matches(-1000000000000000000000000000000000000000))
        self.assertTrue(condition.matches(11))
        self.assertTrue(condition.matches(100000000000000000000000000000000000000000))


def _greaterThan10(value):
    return value > 10
