import yfinance as yf
from datetime import datetime
import pytz


class YahooFinanceFetcher:
    def __init__(self):
        pass

    def is_market_open(self, symbol='AAPL'):
        stock = yf.Ticker(symbol)
        hist = stock.history(period="1d")

        if hist.empty:
            print('Не удалось получить данные о состоянии рынка.')
            return False

        last_trading_time = hist.index[-1].astimezone(pytz.timezone("America/New_York"))
        now = datetime.now(pytz.timezone("America/New_York"))

        # Проверка, если последняя торговая дата совпадает с сегодняшней датой
        if last_trading_time.date() == now.date():
            return True
        else:
            print('Рынок закрыт')
            return False
