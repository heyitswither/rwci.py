# -*- coding: utf-8 -*-

"""
RWCI.py
~~~~~~~~~~~~~~~~~~~
An API wrapper for RWCI.

"""

from .client import Client
from .errors import BadLoginCredentials, BadEventListener
from .message import Message
from .user import User

__title__ = 'rwci'
__author__ = 'heyitswither'
__license__ = 'MIT'
__copyright__ = 'Copyright 2017-Present heyitswither'
__version__ = '0.1.0'
