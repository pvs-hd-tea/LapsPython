"""Dummy primitives for tests."""

def _addition(x): return lambda y: x + y

def _subtraction(x):
    return lambda y: x - y

def _division(x):
    return lambda y: x / y

def _identity(x): return x

def _not(x):
    return not x

def not_a_primitive(x):
    return

