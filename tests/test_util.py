#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import datetime
import unittest

from io import StringIO

from send_email_to_me import util


class TestUtil(unittest.TestCase):
    def setUp(self):
        self.captor = StringIO()
        sys.stdout = self.captor

    def tearDown(self):
        sys.stdout = sys.__stdout__

    def test_days_left(self):
        days_left = util.get_days_left(datetime.datetime(2018, 7, 9, 0, 0, 1), '2018/7/17')
        self.assertEqual(days_left, 7)

    def test_is_holiday(self):
        result = util.is_holiday(datetime.datetime(2018, 7, 16))
        self.assertTrue(result)
        result = util.is_holiday(datetime.datetime(2018, 7, 17))
        self.assertFalse(result)

    def test_days_off(self):
        days_off = util.get_days_off(datetime.datetime(2018, 7, 9, 0, 0, 1), '2018/7/17')
        self.assertEqual(days_off, 3)


if __name__ == "__main__":
    unittest.main()