"""
import alpaca_trade_api as alpaca_api
import pandas as pd
from DoneStorage.credentials.secrets import alpaca_cred


class AlpacaTrader:
    def __init__(self):
        try:
            self.api = alpaca_api.REST(alpaca_cred.get('key_id'),
                                       alpaca_cred.get('secret_key'),
                                       alpaca_cred.get('base_url'),
                                       'v2')
        except Exception as e:
            print(f"Error initializing AlpacaTrader: {e}")

    def get_positions_data(self, include_avg_entry_price=False):
        positions = self.api.list_positions()
        if include_avg_entry_price:
            data = [(p.symbol, int(p.qty), float(p.avg_entry_price), float(p.market_value)) for p in positions]
            columns = ['symbol', 'qty', 'avg_entry_price', 'market_value']
        else:
            data = [(p.symbol, int(p.qty), float(p.market_value)) for p in positions]
            columns = ['symbol', 'qty', 'market_value']
        return pd.DataFrame(data, columns=columns)

    def submit_order(self, symbol, qty, side):
        if side not in ['buy', 'sell']:
            raise ValueError("Invalid order side. Must be 'buy' or 'sell'.")
        self.api.submit_order(symbol=symbol, qty=qty, side=side, type='market', time_in_force='day')
"""