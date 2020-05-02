#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Module for data analyze."""

import json
import datetime
import ijson
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style='darkgrid')


class Analyze:
    """Analyze module"""

    def __init__(self, filename, chart_filename):
        self.filename = filename
        self.chart_filename = chart_filename

    @staticmethod
    def parse_float(number_to_validate):
        """Parse float number"""
        result = 0.0
        if number_to_validate \
                and isinstance(number_to_validate, str):
            if number_to_validate.isnumeric():
                result = float(number_to_validate)
        else:
            if number_to_validate \
                    and isinstance(number_to_validate, float):
                result = number_to_validate
        return result

    @staticmethod
    def parse_full_date(row):
        """Parse data """
        date = datetime.datetime.strptime(
            row["last_update"], "%Y-%m-%d %H:%M:%S"
        )
        return date

    @staticmethod
    def dateplot(axis_x, axis_y, **kwargs):
        """Plot data ito chart """
        axis_ax = plt.gca()
        data = kwargs.pop('data')
        data.plot(x=axis_x, y=axis_y, ax=axis_ax, grid=False, **kwargs)

    @staticmethod
    def country_get_data(country_dictionary, country_title, columns):
        """Get data by countries """
        arr = []
        for key, values in country_dictionary.items():
            if key == country_title:
                for row in values:
                    selected_row = []
                    for item in columns['names']:
                        selected_row.append(row[item])
                    selected_row.append(country_title)
                    arr.append(selected_row)
        return arr

    def init(self):
        """Init analyze process"""
        country_dict = {}
        data = []
        countries = []
        columns = {
            'infile': [],
            'good': [
                'date',
                'confirmed',
                'deaths',
                'recovered',
                'confirmed_diff',
                'deaths_diff',
                'recovered_diff',
                'last_update',
                'active',
                'active_diff',
                'fatality_rate',
                'region'
            ],
            'names': []
        }
        with open(self.filename) as file_stream:
            for json_obj in file_stream:
                country_dict = json.loads(json_obj)

        if country_dict['data']:
            for key in country_dict['data'].items():
                countries.append(key)

        with open(self.filename, 'r') as file_stream:
            objects = ijson.kvitems(file_stream, 'data.Russia.item')
            for key in objects:
                if key[0] and key[0] not in columns['infile'] \
                        and key[0] not in ['region']:
                    columns['infile'].append(key[0])
                    columns['names'].append(key[0])
            # confirmed = (v for k, v in objects if k == 'confirmed')

        columns['infile'].append('region')

        for country_key in countries:
            for item in self.country_get_data(country_dict['data'],
                                              country_key,
                                              columns):
                data.append(item)

        pandas_data_frame = pd.DataFrame(data, columns=columns['good'])
        pandas_data_frame['fatality_rate'] = \
            pandas_data_frame['fatality_rate'].apply(self.parse_float)
        pandas_data_frame['date'] = \
            pandas_data_frame.apply(self.parse_full_date, axis=1)

        grid = sns.FacetGrid(pandas_data_frame,
                             col='region',
                             height=10,
                             aspect=0.8,
                             legend_out=True)
        grid = grid.map_dataframe(self.dateplot,
                                  'date',
                                  'confirmed',
                                  color='g',
                                  marker='.')
        grid.fig.autofmt_xdate()

        grid = grid.map_dataframe(self.dateplot,
                                  'date',
                                  'recovered',
                                  color='r',
                                  marker='.')
        grid.fig.autofmt_xdate()

        grid = grid.map_dataframe(self.dateplot,
                                  'date',
                                  'deaths',
                                  color='y',
                                  marker='.')
        grid.fig.autofmt_xdate()

        grid = (grid.map_dataframe(self.dateplot,
                                   'date',
                                   'fatality_rate',
                                   color='b').add_legend())
        grid.fig.autofmt_xdate()
        grid.savefig(self.chart_filename)
