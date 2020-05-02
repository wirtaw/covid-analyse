#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Module documentation goes here."""

import unittest
import sys
from src.app import Application
from src.app import main

class MyTestCase(unittest.TestCase):
    """Class documentation goes here."""
    def test_default_greeting_set(self):
        """Test documentation goes here."""
        input="SDF"
        app = Application()
        app.set_message(input)
        self.assertEqual(app.message, input)
        main(sys.argv[1:])

    def test_wrong_period_set(self):
        """Wrong period"""
        app = Application()
        app.set_period('')
        self.assertEqual(app.period, 7)
        main(sys.argv[1:])

    def test_empty_period_set(self):
        """Empty period"""
        app = Application()
        app.set_period()
        self.assertEqual(app.period, 7)
        main(sys.argv[1:])

    def test_10_str_period_set(self):
        """10 days period"""
        input="10"
        app = Application()
        app.set_period(input)
        self.assertEqual(app.period, int(input))
        main(sys.argv[1:])

    def test_14_period_set(self):
        """14 days period"""
        input = 14
        app = Application()
        app.set_period(input)
        self.assertEqual(app.period, input)
        main(sys.argv[1:])

    def test_wrong_countries_set(self):
        """Wrong countries"""
        app = Application()
        app.set_countries('')
        self.assertEqual(app.countries, ['USA', 'CHN', 'ITA'])
        main(sys.argv[1:])

    def test_empty_countries_set(self):
        """Empty countries"""
        app = Application()
        app.set_countries()
        self.assertEqual(app.countries, ['USA', 'CHN', 'ITA'])
        main(sys.argv[1:])

    def test_UA_countries_set(self):
        """Set one country"""
        app = Application()
        app.set_countries('UA')
        self.assertEqual(app.countries, ['UA'])
        main(sys.argv[1:])

    def test_list_countries_set(self):
        """Set list country"""
        input = 'LTU,BLR,POL'
        app = Application()
        app.set_countries(input)
        self.assertEqual(app.countries, ['LTU', 'BLR', 'POL'])
        main(sys.argv[1:])

if __name__ == '__main__':
    unittest.main()
