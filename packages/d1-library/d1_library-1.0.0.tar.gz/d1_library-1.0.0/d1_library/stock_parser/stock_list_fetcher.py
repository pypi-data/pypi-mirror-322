# -*- coding: utf-8 -*-
"""
Created on 30/12/2023
Author: D-one
"""
import requests
import pandas as pd


class StockListFetcher(object):
    """
    Класс для парсинга информации о компаниях торгующихся на рынках:
    'NYSE', 'NASDAQ', 'AMEX'
    example: ss = StockListFetcher('NYSE').get_stock_df()
    """
    def __init__(self, exchange_name):
        self.BASE_URL_API = 'https://api.nasdaq.com/api/screener/stocks'
        self.exchange_name = exchange_name
        self.data = self._get_soup_json()

    def _get_soup_json(self):
        headers = {
            'authority': 'api.nasdaq.com',
            'accept': 'application/json, text/plain, */*',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/87.0.4280.141 Safari/537.36',
            'origin': 'https://www.nasdaq.com',
            'sec-fetch-site': 'same-site',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://www.nasdaq.com/',
            'accept-language': 'en-US,en;q=0.9',
        }
        params = (
            ('tableonly', 'true'),
            ('limit', '25'),
            ('offset', '0'),
            ('download', 'true'),
            ('exchange', self.exchange_name)
        )
        r = requests.get(self.BASE_URL_API, headers=headers, params=params)
        data = r.json()['data']

        return data

    def _get_us_stock_df(self, selected_columns=None):
        df = pd.DataFrame(self.data['rows'], columns=self.data['headers'])
        us_stock_df = df[~df['symbol'].str.contains(r'\.|\^|\s')]
        base_columns = ['symbol', 'name', 'country', 'sector', 'industry', 'ipoyear', 'marketCap', 'volume', 'url']
        if selected_columns is None:
            selected_columns = base_columns
        us_stock_df = us_stock_df[selected_columns]
        us_stock_df['symbol'] = us_stock_df['symbol'].str.replace("/", "-")
        return us_stock_df

    def get_stock_df(self, selected_columns=None):
        """
        Вернет df с информацией о всех тикерах на выбранном рынке
        :param selected_columns: [] ->
        - 'symbol',
        - 'name',
        - 'country',
        - 'sector',
        - 'industry',
        - 'ipoyear',
        - 'marketCap',
        - 'volume',
        - 'url'
        :return: df with selected columns
        """
        return self._get_us_stock_df(selected_columns)
