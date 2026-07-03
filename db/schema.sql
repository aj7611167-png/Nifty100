CREATE TABLE IF NOT EXISTS "companies" (
"id" TEXT,
  "company_logo" TEXT,
  "company_name" TEXT,
  "chart_link" TEXT,
  "about_company" TEXT,
  "website" TEXT,
  "nse_profile" TEXT,
  "bse_profile" TEXT,
  "face_value" REAL,
  "book_value" REAL,
  "roce_percentage" REAL,
  "roe_percentage" REAL
);
CREATE TABLE IF NOT EXISTS "profitandloss" (
"id" INTEGER,
  "company_id" TEXT,
  "year" TEXT,
  "sales" INTEGER,
  "expenses" INTEGER,
  "operating_profit" REAL,
  "opm_percentage" REAL,
  "other_income" INTEGER,
  "interest" INTEGER,
  "depreciation" INTEGER,
  "profit_before_tax" INTEGER,
  "tax_percentage" REAL,
  "net_profit" INTEGER,
  "eps" REAL,
  "dividend_payout" REAL
);
CREATE TABLE IF NOT EXISTS "balancesheet" (
"id" INTEGER,
  "company_id" TEXT,
  "year" TEXT,
  "equity_capital" REAL,
  "reserves" INTEGER,
  "borrowings" INTEGER,
  "other_liabilities" INTEGER,
  "total_liabilities" INTEGER,
  "fixed_assets" INTEGER,
  "cwip" INTEGER,
  "investments" INTEGER,
  "other_asset" INTEGER,
  "total_assets" INTEGER
);
CREATE TABLE IF NOT EXISTS "cashflow" (
"id" INTEGER,
  "company_id" TEXT,
  "year" TEXT,
  "operating_activity" REAL,
  "investing_activity" REAL,
  "financing_activity" REAL,
  "net_cash_flow" REAL
);
CREATE TABLE IF NOT EXISTS "analysis" (
"id" INTEGER,
  "company_id" TEXT,
  "compounded_sales_growth" TEXT,
  "compounded_profit_growth" TEXT,
  "stock_price_cagr" TEXT,
  "roe" TEXT
);
CREATE TABLE IF NOT EXISTS "documents" (
"id" INTEGER,
  "company_id" TEXT,
  "Year" INTEGER,
  "Annual_Report" TEXT
);
CREATE TABLE IF NOT EXISTS "prosandcons" (
"id" INTEGER,
  "company_id" TEXT,
  "pros" TEXT,
  "cons" TEXT
);
CREATE TABLE IF NOT EXISTS "sectors" (
"id" INTEGER,
  "company_id" TEXT,
  "broad_sector" TEXT,
  "sub_sector" TEXT,
  "index_weight_pct" REAL,
  "market_cap_category" TEXT
);
CREATE TABLE IF NOT EXISTS "stock_prices" (
"id" INTEGER,
  "company_id" TEXT,
  "date" TEXT,
  "open_price" REAL,
  "high_price" REAL,
  "low_price" REAL,
  "close_price" REAL,
  "volume" INTEGER,
  "adjusted_close" REAL
);
CREATE TABLE IF NOT EXISTS "financial_ratios" (
"id" INTEGER,
  "company_id" TEXT,
  "year" TEXT,
  "net_profit_margin_pct" REAL,
  "operating_profit_margin_pct" REAL,
  "return_on_equity_pct" REAL,
  "debt_to_equity" REAL,
  "interest_coverage" REAL,
  "asset_turnover" REAL,
  "free_cash_flow_cr" REAL,
  "capex_cr" REAL,
  "earnings_per_share" REAL,
  "book_value_per_share" REAL,
  "dividend_payout_ratio_pct" REAL,
  "total_debt_cr" INTEGER,
  "cash_from_operations_cr" REAL
);
CREATE TABLE IF NOT EXISTS "peer_groups" (
"id" INTEGER,
  "peer_group_name" TEXT,
  "company_id" TEXT,
  "is_benchmark" INTEGER
);
CREATE TABLE IF NOT EXISTS "market_cap" (
"id" INTEGER,
  "company_id" TEXT,
  "year" INTEGER,
  "market_cap_crore" REAL,
  "enterprise_value_crore" REAL,
  "pe_ratio" REAL,
  "pb_ratio" REAL,
  "ev_ebitda" REAL,
  "dividend_yield_pct" REAL
);
