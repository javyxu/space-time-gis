# -*- coding: utf-8 -*-
# pylint: disable=C,R,W
'''
# Created on Mar-16-19 03:31
# Author: javy@xu
# Email: xujavy@gmail.com
# Description: File's test_helloworld.py module
'''

import os
import unittest

from spacetimegis.core import helloworld

class Test_HelloWorld(unittest.TestCase):
    def test_helloworld(self):
        helloworld.hellworld()


if __name__ == "__main__":
    unittest.main()
