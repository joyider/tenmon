# -*- coding: utf-8 -*-
# Filename: three2two by: andrek
# Timesamp:2018-10-27 :: 11:11 using PyCharm

import operator
import sys
import unicodedata
import types
import platform

PY_CYTHON = platform.python_implementation() == 'CPython'
PY_PYPY = platform.python_implementation() == 'PyPy'
PY_JYTHON = platform.python_implementation() == 'Jython'
PY_IRON = platform.python_implementation() == 'IronPython'
PY3 = sys.version_info[0] == 3

try:
    from statistics import mean
except ImportError:
    # Statistics is only available for Python 3.4 or higher
    def mean(numbers):
        return float(sum(numbers)) / max(len(numbers), 1)

if PY3:
    import queue
    from configparser import ConfigParser, NoOptionError, NoSectionError
    from urllib.request import urlopen
    from urllib.error import HTTPError, URLError
    from urllib.parse import urlparse
    from urllib.parse import urlencode

    from .httplib2.python3 import httplib2

    input = input
    range = range
    map = map

    text_type = str
    binary_type = bytes
    bool_type = bool

    viewkeys = operator.methodcaller('keys')
    viewvalues = operator.methodcaller('values')
    viewitems = operator.methodcaller('items')

    def to_ascii(s):
        """Convert the bytes string to a ASCII string
        Usefull to remove accent (diacritics)"""
        return str(s, 'utf-8')

    def listitems(d):
        return list(d.items())

    def listkeys(d):
        return list(d.keys())

    def listvalues(d):
        return list(d.values())

    def iteritems(d):
        return iter(d.items())

    def iterkeys(d):
        return iter(d.keys())

    def itervalues(d):
        return iter(d.values())

    def u(s):
        if isinstance(s, text_type):
            return s
        return s.decode('utf-8', 'replace')

    def b(s):
        if isinstance(s, binary_type):
            return s
        return s.encode('latin-1')

    def nativestr(s):
        if isinstance(s, text_type):
            return s
        return s.decode('utf-8', 'replace')
else:
    import Queue as queue
    from itertools import imap as map
    from ConfigParser import SafeConfigParser as ConfigParser, NoOptionError, NoSectionError
    from urllib2 import urlopen, HTTPError, URLError
    from urlparse import urlparse
    from urllib import urlencode

    from .httplib2.python2 import httplib2

    input = raw_input
    range = xrange
    ConfigParser.read_file = ConfigParser.readfp

    text_type = unicode
    binary_type = str
    bool_type = types.BooleanType

    viewkeys = operator.methodcaller('viewkeys')
    viewvalues = operator.methodcaller('viewvalues')
    viewitems = operator.methodcaller('viewitems')

    def to_ascii(s):
        """Convert the unicode 's' to a ASCII string
        Usefull to remove accent (diacritics)"""
        if isinstance(s, binary_type):
            return s
        return unicodedata.normalize('NFKD', s).encode('ASCII', 'ignore')

    def listitems(d):
        return d.items()

    def listkeys(d):
        return d.keys()

    def listvalues(d):
        return d.values()

    def iteritems(d):
        return d.iteritems()

    def iterkeys(d):
        return d.iterkeys()

    def itervalues(d):
        return d.itervalues()

    def u(s):
        if isinstance(s, text_type):
            return s
        return s.decode('utf-8')

    def b(s):
        if isinstance(s, binary_type):
            return s
        return s.encode('utf-8', 'replace')

    def nativestr(s):
        if isinstance(s, binary_type):
            return s
        return s.encode('utf-8', 'replace')