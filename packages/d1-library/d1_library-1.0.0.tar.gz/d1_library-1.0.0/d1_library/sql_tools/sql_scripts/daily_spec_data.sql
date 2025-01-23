SELECT date, symbol, close
FROM daily_data
WHERE date between '{start}' AND '{end}'
AND symbol {condition} {symbol}