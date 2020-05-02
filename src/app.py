#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Module documentation goes here."""

from __future__ import print_function

__author__ = "Vladimir Poplavskij"
__copyright__ = "Copyright 2020, Vladimir Poplavskij"
__credits__ = ["C D", "A B"]
__license__ = "Apache 2.0"
__version__ = "1.0.1"
__maintainer__ = "Vladimir Poplavskij"
__email__ = "float45@gmail.com"
__status__ = "Development"

import os
import sys
import argparse
from logzero import logger


PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_DIR)

import scrapping


def log(function):
    """Handy logging decorator."""

    def inner(*args, **kwargs):
        """Innter method."""
        logger.debug(function)
        function(*args, **kwargs)

    return inner


class Application():
    """Main application"""

    def __init__(self):
        self.message = 'Welcome to the COVID-19 analyse app!'
        self.countries = []
        self.period = 0

    def set_message(self, message):
        """Welcome message."""
        self.message = message

    @log
    def print_message(self):
        """Function description."""
        print(self.message)

    def set_period(self, period=None):
        """Set period in the days. (default 7)"""
        if period and isinstance(period, str):
            if period.isnumeric():
                self.period = int(period)
            else:
                self.period = 7
        else:
            if period and isinstance(period, int):
                self.period = period
            else:
                self.period = 7

    def set_countries(self, countries=None):
        """Set list of the countries (ISO) divided by comma.
        Default (['USA', 'CHN', 'ITA'])"""
        if countries and isinstance(countries, str):
            if countries.find(',') != -1:
                self.countries = countries.split(',')
            else:
                self.countries.append(countries)
        else:
            self.countries = ['USA', 'CHN', 'ITA']


def main(args):
    """ Main entry point of the app """
    app = Application()
    if args and args.period:
        app.set_period(args.period)
    if args and args.countries:
        app.set_countries(args.countries)
    app.print_message()

    if args and args.period and args.countries:
        scrapper = scrapping.Scrapper(app.period,
                                      app.countries,
                                      './data/countriesData.json')
        scrapper.init()

    logger.info(args)


if __name__ == "__main__":
    PARSER = argparse.ArgumentParser()

    # Optional argument flag which defaults to False
    PARSER.add_argument("-f", "--flag", action="store_true", default=False)

    # Optional argument which requires a parameter (eg. -d test)
    PARSER.add_argument("-n", "--name", action="store", dest="name")
    PARSER.add_argument("-c", "--countries", action="store", dest="countries")
    PARSER.add_argument("-p", "--period", action="store", dest="period")

    # Optional verbosity counter (eg. -v, -vv, -vvv, etc.)
    PARSER.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Verbosity (-v, -vv, etc)")

    # Specify output of "--version"
    PARSER.add_argument(
        "--version",
        action="version",
        version="%(prog)s (version {version})".format(version=__version__))

    MYARGS = PARSER.parse_args()
    main(MYARGS)
