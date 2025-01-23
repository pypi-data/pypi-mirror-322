BEGIN;
INSERT INTO daily_data (symbol, open, high, low, close, volume, date, u_key, data_vendor_id, stock_id)
SELECT t.symbol, t.open, t.high, t.low, t.close, t.volume, t.date, t.u_key, t.data_vendor_id, t.stock_id
FROM temporary_table AS t
ON CONFLICT (u_key) DO UPDATE SET
    symbol = EXCLUDED.symbol,
    open = EXCLUDED.open,
    high = EXCLUDED.high,
    low = EXCLUDED.low,
    close = EXCLUDED.close,
    volume = EXCLUDED.volume,
    date = EXCLUDED.date,
    data_vendor_id = EXCLUDED.data_vendor_id,
    stock_id = EXCLUDED.stock_id;
DROP TABLE temporary_table;
COMMIT;



