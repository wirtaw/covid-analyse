#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Module for data scrapping."""

import json
import http.client
from datetime import date


class Scrapper:
    """Scrapper application"""

    def __init__(self, period, countries, filename):
        self.api_endpoints = {
            'main': 'covid-api.com',
            'regions': '/api/regions',
            'reports': '/api/reports'
        }
        self.filename = filename
        self.period = period
        self.countries = countries
        self.conn = http.client.HTTPSConnection(self.api_endpoints['main'])
        self.countries_to_request = {}
        self.countries_data = {'data': {}}

    @staticmethod
    def json_validator(data):
        """Validate json"""
        try:
            json.loads(data)
            return True
        except ValueError as error:
            print("invalid json: %s" % error)
            return False

    def dates_for_data(self, iso):
        """Prepare data string dict for requests"""
        arr = []
        today = date.today()
        dateordinal = today.toordinal()
        preiod_iterator = 1
        while preiod_iterator < self.period:
            dateordinal = dateordinal - 1
            formatdate = date.fromordinal(dateordinal).isoformat()
            reports = self.api_endpoints['reports']
            arr.append(f"{reports}?date={formatdate}&iso={iso}")
            preiod_iterator += 1
        return arr

    def get_request_covid(self, query):
        """Make request to API"""
        payload = ''
        headers = {}
        self.conn.request("GET", query, payload, headers)
        res = self.conn.getresponse()

        return json.loads(res.read())

    def init(self):
        """Init scrapping process"""
        responseisojson = self.get_request_covid(self.api_endpoints['regions'])

        if responseisojson and responseisojson['data']:
            for country in responseisojson['data']:
                for value in self.countries:
                    if country['iso'] == value:
                        self.countries_to_request[country['name']] = \
                            self.dates_for_data(value)
            if self.countries_to_request:
                for key, values in self.countries_to_request.items():
                    self.countries_data['data'][key] = []
                    for query in values:
                        res = self.get_request_covid(query)
                        if len(res['data']) > 0:
                            self.countries_data['data'][key]\
                                .append(res['data'][0])
                if self.json_validator(json.dumps(self.countries_data)):
                    data_file = open(self.filename, "w")
                    data_file.write(json.dumps(self.countries_data))
                    data_file.close()
            else:
                print('No countries')
        else:
            print('No regions')
