# Sprint 1 Report

## Objective

Build ETL pipeline for Nifty100 financial dataset.

---

## Data Sources

Total Files: 12

1. companies.xlsx
2. profitandloss.xlsx
3. balancesheet.xlsx
4. cashflow.xlsx
5. analysis.xlsx
6. documents.xlsx
7. prosandcons.xlsx
8. sectors.xlsx
9. stock_prices.xlsx
10. financial_ratios.xlsx
11. peer_groups.xlsx
12. market_cap.xlsx

---

## Database

SQLite Database:

db/nifty100.db

---

## Tables Loaded

| Table | Rows |
|---------|---------|
| companies | 92 |
| profitandloss | 1276 |
| balancesheet | 1312 |
| cashflow | 1187 |
| analysis | 20 |
| documents | 1585 |
| prosandcons | 16 |
| sectors | 92 |
| stock_prices | 5520 |
| financial_ratios | 1184 |
| peer_groups | 56 |
| market_cap | 552 |

---

## Data Quality Checks

Performed:

- Duplicate Check
- Null Value Check
- Row Count Validation

Result:

No duplicate rows found.

Null values identified and documented for further cleaning.

---

## Status

Sprint 1 Completed Successfully.