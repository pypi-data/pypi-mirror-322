# -*- coding: utf-8 -*-
"""
Created on 30/01/2024
Author: D-one
"""
import os
import importlib.util
from sqlalchemy import create_engine, text
import pytz
import datetime as date
import pandas as pd
import time

# Dynamically determine the base path
BASE_PATH = os.path.dirname(os.path.abspath(__file__))


class DatabaseInsert:
    """
    Это класс для загрузки данных в базу данных
    """
    def __init__(self, secrets_path=None, timeout=30):
        if secrets_path:
            # Загружаем модуль secrets динамически из указанного пути
            spec = importlib.util.spec_from_file_location("secrets", secrets_path)
            secrets = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(secrets)
            self.db_cred = secrets.db_secmaster_cred
        else:
            raise ValueError("secrets_path must be provided")
        self.engine_url = self._construct_engine_url()
        self.engine = create_engine(
            self.engine_url,
            connect_args={
                'connect_timeout': timeout,
                'keepalives': 1,
                'keepalives_idle': 30,
                'keepalives_interval': 10,
                'keepalives_count': 5
            }
        )

    def _construct_engine_url(self):
        return (f"postgresql://{self.db_cred.get('dbUser')}:{self.db_cred.get('dbPWD')}@"
                f"{self.db_cred.get('dbHost')}/{self.db_cred.get('dbName')}")

    def insert_symbols(self, df, exchange_id):
        try:
            # Добавляем необходимые колонки
            df['exchange_id'] = exchange_id
            df['last_updated_date'] = date.datetime.now(pytz.UTC)

            # Создаем временную таблицу
            df.to_sql('temporary_table', self.engine, if_exists='replace', index=False)

            # Выполняем INSERT с ON CONFLICT
            with self.engine.connect() as conn:
                with open(os.path.join(BASE_PATH, 'sql_scripts', 'insert_symbols.sql'), 'r') as f:
                    sql = f.read()
                conn.execute(text(sql))
                conn.commit()

            return True

        except Exception as e:
            print(f"Error executing SQL: {e}")
            return False

    def insert_daily_data(self, df):
        max_retries = 3
        retry_delay = 5
        
        for attempt in range(max_retries):
            try:
                df.to_sql('temporary_table', self.engine, if_exists='replace', index=False)
                
                with self.engine.connect() as conn:
                    with open(os.path.join(BASE_PATH, 'sql_scripts', 'insert_daily_data.sql'), 'r') as f:
                        sql = f.read()
                    conn.execute(text(sql))
                    conn.commit()
                return True
                
            except Exception as e:
                if attempt == max_retries - 1:
                    print(f"Failed to insert data after {max_retries} attempts: {e}")
                    return False
                else:
                    print(f"Attempt {attempt + 1} failed, retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
