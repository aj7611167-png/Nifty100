# Nifty100 Analytics Platform

A complete data analytics platform developed as part of the **Bluestock Fintech Data Analytics Internship**.

## Project Overview

The project analyzes Nifty100 companies by collecting, cleaning, validating, storing, and analyzing financial data. It provides stock screening, peer comparison, radar charts, and company insights using Python and SQLite.

---

# Sprint 1 - Data Foundation

- Environment setup
- ETL pipeline
- Data ingestion
- Data normalization
- Data quality validation
- SQLite database creation
- Automated data loading

---

# Sprint 2 - Financial Analytics

- Financial ratio calculations
- CAGR calculations
- Quality score generation
- Financial KPIs
- Company scoring engine
- Screener engine
- Master dataframe creation

---

# Sprint 3 - Analytics & Reporting

- Stock Screener
- Peer Group Analysis
- Peer Comparison Excel Report
- Radar Chart Generation
- Company Insights
- Data Quality Report
- Excel Export with Formatting

---

## Technologies Used

- Python
- Pandas
- SQLite
- OpenPyXL
- Matplotlib

---

## Project Structure

```
config/
db/
docs/
output/
reports/
src/
```

---

## Installation

Create a virtual environment:

```bash
python -m venv venv
```

Activate it:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Running the Project

Run Screener:

```bash
python -m src.analytics.screener
```

Run Peer Comparison:

```bash
python -m src.analytics.export_peer_excel
```

Generate Radar Charts:

```bash
python -m src.analytics.radar
```

Generate Company Reports:

```bash
python -m src.analytics.report
```

---

## Outputs

- SQLite Database
- Validation Reports
- Screener Output (Excel)
- Peer Comparison Workbook
- Radar Charts
- Company Insights
- Data Quality Report

---

## Author

**Ayush Jha**

Bluestock Fintech Internship