BEGIN;
INSERT INTO symbols (exchange_id, symbol, name, country, ipoyear, sector, industry, last_updated_date, "marketCap", volume, url)
SELECT t.exchange_id, t.symbol, t.name, t.country, t.ipoyear, t.sector, t.industry, t.last_updated_date, CAST(NULLIF(t."marketCap", '') AS NUMERIC), CAST(NULLIF(t.volume, '') AS NUMERIC), t.url
FROM temporary_table AS t
ON CONFLICT (symbol) DO UPDATE SET
    name = EXCLUDED.name,
    country = EXCLUDED.country,
    sector = EXCLUDED.sector,
    industry = EXCLUDED.industry,
    ipoyear = EXCLUDED.ipoyear,
    "marketCap" = EXCLUDED."marketCap",
    volume = EXCLUDED.volume,
    url = EXCLUDED.url,
    exchange_id = EXCLUDED.exchange_id,
    last_updated_date = EXCLUDED.last_updated_date;
DROP TABLE temporary_table;
COMMIT;