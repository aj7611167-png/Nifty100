# 📈 Nifty100 Analytics Platform

A complete financial analytics platform developed as part of the **Bluestock Fintech Data Analytics Internship**.

The project collects, validates, stores, analyzes, and visualizes financial data of Nifty100 companies using Python, SQLite, and Streamlit.

---

# 🚀 Project Features

## Sprint 1 – Data Foundation

- Environment setup
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
- Peer Comparison Excel Report
- Radar Chart Generation
- Company Insights
- Data Quality Report
- Excel Export

---

## Sprint 4 – Interactive Dashboard

### Dashboard Home

- Overall Market Summary
- Total Companies
- Sector Distribution
- Financial KPIs
- Interactive Charts

### Company Profile

- Company Information
- ROE & ROCE
- Net Profit Margin
- Debt to Equity
- Revenue CAGR
- Free Cash Flow
- Sales vs Net Profit
- Balance Sheet Charts
- Cash Flow Charts
- Pros & Cons

### Stock Screener

- Sector Filter
- ROE Filter
- ROCE Filter
- Debt/Equity Filter
- Quality Score Filter
- Revenue CAGR Filter
- Free Cash Flow Filter
- Download Results as CSV

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

```
nifty100-project/
│
├── config/
├── db/
├── docs/
├── output/
├── reports/
├── src/
│   ├── analytics/
│   ├── dashboard/
│   │   ├── app.py
│   │   ├── pages/
│   │   └── utils/
│   └── data/
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

Create virtual environment

```bash
python -m venv venv
```

Activate virtual environment

### macOS/Linux

```bash
source venv/bin/activate
```

### Windows

```bash
venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# ▶ Running the Dashboard

Launch Streamlit Dashboard

```bash
streamlit run src/dashboard/app.py
```

The dashboard opens automatically in your browser.

---

# 📊 Dashboard Pages

## 🏠 Home Dashboard

- Company Summary
- Financial Overview
- Sector Analysis

---

## 🏢 Company Profile

- Company Information
- Financial Metrics
- Sales & Profit Charts
- Balance Sheet
- Cash Flow
- Pros & Cons

---

## 🔎 Stock Screener

- Apply Financial Filters
- Interactive Results
- CSV Download

---

# 📦 Outputs

- SQLite Database
- Financial Analytics
- Dashboard
- Company Profiles
- Stock Screener
- Peer Comparison Reports
- Validation Reports
- CSV Export

---

# 👨‍💻 Author

**Ayush Jha**

B.Tech CSE (AI & ML)

MIT Academy of Engineering, Pune

Bluestock Fintech – Data Analytics Internship

---

# 📄 License

This project was developed for educational purposes as part of the Bluestock Fintech Internship.