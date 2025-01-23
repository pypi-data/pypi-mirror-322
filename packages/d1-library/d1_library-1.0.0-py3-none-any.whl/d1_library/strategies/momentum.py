# -*- coding: utf-8 -*-
"""
Created on 07/01/2024
Author: D-one
"""
import pandas as pd
import numpy as np
from typing import List, Union, Any
from scipy import stats


class Momentum(object):
    @staticmethod
    def _calculate_momentum_score(time_series: List[float]) -> float:
        length = len(time_series)
        x_values = np.arange(length)
        log_time_series = np.log(time_series)
        regression = stats.linregress(x_values, log_time_series)
        annualized_slope = (np.exp(regression.slope) ** 252 - 1) * 100

        return annualized_slope * (regression.rvalue ** 2)

    def calculate_momentum_score(self, df: pd.DataFrame, momentum_window: Union[int, str], minimum_momentum: int) -> pd.DataFrame:
        df['momentum'] = df.groupby('symbol')['close'].rolling(
            momentum_window,
            min_periods=minimum_momentum
        ).apply(self._calculate_momentum_score).reset_index(level=0, drop=True)
        return df

    def filter_by_date(self, df: pd.DataFrame, current_data_date: str) -> pd.DataFrame:
        df = df.loc[df['date'] == pd.to_datetime(current_data_date)]
        return df

    def get_top_symbols(self, df: pd.DataFrame, portfolio_size: int) -> list[Any]:
        df = df.sort_values(by='momentum', ascending=False).head(portfolio_size).reset_index(drop=True)
        return list(set(df['symbol'].tolist()))

    def calculate_momentum(self, df: pd.DataFrame, momentum_window: Union[int, str], minimum_momentum: int,
                           current_data_date: str, portfolio_size: int) -> list[Any]:
        df = self.calculate_momentum_score(df, momentum_window, minimum_momentum)
        df = self.filter_by_date(df, current_data_date)
        return self.get_top_symbols(df, portfolio_size)
