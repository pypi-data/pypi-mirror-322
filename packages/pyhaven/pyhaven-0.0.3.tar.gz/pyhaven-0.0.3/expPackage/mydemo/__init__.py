r"""
This is mydemo regular package.
include __init__.py
"""

import sys

__version__ = '0.0.1'
__all__ = [
    'gcd',
    'p_argv',
]
__author__ = 'mingwe <mingwe.me@qq.com>'

def gcd(a,b):
    t = 0
    while b!=0:
        t = a%b
        a = b
        b = t
    return a
    
def p_argv():
    return sys.argv

def test():
    return "test"
