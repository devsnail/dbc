import unittest

from conditions import Is, Not, Equals, LessThan, GreaterThan, NotNone, \
                       LessThanOrEqualTo, GreaterThanOrEqualTo, Function


class ContractsTest(unittest.TestCase):
    def testIs(self):
        condition = Is("String")
        self.assertTrue(condition.check("String"))
        self.assertFalse(condition.check("AnotherString"))
        self.assertFalse(condition.check(None))
        self.assertFalse(condition.check("Strings".rstrip("s")))

    def testEquals(self):
        condition = Equals("String")
        self.assertTrue(condition.check("String"))
        self.assertFalse(condition.check("AnotherString"))
        self.assertFalse(condition.check(None))
        self.assertTrue(condition.check("Strings".rstrip("s")))

    def testLessThan(self):
        condition = LessThan(10)
        self.assertTrue(condition.check(4))
        self.assertFalse(condition.check(10))
        self.assertFalse(condition.check(1000000000000000000000000000000000000000))
        self.assertTrue(condition.check(9))
        self.assertTrue(condition.check(-100000000000000000000000000000000000000000))

    def testLessThanOrEqualTo(self):
        condition = LessThanOrEqualTo(10)
        self.assertTrue(condition.check(4))
        self.assertTrue(condition.check(10))
        self.assertFalse(condition.check(1000000000000000000000000000000000000000))
        self.assertTrue(condition.check(9))
        self.assertTrue(condition.check(-100000000000000000000000000000000000000000))

    def testGreaterThan(self):
        condition = GreaterThan(10)
        self.assertTrue(condition.check(13))
        self.assertFalse(condition.check(10))
        self.assertFalse(condition.check(-1000000000000000000000000000000000000000))
        self.assertTrue(condition.check(11))
        self.assertTrue(condition.check(100000000000000000000000000000000000000000))

    def testGreaterThanOrEqualTo(self):
        condition = GreaterThanOrEqualTo(10)
        self.assertTrue(condition.check(13))
        self.assertTrue(condition.check(10))
        self.assertFalse(condition.check(-1000000000000000000000000000000000000000))
        self.assertTrue(condition.check(11))
        self.assertTrue(condition.check(100000000000000000000000000000000000000000))

    def testAnd(self):
        condition = GreaterThan(10) + LessThan(20)
        self.assertTrue(condition.check(11))
        self.assertFalse(condition.check(10))
        self.assertTrue(condition.check(19))
        self.assertFalse(condition.check(20))

    def testOr(self):
        condition = GreaterThan(20) | LessThan(10)
        self.assertTrue(condition.check(9))
        self.assertFalse(condition.check(10))
        self.assertTrue(condition.check(21))
        self.assertFalse(condition.check(20))
        self.assertFalse(condition.check(15))

    def testNot(self):
        condition = Not(Equals("String"))
        self.assertFalse(condition.check("String"))
        self.assertTrue(condition.check("AnotherString"))

    def testNotIsNone(self):
        condition = Not(Is(None))
        self.assertTrue(condition.check("NotNone"))
        self.assertFalse(condition.check(None))

    def testNotNone(self):
        condition = NotNone()
        self.assertTrue(condition.check("NotNone"))
        self.assertFalse(condition.check(None))

    def testFunctionWithLambda(self):
        condition = Function(lambda x: x > 10)
        self.assertTrue(condition.check(13))
        self.assertFalse(condition.check(10))
        self.assertFalse(condition.check(-1000000000000000000000000000000000000000))
        self.assertTrue(condition.check(11))
        self.assertTrue(condition.check(100000000000000000000000000000000000000000))

    def testFunctionWithMethod(self):
        condition = Function(self._greaterThan10)
        self.assertTrue(condition.check(13))
        self.assertFalse(condition.check(10))
        self.assertFalse(condition.check(-1000000000000000000000000000000000000000))
        self.assertTrue(condition.check(11))
        self.assertTrue(condition.check(100000000000000000000000000000000000000000))

    def _greaterThan10(self, value):
        return value > 10

    def testFunctionWithFunction(self):
        condition = Function(_greaterThan10)
        self.assertTrue(condition.check(13))
        self.assertFalse(condition.check(10))
        self.assertFalse(condition.check(-1000000000000000000000000000000000000000))
        self.assertTrue(condition.check(11))
        self.assertTrue(condition.check(100000000000000000000000000000000000000000))


def _greaterThan10(value):
    return value > 10
