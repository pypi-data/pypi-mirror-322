#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-
# author： NearlyHeadlessJack
# email: wang@rjack.cn
# datetime： 2025/1/6 13:19 
# ide： PyCharm
# file: test_demo.py
import unittest
import os
from weauth.constants import exit_code

@unittest.skip('待重写')
class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(os.system('python WeAuth.py -test'),0)  # add assertion here


if __name__ == '__main__':
    unittest.main()
