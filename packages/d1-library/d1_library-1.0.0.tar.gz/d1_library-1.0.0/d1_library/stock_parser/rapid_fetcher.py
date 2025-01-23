# -*- coding: utf-8 -*-
"""
Created on 30/12/2023
Author: D-one
"""
import importlib.util
from alpha_vantage.timeseries import TimeSeries
import time
import pandas as pd
from datetime import datetime


class AlphaVantageFetcher:
    def __init__(self, secrets_path=None):
        if secrets_path:
            # Загружаем модуль secrets динамически из указанного пути
            spec = importlib.util.spec_from_file_location("secrets", secrets_path)
            secrets = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(secrets)
            self.rapid_api_cred = secrets.rapid_api_cred
        else:
            raise ValueError("secrets_path must be provided")
        self.api_key = self.rapid_api_cred.get('rapid_api_key')
        self.host = self.rapid_api_cred.get('rapid_api_host')
        self.ts = TimeSeries(key=self.api_key, rapidapi=True)

    def get_symbol_data(self, symbol):
        """
        s = AlphaVantageFetcher(key).get_symbol_data(symbol)
        :param symbol:
        :return:
        """
        data_ts, data_md = self.ts.get_daily_adjusted(symbol=symbol, outputsize="full")
        data_rows = [
            [
                datetime.strptime(d, "%Y-%m-%d").date(),
                float(p['1. open']),
                float(p['2. high']),
                float(p['3. low']),
                float(p['4. close']),
                float(p['5. adjusted close']),
                int(p['6. volume']),
                float(p['7. dividend amount']),
                float(p['8. split coefficient']),
                data_md['2. Symbol']
            ]
            for d, p in data_ts.items()
        ]
        symbol_data = pd.DataFrame(data_rows, columns=['date_price',
                                                       'open_price',
                                                       'high_price',
                                                       'low_price',
                                                       'close_price',
                                                       'adj_close_price',
                                                       'total_volume',
                                                       'dividend_amount',
                                                       'split_coefficient',
                                                       'symbol'])
        return symbol_data

    def get_all_symbol_data(self, symbols):
        """
        ss = AlphaVantageFetcher(key).get_all_symbol_data(symbols)
        :param symbols:
        :return:
        """
        all_symbol_data = []
        r = 0
        for each in symbols:
            try:
                if r < 75:
                    data = self.get_symbol_data(each)
                    all_symbol_data.append(data)
                    r += 1
                else:
                    time.sleep(60)
                    r = 0
            except:
                continue
        all_symbol_data_df = pd.concat(all_symbol_data, ignore_index=True)
        return all_symbol_data_df
