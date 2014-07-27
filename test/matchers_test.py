import unittest

from matchers import Is, Not, Equals, LessThan, GreaterThan, NotNone, \
                       LessThanOrEqualTo, GreaterThanOrEqualTo, Function


class MatchersTest(unittest.TestCase):
    def testIs(self):
        matcher = Is("String")
        self.assertTrue(matcher.matches("String"))
        self.assertFalse(matcher.matches("AnotherString"))
        self.assertFalse(matcher.matches(None))
        self.assertFalse(matcher.matches("Strings".rstrip("s")))

    def testEquals(self):
        matcher = Equals("String")
        self.assertTrue(matcher.matches("String"))
        self.assertFalse(matcher.matches("AnotherString"))
        self.assertFalse(matcher.matches(None))
        self.assertTrue(matcher.matches("Strings".rstrip("s")))

    def testLessThan(self):
        matcher = LessThan(10)
        self.assertTrue(matcher.matches(4))
        self.assertFalse(matcher.matches(10))
        self.assertFalse(matcher.matches(1000000000000000000000000000000000000000))
        self.assertTrue(matcher.matches(9))
        self.assertTrue(matcher.matches(-100000000000000000000000000000000000000000))

    def testLessThanOrEqualTo(self):
        matcher = LessThanOrEqualTo(10)
        self.assertTrue(matcher.matches(4))
        self.assertTrue(matcher.matches(10))
        self.assertFalse(matcher.matches(1000000000000000000000000000000000000000))
        self.assertTrue(matcher.matches(9))
        self.assertTrue(matcher.matches(-100000000000000000000000000000000000000000))

    def testGreaterThan(self):
        matcher = GreaterThan(10)
        self.assertTrue(matcher.matches(13))
        self.assertFalse(matcher.matches(10))
        self.assertFalse(matcher.matches(-1000000000000000000000000000000000000000))
        self.assertTrue(matcher.matches(11))
        self.assertTrue(matcher.matches(100000000000000000000000000000000000000000))

    def testGreaterThanOrEqualTo(self):
        matcher = GreaterThanOrEqualTo(10)
        self.assertTrue(matcher.matches(13))
        self.assertTrue(matcher.matches(10))
        self.assertFalse(matcher.matches(-1000000000000000000000000000000000000000))
        self.assertTrue(matcher.matches(11))
        self.assertTrue(matcher.matches(100000000000000000000000000000000000000000))

    def testAnd(self):
        matcher = GreaterThan(10) + LessThan(20)
        self.assertTrue(matcher.matches(11))
        self.assertFalse(matcher.matches(10))
        self.assertTrue(matcher.matches(19))
        self.assertFalse(matcher.matches(20))

    def testOr(self):
        matcher = GreaterThan(20) | LessThan(10)
        self.assertTrue(matcher.matches(9))
        self.assertFalse(matcher.matches(10))
        self.assertTrue(matcher.matches(21))
        self.assertFalse(matcher.matches(20))
        self.assertFalse(matcher.matches(15))

    def testNot(self):
        matcher = Not(Equals("String"))
        self.assertFalse(matcher.matches("String"))
        self.assertTrue(matcher.matches("AnotherString"))

    def testNotIsNone(self):
        matcher = Not(Is(None))
        self.assertTrue(matcher.matches("NotNone"))
        self.assertFalse(matcher.matches(None))

    def testNotNone(self):
        matcher = NotNone()
        self.assertTrue(matcher.matches("NotNone"))
        self.assertFalse(matcher.matches(None))

    def testFunctionWithLambda(self):
        matcher = Function(lambda x: x > 10)
        self.assertTrue(matcher.matches(13))
        self.assertFalse(matcher.matches(10))
        self.assertFalse(matcher.matches(-1000000000000000000000000000000000000000))
        self.assertTrue(matcher.matches(11))
        self.assertTrue(matcher.matches(100000000000000000000000000000000000000000))

    def testFunctionWithMethod(self):
        matcher = Function(self._greaterThan10)
        self.assertTrue(matcher.matches(13))
        self.assertFalse(matcher.matches(10))
        self.assertFalse(matcher.matches(-1000000000000000000000000000000000000000))
        self.assertTrue(matcher.matches(11))
        self.assertTrue(matcher.matches(100000000000000000000000000000000000000000))

    def _greaterThan10(self, value):
        return value > 10

    def testFunctionWithFunction(self):
        matcher = Function(_greaterThan10)
        self.assertTrue(matcher.matches(13))
        self.assertFalse(matcher.matches(10))
        self.assertFalse(matcher.matches(-1000000000000000000000000000000000000000))
        self.assertTrue(matcher.matches(11))
        self.assertTrue(matcher.matches(100000000000000000000000000000000000000000))


def _greaterThan10(value):
    return value > 10
