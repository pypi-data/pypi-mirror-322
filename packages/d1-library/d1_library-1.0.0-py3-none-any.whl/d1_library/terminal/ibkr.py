# -*- coding: utf-8 -*-
"""
Created on 19/02/2024
Author: D-one
"""
import pandas as pd
import time
import logging
import os
from ib_insync import IB, Stock, MarketOrder, util
util.startLoop()


class IBAPI:
    #SERVER_IP = os.getenv('IB_HOST', '127.0.0.1')
    SERVER_IP = os.getenv('IB_HOST', '192.168.1.186')
    SERVER_PORT = int(os.getenv('IB_PORT', 5431))
    CLIENT_ID = int(os.getenv('IB_CLIENT_ID', 552614))
    SLEEP_TIME = 0.5
    WAIT_TIME = 3
    REQ_ID = 0

    def __init__(self):
        self.ib = IB()

    def connect(self):
        if not self.ib.isConnected():
            self.ib.connect(self.SERVER_IP, self.SERVER_PORT, clientId=self.CLIENT_ID)

    def handle_request(self, request_func, error_message):
        try:
            self.connect()
            result = pd.DataFrame(request_func())
            self.disconnect()
            return result
        except Exception as e:
            logging.error(f"{error_message}: {e}")
            return None

    def get_account(self, tag, currency):
        acc = self.handle_request(self.ib.accountSummary, "Error getting accountSummary")
        acc = acc[acc['tag'] == tag]
        acc = acc[acc['currency'] == currency]
        return acc

    def get_positions(self):
        positions = self.handle_request(self.ib.positions, "Error getting positions")
        positions['symbol'] = positions['contract'].apply(lambda x: x.symbol)
        positions = positions.rename(columns={'position': 'qty'})
        return positions

    def get_portfolio(self):
        return self.handle_request(self.ib.portfolio, "Error getting portfolio")

    def get_news(self):
        return self.handle_request(self.ib.newsTicks, "Error getting newsTicks")

    def submit_order(self, symbol, qty, side):
        return self.handle_request(lambda: self.ib.placeOrder(Stock(symbol, 'SMART', 'USD'),
                                                              MarketOrder(side, qty)),"Error submitting order")

    def disconnect(self):
        if self.ib.isConnected():
            self.ib.disconnect()