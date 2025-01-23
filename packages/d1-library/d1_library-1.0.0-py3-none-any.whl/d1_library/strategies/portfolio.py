# -*- coding: utf-8 -*-
"""
Created on 11/01/2024
Author: D-one
"""
import pandas as pd
from pypfopt import EfficientFrontier, objective_functions, risk_models, expected_returns
from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices
import cvxpy as cp


class OptimizationPortfolio(object):
    def __init__(self, data, df_pf, cash):
        self.data = data
        self.df_u = self.create_pivot_table()
        self.df_pf = df_pf
        self.cash = cash
        self.new_portfolio = None

    def create_pivot_table(self):
        return self.data.pivot_table(
            index='date',
            columns='symbol',
            values='close',
            aggfunc='sum')

    def create_efficient_frontier(self):
        mu = expected_returns.mean_historical_return(self.df_u)
        s = risk_models.sample_cov(self.df_u)
        ef = EfficientFrontier(mu, s)
        ef.add_objective(objective_functions.L2_reg, gamma=1)
        ef.add_constraint(lambda w: w <= 0.25)
        ef.max_sharpe()

        # Добавление ограничения на максимальный вес 25%
        return ef

    def create_discrete_allocation(self, cleaned_weights):
        latest_prices = get_latest_prices(self.df_u)
        da = DiscreteAllocation(cleaned_weights, latest_prices, total_portfolio_value=self.cash)
        allocation, leftover = da.greedy_portfolio()
        return allocation

    def calculate_portfolio(self):
        ef = self.create_efficient_frontier()
        cleaned_weights = ef.clean_weights()
        return self.create_discrete_allocation(cleaned_weights)

    def create_output_df(self, allocation):
        symbol_list = list(allocation.keys())
        num_shares_list = list(allocation.values())
        qty_dict = dict(zip(symbol_list, num_shares_list))
        data = self.data.loc[self.data['symbol'].isin(symbol_list)]
        data = data.loc[data['date'] == data['date'].max()].sort_values(by='symbol')
        data['qty_new'] = data['symbol'].map(qty_dict)
        data['amount_held'] = data['close'] * data['qty_new']
        return data.loc[data['qty_new'] != 0]

    def get_new_portfolio(self):
        if self.new_portfolio is None:
            allocation = self.calculate_portfolio()
            self.new_portfolio = self.create_output_df(allocation)
        return self.new_portfolio

    def get_buy_sell_stocks(self):
        df = self.get_new_portfolio()
        # Переименовываем столбец 'qty' в 'position' для соответствия с IBKR API
        df = pd.merge(df, self.df_pf.rename(columns={'qty': 'position'}), on='symbol', how='outer').fillna(0)
        df['qty_b_s'] = df['qty_new'] - df['position']
        df = df[df['qty_b_s'] != 0]
        df_buy = df.loc[df['qty_b_s'] > 0][['symbol', 'qty_b_s']]
        df_sell = df.loc[df['qty_b_s'] < 0][['symbol', 'qty_b_s']]
        df_sell['qty_b_s'] = df_sell['qty_b_s'] * -1
        return df_buy, df_sell
