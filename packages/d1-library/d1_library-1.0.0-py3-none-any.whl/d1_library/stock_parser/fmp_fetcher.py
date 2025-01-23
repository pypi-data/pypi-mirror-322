# -*- coding: utf-8 -*-
"""
Created on 24/01/2024
Author: D-one
"""
import importlib.util
import time
import pandas as pd
from fmp_python.fmp import FMP
from datetime import datetime
import requests


class FMPFetcher:
    RATE_LIMIT = 300  # лимит запроса
    SLEEP_TIME = 60  # на сколько сек уснуть после превышения лимита
    DATA_VENDOR_ID = 5  # FMP id в базе
    STOCK_ID = 1  # id биржи - nyse = 1

    def __init__(self, secrets_path=None):
        if secrets_path:
            # Загружаем модуль secrets динамически из указанного пути
            spec = importlib.util.spec_from_file_location("secrets", secrets_path)
            secrets = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(secrets)
            self.fmp_cred = secrets.fmp_cred
        else:
            raise ValueError("secrets_path must be provided")
        self.fmp_api_key = self.fmp_cred.get('fmp_api_key')
        self.fmp = FMP(api_key=self.fmp_api_key, output_format='pandas')
        self.columns_for_db = ['data_vendor_id',
                               'stock_id',
                               'date',
                               'open',
                               'high',
                               'low',
                               'close',
                               'volume',
                               'symbol',
                               'u_key']

    def fetch_data(self, symbols, fetch_func, **kwargs):
        """
        Линейный запрос к FMP
        """
        symbol_data = []
        r = 0
        max_retries = 3  # Добавляем повторные попытки
        
        for each in symbols:
            for attempt in range(max_retries):
                try:
                    if r < self.RATE_LIMIT:
                        data = fetch_func(each, **kwargs)
                        if not data.empty and isinstance(data, pd.DataFrame):
                            data['symbol'] = each
                            symbol_data.append(data)
                            r += 1
                            break  # Успешно получили данные
                        else:
                            print(f"Empty or invalid data for symbol {each}")
                    else:
                        if symbol_data:
                            print(f"Rate limit reached, sleeping for {self.SLEEP_TIME} seconds")
                            time.sleep(self.SLEEP_TIME)
                            r = 0
                except requests.exceptions.RequestException as e:
                    if attempt == max_retries - 1:  # Последняя попытка
                        print(f"Failed to fetch data for {each} after {max_retries} attempts: {e}")
                    else:
                        print(f"Attempt {attempt + 1} failed for {each}, retrying...")
                        time.sleep(5)  # Ждем 5 секунд перед повторной попыткой
                except Exception as e:
                    print(f"Unexpected error for symbol {each}: {e}")
                    break
        
        if not symbol_data:
            print("No valid data collected for any symbols")
            return pd.DataFrame()
        
        # Проверяем согласованность колонок
        columns = symbol_data[0].columns
        filtered_data = []
        for df in symbol_data:
            if all(col in df.columns for col in columns):
                filtered_data.append(df[columns])  # Используем только нужные колонки
        
        if not filtered_data:
            print("No consistent data found across symbols")
            return pd.DataFrame()
        
        return pd.concat(filtered_data, ignore_index=True)

    def prepare_data(self, df):
        """
        Добавление полй для базы данных
        :param df: выгрузка из FMP
        :return: df спец. структурой
        """
        df['data_vendor_id'] = self.DATA_VENDOR_ID
        df['stock_id'] = self.STOCK_ID
        df['u_key'] = df['symbol'].astype(str) + '_' + df['date'].astype(str)
        df = df.drop_duplicates(subset='u_key')
        return df[self.columns_for_db]

    def get_all_symbol_data(self, symbol, from_date):
        """
        Выгрузка всей истории по символам с определенной даты
        :param symbol: ['A']
        :param from_date: str format 'YYYY-MM-DD'
        :return: df history
        """
        def fetch_with_date(symbol, from_date):
            url = f"https://financialmodelingprep.com/api/v3/historical-price-full/{symbol}"
            params = {
                'from': from_date,
                'to': datetime.now().strftime('%Y-%m-%d'),
                'apikey': self.fmp_api_key
            }
            try:
                response = requests.get(url, params=params)
                if response.status_code == 200:
                    data = response.json()
                    if 'historical' in data:
                        df = pd.DataFrame(data['historical'])
                        df['date'] = pd.to_datetime(df['date'])
                        df['symbol'] = symbol
                        # Сортируем по дате и удаляем дубликаты с учетом символа
                        df = df.sort_values('date').drop_duplicates(subset=['date', 'symbol'])
                        df = df.ffill()
                        return df
                    print(f"No data received for {symbol}")
                    return pd.DataFrame()
            except Exception as e:
                print(f"Error fetching data for {symbol}: {str(e)}")
                return pd.DataFrame()

        all_symbol_data_df = self.fetch_data(symbol, fetch_with_date, from_date=from_date)
        if not all_symbol_data_df.empty:
            all_symbol_data_df['date'] = pd.to_datetime(all_symbol_data_df['date']).dt.date
            numeric_columns = ['open', 'high', 'low', 'close', 'volume']
            all_symbol_data_df[numeric_columns] = all_symbol_data_df[numeric_columns].ffill()
            all_symbol_data_df[numeric_columns] = all_symbol_data_df[numeric_columns].bfill()
            
            return self.prepare_data(all_symbol_data_df)
        return pd.DataFrame()

    def get_quote_short(self, symbols):
        """
        Выгрузка по символам за 1d+
        :param symbols: ['A','AA',..,]
        :return: df
        """
        symbol_data_df = self.fetch_data(symbols, self.fmp.get_quote)
        symbol_data_df['date'] = pd.to_datetime(symbol_data_df['timestamp'].apply(
            lambda x: datetime.fromtimestamp(x).strftime('%Y-%m-%d')))
        symbol_data_df.rename(columns={'dayHigh': 'high', 'dayLow': 'low', 'price': 'close'}, inplace=True)
        return self.prepare_data(symbol_data_df)

    def get_historical_data(self, symbol, start_date=None, end_date=None):
        """
        Получает исторические данные для символа
        :param symbol: str
        :param start_date: str format 'YYYY-MM-DD'
        :param end_date: str format 'YYYY-MM-DD'
        :return: pd.DataFrame
        """
        try:
            # Используем правильные параметры API
            if start_date:
                historical_data = self.fmp.get_historical_price(
                    symbol,
                    from_date=start_date,  # Ипользуем from_date вместо _from
                    to_date=end_date if end_date else datetime.now().strftime('%Y-%m-%d')
                )
            else:
                historical_data = self.fmp.get_historical_price(symbol)
                
            if not historical_data:
                return pd.DataFrame()
                
            df = pd.DataFrame(historical_data)
            df['date'] = pd.to_datetime(df['date'])
            df.set_index('date', inplace=True)
            return df
            
        except Exception as e:
            print(f"Error fetching data for symbol {symbol}: {str(e)}")
            return pd.DataFrame()

    def get_price_target(self, symbol):
        """
        Получение целевых цен аналитиков для акции
        """
        url = f"https://financialmodelingprep.com/api/v3/price-target/{symbol}"
        params = {'apikey': self.fmp_api_key}
        try:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                return pd.DataFrame(data)
            return pd.DataFrame()
        except Exception as e:
            print(f"Error fetching price target for {symbol}: {str(e)}")
            return pd.DataFrame()

    def get_analyst_estimates(self, symbol):
        """
        Получение оценок аналитиков
        """
        url = f"https://financialmodelingprep.com/api/v3/analyst-estimates/{symbol}"
        params = {'apikey': self.fmp_api_key}
        try:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                return pd.DataFrame(data)
            return pd.DataFrame()
        except Exception as e:
            print(f"Error fetching analyst estimates for {symbol}: {str(e)}")
            return pd.DataFrame()

    def get_social_sentiment(self, symbol):
        """
        Получение социальных настроений по акции
        """
        url = f"https://financialmodelingprep.com/api/v4/social-sentiment/{symbol}"
        params = {'apikey': self.fmp_api_key}
        try:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                return pd.DataFrame(data)
            return pd.DataFrame()
        except Exception as e:
            print(f"Error fetching social sentiment for {symbol}: {str(e)}")
            return pd.DataFrame()

    def get_company_profile(self, symbol):
        """
        Получение профиля компании
        """
        url = f"https://financialmodelingprep.com/api/v3/profile/{symbol}"
        params = {'apikey': self.fmp_api_key}
        try:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                return pd.DataFrame(data)
            return pd.DataFrame()
        except Exception as e:
            print(f"Error fetching company profile for {symbol}: {str(e)}")
            return pd.DataFrame()

    def get_analyst_recommendations(self, symbol):
        """
        Получение рекомендаций аналитиков для акции
        """
        url = f"https://financialmodelingprep.com/api/v3/analyst-stock-recommendations/{symbol}"
        params = {'apikey': self.fmp_api_key}
        try:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                df = pd.DataFrame(data)
                if not df.empty:
                    # Сортируем по дате и берем самые свежие данные
                    df['date'] = pd.to_datetime(df['date'])
                    df = df.sort_values('date', ascending=False)
                    latest_rec = df.iloc[0]
                    
                    # Создаем новый DataFrame с правильными названиями полей
                    return pd.DataFrame([{
                        'strongBuy': latest_rec['analystRatingsStrongBuy'],
                        'buy': latest_rec['analystRatingsbuy'],
                        'hold': latest_rec['analystRatingsHold'],
                        'sell': latest_rec['analystRatingsSell'],
                        'strongSell': latest_rec['analystRatingsStrongSell'],
                        'date': latest_rec['date']
                    }])
                return pd.DataFrame()
            return pd.DataFrame()
        except Exception as e:
            print(f"Error fetching analyst recommendations for {symbol}: {str(e)}")
            return pd.DataFrame()
