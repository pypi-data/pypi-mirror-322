# -*- coding: utf-8 -*-
"""
Created on 15/01/2024
Author: D-one
"""
import importlib.util
import requests
from itertools import islice
import pandas as pd
from datetime import datetime
import pytz


class TdameritradeFetcher(object):
    def __init__(self, secrets_path=None):
        if secrets_path:
            # Загружаем модуль secrets динамически из указанного пути
            spec = importlib.util.spec_from_file_location("secrets", secrets_path)
            secrets = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(secrets)
            self.tdameritrade_cred = secrets.tdameritrade_cred
        else:
            raise ValueError("secrets_path must be provided")
        self.consumer_key = self.tdameritrade_cred.get('consumer_key')

    def _get_symbol_data(self, symbols):
        data = self._fetch_data_from_api(r"https://api.tdameritrade.com/v1/marketdata/quotes",
                                         {'symbol': ','.join(symbols)})
        if data is None:
            return pd.DataFrame()
        else:
            return pd.DataFrame.from_dict(data, orient='index').reset_index(drop=True)
    @staticmethod
    def _chunks(iterable, n):
        it = iter(iterable)
        while True:
            chunk = tuple(islice(it, n))
            if not chunk:
                return
            yield chunk

    def is_market_open(self):
        today = datetime.today().astimezone(pytz.timezone("America/New_York")).strftime('%Y-%m-%d')
        data = self._fetch_data_from_api('https://api.tdameritrade.com/v1/marketdata/EQUITY/hours', {'date': today})

        if data is None:
            print('Не удалось получить данные о состоянии рынка.')
            return False

        if data.get('equity', {}).get('EQ', {}).get('isOpen'):
            return True
        else:
            print('Рынок закрыт')
            return False

    def get_all_symbols_daily_data(self, symbols):
        if self.is_market_open():
            today = datetime.today().astimezone(pytz.timezone("America/New_York")).strftime('%Y-%m-%d')
            df = pd.concat([self._get_symbol_data(chunk) for chunk in self._chunks(set(symbols), 200)], sort=False)
            df = df.sort_values(by=['symbol'], ascending=True)
            columns = ['symbol', 'openPrice', 'highPrice', 'lowPrice', 'closePrice', 'totalVolume']
            df = df[columns] if all(col in df.columns for col in columns) else df
            df['date'] = pd.to_datetime(today)
            df = df.rename(columns={
                'openPrice': 'open',
                'highPrice': 'high',
                'lowPrice': 'low',
                'closePrice': 'close',
                'totalVolume': 'volume'
            })
            df['data_vendor_id'] = 3
            df['stock_id'] = 1
            df['u_key'] = df['symbol'].astype(str) + '_' + df['date'].astype(str)
            return df

    def _fetch_data_from_api(self, url, params):
        params.update({'apikey': self.cred.get('consumer_key')})
        try:
            request = requests.get(url=url, params=params)
            request.raise_for_status()  # Raises stored HTTPError, if one occurred.
            return request.json()
        except requests.exceptions.HTTPError as e:
            print('HTTP error occurred: ' + str(e))
            return None
        except KeyError:
            print('Рынок сегодня не работает')
            return None
