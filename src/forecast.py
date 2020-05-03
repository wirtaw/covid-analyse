#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Module for data forecast."""

import math
import json
import ijson
import pandas as pd
import statsmodels.api as sm
import seaborn as sns

sns.set(style='whitegrid')


class Forecast:
    """Forecast module"""

    def __init__(self, filename, country_forecast, after_days, chart_filename):
        self.chart_filename = chart_filename
        self.filename = filename
        self.country = country_forecast
        self.after_days = after_days

    @staticmethod
    def log(number_to_log):
        """Log number"""
        result = 0.0
        if number_to_log \
                and isinstance(number_to_log, str):
            if number_to_log.isnumeric():
                result = math.log(int(number_to_log))
        else:
            if number_to_log \
                    and isinstance(number_to_log, int):
                result = math.log(number_to_log)
        return result

    @staticmethod
    def country_get_data(country_dictionary, country_title, columns):
        """Get data by countries """
        arr = []
        for key, values in country_dictionary.items():
            if key == country_title[0]:
                time_counter = 0
                for row in values:
                    selected_row = [time_counter]
                    for item in columns['names']:
                        selected_row.append(row[item])
                    selected_row.append(country_title[0])
                    arr.append(selected_row)
        return arr

    def calculate_result(self, x_start, b_coef):
        """Get Calculate result """

        return x_start * math.pow(b_coef, self.after_days)

    def get_forecast(self):
        """Init forecast process"""
        country_dict = {}
        data = []
        countries = []
        columns = {
            'infile': [],
            'good': [
                'time',
                'date',
                'confirmed',
                'region'
            ],
            'names': [],
            'exclude': [
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
            ]
        }
        with open(self.filename) as file_stream:
            for json_obj in file_stream:
                country_dict = json.loads(json_obj)

        if country_dict['data']:
            for key in country_dict['data'].items():
                if key[0] == self.country:
                    countries.append(key)

        with open(self.filename, 'r') as file_stream:
            objects = ijson.kvitems(file_stream, 'data.Russia.item')
            for key in objects:
                if key[0] and key[0] not in columns['infile'] \
                        and key[0] not in columns['exclude']:
                    columns['infile'].append(key[0])
                    columns['names'].append(key[0])

        for country_key in countries:
            for item in self.country_get_data(country_dict['data'],
                                              country_key,
                                              columns):
                data.append(item)
        data = list(reversed(data))
        time_counter = 0
        for item in data:
            print(f"{time_counter} {item[1]} {item[2]}")
            item[0] = time_counter
            # print(f"{time_counter}")
            # print(f"{item[1]}")
            # print(f"{item[2]}")
            time_counter = time_counter + 1

        pandas_data_frame = pd.DataFrame(data, columns=columns['good'])
        pandas_data_frame['logConfirmed'] = \
            pandas_data_frame['confirmed'].apply(self.log)
        pandas_data_frame.head(10)

        X_axis = pandas_data_frame.time
        X_axis = sm.add_constant(X_axis)

        Y_axis = pandas_data_frame.logConfirmed

        mod = sm.OLS(Y_axis, X_axis)
        res = mod.fit()
        print(f"const {res.params.const} time {res.params.time}")

        x_start = math.exp(res.params.const)
        b_coef = math.exp(res.params.time)

        time_counter = 0
        start_date = data[0][1]
        length = len(data)
        forecast_data = []
        while time_counter < length:
            forecast_data.append([
                data[time_counter][2],
                int(x_start * math.pow(b_coef, time_counter))])
            time_counter = time_counter + 1

        dates = pd.date_range(start_date, periods=length, freq="D")

        pandas_data_frame_forecast = pd.DataFrame(
            forecast_data,
            dates,
            columns=[f"{self.country}",
                     f"forecast{self.country}"]
        )
        sns.lineplot(data=pandas_data_frame_forecast,
                     palette="tab10",
                     linewidth=2.5)
        plot = pandas_data_frame_forecast.plot()
        fig = plot.get_figure()
        fig.savefig(self.chart_filename)
        return int(self.calculate_result(x_start, b_coef))
