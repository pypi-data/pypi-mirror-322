# -*- coding: utf-8 -*-
"""
Created on 04/01/2024
Author: D-one
"""
import os
import importlib.util
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
import pandas as pd
from datetime import timedelta, datetime

# Dynamically determine the base path
BASE_PATH = os.path.dirname(os.path.abspath(__file__))


class DatabaseFetcher:
    """
    Это класс для выгрузки данных из базы данных
    """
    # Устанавливаем путь к secrets файлу если он передан

    def __init__(self, secrets_path=None, timeout=5):
        if secrets_path:
            # Загружаем модуль secrets динамически из указанного пути
            spec = importlib.util.spec_from_file_location("secrets", secrets_path)
            secrets = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(secrets)
            self.db_cred = secrets.db_secmaster_cred
        else:
            raise ValueError("secrets_path must be provided")
        self.engine_url = (f"postgresql://{self.db_cred.get('dbUser')}:{self.db_cred.get('dbPWD')}@"
                           f"{self.db_cred.get('dbHost')}/{self.db_cred.get('dbName')}")
        self.engine = create_engine(self.engine_url, connect_args={'connect_timeout': timeout})

    def connect(self):
        try:
            engine = create_engine(self.engine_url)
            connection = engine.connect()
            return connection
        except OperationalError:
            print("Error: Unable to establish a database connection.")
            return None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_connection()

    def _execute_sql(self, f_sql, **kwargs):
        try:
            sql_file_path = os.path.join(BASE_PATH, 'sql_scripts', f_sql)
            with open(sql_file_path, 'r', encoding='utf-8') as sql_file:
                # Assuming kwargs has keys 'start', 'end', and 'symbol' that we want to check
                condition = '=' if isinstance(kwargs.get('symbol'), str) else 'IN'
                symbol_str = ', '.join(f"'{s}'" for s in kwargs.get('symbol')) if isinstance(kwargs.get('symbol'),
                                                                                             list) else kwargs.get(
                    'symbol')
                sql_query = sql_file.read().format(condition=condition, start=kwargs.get('start'),
                                                   end=kwargs.get('end'), symbol=symbol_str, date=kwargs.get('date'))
                df = pd.read_sql_query(sql_query, self.engine)
            return df
        except Exception as e:
            print(f"Error executing SQL: {e}")
            return None

    def get_daily_data(self, start, end):
        """
        Все данные в разрезе дней за период
        :param start: пример - '2018-01-01'
        :param end: пример - '2018-12-31'
        :return: df с ценами закрытия за период
        """
        df = self._execute_sql('daily_data.sql', start=start, end=end)
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values(by='date').reset_index(drop=True)
        df['close'] = df['close'].apply(lambda x: float(x))
        return df

    def get_spec_daily_data(self, start, end, symbol):
        """
        Данные по выбранным тикерам за период
        :param start: пример - '2018-01-01'
        :param end: пример - '2018-12-31'
        :param symbol: нужные символы в list ~ symbol = ['A', 'AA', 'NIO']
        :return: df с ценами закрытия за период
        """
        symbol = tuple(str(x) for x in symbol)
        df = self._execute_sql('daily_spec_data.sql', start=start, end=end, symbol=symbol)
        if df is None or 'date' not in df.columns or 'close' not in df.columns:
            print("Error: DataFrame does not have expected columns.")
            return None
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values(by='date').reset_index(drop=True)
        df['close'] = df['close'].apply(lambda x: float(x))
        return df

    def fetch_exchange_id(self, abbrev):
        """
        Выгрузка id рынка
        :param abbrev: 'NYSE'
        :return: exchange_id
        """
        exchange_id = self._execute_sql('exchange_id.sql', abbrev=abbrev)
        return exchange_id['id'].iloc[0]

    def fetch_vendor_id(self, vendor_name):
        """
        Выгрузка id вендора данных
        :param vendor_name: 'Alpha_Vantage'
        :return: vendor_id
        """
        vendor_id = self._execute_sql('vendor_id.sql', vendor_name=vendor_name)
        return vendor_id['id'].iloc[0]

    def fetch_symbol_id(self):
        """
        :return: symbol_id
        """
        symbol_id = self._execute_sql('symbol_id.sql')
        return symbol_id

    def get_actual_symbols(self):
        """
        :return: список уникальных тикеров за последние 3 дня
        """
        dat = (datetime.now() + timedelta(hours=-72)).date()
        symbol = self._execute_sql('symbols.sql', date=dat)
        return list(symbol['symbol'])

    def close_connection(self):
        self.engine.dispose()
