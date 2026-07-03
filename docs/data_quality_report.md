# Data Quality Report

## Project

Nifty100 Data Foundation

## Database Validation Summary

### Tables Loaded

* companies
* profitandloss
* balancesheet
* cashflow
* analysis
* documents
* prosandcons
* sectors
* stock_prices
* financial_ratios
* peer_groups
* market_cap

### Data Quality Checks

#### Duplicate Records

All tables checked.

Result:

* Duplicate Rows = 0

#### Null Value Review

Observed null values in:

* companies
* profitandloss
* cashflow
* documents
* prosandcons
* financial_ratios

Severity:

WARNING

No critical failures found.

#### Foreign Key Integrity

Result:

PASS

#### Primary Key Integrity

Result:

PASS

### Database Statistics

| Table            | Rows |
| ---------------- | ---- |
| companies        | 92   |
| profitandloss    | 1276 |
| balancesheet     | 1312 |
| cashflow         | 1187 |
| analysis         | 20   |
| documents        | 1585 |
| prosandcons      | 16   |
| sectors          | 92   |
| stock_prices     | 5520 |
| financial_ratios | 1184 |
| peer_groups      | 56   |
| market_cap       | 552  |

### Conclusion

All source files were successfully loaded into SQLite.

No duplicate records were detected.

No critical data quality issues were identified.

Database is ready for downstream analytics and reporting.
