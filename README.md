# 📈 Nifty100 Analytics Platform

A complete financial analytics platform developed as part of the **Bluestock Fintech Data Analytics Internship**.

The project collects, validates, stores, analyzes, and visualizes financial data of Nifty100 companies using **Python, SQLite, Pandas, and Streamlit**.

---

# 🚀 Project Features

## Sprint 1 – Data Foundation

- Environment Setup
- ETL Pipeline
- Data Cleaning
- Data Normalization
- Data Validation
- SQLite Database Creation
- Automated Data Loading

---

## Sprint 2 – Financial Analytics

- Financial Ratio Calculations
- Revenue CAGR
- PAT CAGR
- EPS CAGR
- Composite Quality Score
- Financial KPI Engine
- Master Analytics Dataset

---

## Sprint 3 – Analytics & Reporting

- Stock Screener Engine
- Peer Group Analysis
- Peer Comparison Reports
- Radar Chart Generation
- Company Insights
- Data Quality Reports
- Excel Report Generation

---

## Sprint 4 – Interactive Dashboard

### 🏠 Dashboard Home

- Overall Market Summary
- Total Companies
- Sector Distribution
- Financial KPIs
- Interactive Charts

### 🏢 Company Profile

- Company Information
- ROE & ROCE
- Net Profit Margin
- Debt to Equity
- Revenue CAGR
- Free Cash Flow
- Sales vs Net Profit
- Balance Sheet Visualization
- Cash Flow Visualization
- AI Generated Pros & Cons

### 🔍 Stock Screener

- Sector Filter
- ROE Filter
- ROCE Filter
- Debt-to-Equity Filter
- Quality Score Filter
- Revenue CAGR Filter
- Free Cash Flow Filter
- CSV Export

---

## Sprint 5 – Profitability Intelligence

- Operating Margin Analysis
- Net Profit Margin Analysis
- Gross Profit Margin Analysis
- EBITDA Margin Analysis
- Return on Equity (ROE) Quality
- Return on Assets (ROA) Quality
- Return on Capital Employed (ROCE) Quality
- Interest Coverage Analysis
- PAT Growth Analysis
- EPS Growth Analysis
- Composite Profitability Score
- Earnings Quality Score
- Profitability Ranking
- Top & Bottom Company Ranking
- Excel Report Generation
- CSV Summary Report Export

---

# 🛠 Technologies Used

- Python
- Pandas
- NumPy
- SQLite
- SQLAlchemy
- Streamlit
- Plotly
- OpenPyXL
- Pytest
- Python-dotenv

---

# 📁 Project Structure

```text
nifty100-project/
│
├── config/
├── db/
├── docs/
├── output/
├── reports/
│
├── src/
│   │
│   ├── analytics/
│   │     ├── financial_analytics.py
│   │     └── profitability_kpis.py
│   │
│   ├── dashboard/
│   │     ├── app.py
│   │     ├── pages/
│   │     └── utils/
│   │
│   ├── data/
│   │
│   └── nlp/
│         ├── parser.py
│         └── pros_cons_generator.py
│
├── tests/
├── requirements.txt
├── README.md
└── Makefile
```

---

# ⚙ Installation

Clone the repository

```bash
git clone <repository-url>
```

Move into the project

```bash
cd nifty100-project
```

Create a virtual environment

```bash
python -m venv venv
```

Activate the virtual environment

### macOS / Linux

```bash
source venv/bin/activate
```

### Windows

```bash
venv\Scripts\activate
```

Install all dependencies

```bash
pip install -r requirements.txt
```

---

# ▶ Running the Dashboard

Launch the Streamlit dashboard

```bash
streamlit run src/dashboard/app.py
```

The dashboard will automatically open in your browser.

---

# 📊 Dashboard Pages

## 🏠 Home Dashboard

- Company Summary
- Market Overview
- Sector Analysis
- Financial KPIs
- Interactive Charts

---

## 🏢 Company Profile

- Company Information
- Financial Ratios
- Sales & Profit Trends
- Balance Sheet Analysis
- Cash Flow Analysis
- AI Generated Pros & Cons

---

## 🔍 Stock Screener

- Apply Financial Filters
- Interactive Search Results
- CSV Download

---

# 📈 Profitability Intelligence Reports

Sprint 5 generates the following reports:

- Profitability Intelligence Excel Report
- Profitability Summary CSV
- Operating Margin Analysis
- Net Profit Margin Analysis
- Gross Profit Margin Analysis
- EBITDA Margin Analysis
- ROE / ROA / ROCE Quality Analysis
- Interest Coverage Analysis
- PAT Growth Analysis
- EPS Growth Analysis
- Composite Profitability Score
- Earnings Quality Score
- Profitability Ranking

---

# 📦 Outputs

- SQLite Database
- Financial Analytics Reports
- Interactive Dashboard
- Company Profiles
- Stock Screener
- Peer Comparison Reports
- Profitability Intelligence Reports
- Excel Reports
- CSV Summary Reports
- Validation Reports

---

# 👨‍💻 Author

**Ayush Jha**

B.Tech Computer Science & Engineering (AI & ML)

MIT Academy of Engineering, Pune

Bluestock Fintech – Data Analytics Internship

---

# 📄 License

This project was developed for educational purposes as part of the Bluestock Fintech Data Analytics Internship.