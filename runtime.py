import os


def Runtime():
    if _Runtime._instance is None:
        _Runtime._instance = _Runtime()
    return _Runtime._instance


class _Runtime(object):
    _instance = None
    def __init__(self):
        super(_Runtime, self).__init__()
        self._variables = {}

    def getVariable(self, key):
        return os.environ.get(key, self._variables.get(key, None))

    def setVariable(self, key, value):
        self._variables[key] = value
