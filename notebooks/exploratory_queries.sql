-- Query 1
SELECT COUNT(*) FROM companies;

-- Query 2
SELECT COUNT(*) FROM stock_prices;

-- Query 3
SELECT company_name
FROM companies
LIMIT 10;

-- Query 4
SELECT company_id, MAX(year)
FROM profitandloss
GROUP BY company_id;

-- Query 5
SELECT company_id, SUM(net_profit)
FROM profitandloss
GROUP BY company_id
ORDER BY SUM(net_profit) DESC
LIMIT 10;

-- Query 6
SELECT company_id, market_cap_crore
FROM market_cap
ORDER BY market_cap_crore DESC
LIMIT 10;

-- Query 7
SELECT broad_sector, COUNT(*)
FROM sectors
GROUP BY broad_sector;

-- Query 8
SELECT AVG(return_on_equity_pct)
FROM financial_ratios;

-- Query 9
SELECT company_id, close_price
FROM stock_prices
ORDER BY close_price DESC
LIMIT 10;

-- Query 10
SELECT company_id, debt_to_equity
FROM financial_ratios
ORDER BY debt_to_equity DESC
LIMIT 10;