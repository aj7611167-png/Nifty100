# 📈 Nifty100 Analytics Platform

A complete financial analytics platform developed as part of the **Bluestock Fintech Data Analytics Internship**.

The platform collects, validates, stores, analyzes, and visualizes financial data for **Nifty100 companies** using **Python, SQLite, Pandas, Streamlit, and FastAPI**.

The project follows a complete end-to-end data analytics workflow:

- Data Collection
- ETL Pipeline
- Data Cleaning
- Data Validation
- Financial Analytics
- KPI Generation
- Interactive Dashboard
- REST API Development
- Testing & Validation
- Performance Optimization

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

## Sprint 6 – API Platform & Advanced Analytics

Sprint 6 extends the project beyond analytics by introducing a complete REST API using FastAPI, automated testing, API documentation, and performance optimization.

### 🌐 REST API

- FastAPI-based REST API
- Modular API architecture
- SQLite backend integration
- JSON responses
- Automatic request validation
- Error handling
- Interactive API documentation

### 📡 API Endpoints

#### Health API

- Health Check Endpoint

#### Company APIs

- Company Profile
- Company Financial Data
- Company Analytics

#### Financial APIs

- Financial Ratios
- Market Capitalization
- Valuation Metrics
- Risk Metrics

#### Analytics APIs

- Stock Screener
- Sector Analysis
- Peer Group Analysis
- Portfolio Analytics

#### Document APIs

- Company Documents
- Pros & Cons
- Reports

### 🧪 Testing & Validation

- API Endpoint Testing
- ETL Validation Tests
- Data Quality Rule Tests
- KPI Validation Tests
- Pytest Test Suite
- HTML Test Report Generation

### ⚡ Performance Optimization

- SQLite Index Creation
- Query Optimization
- Faster API Response Time
- Database Performance Improvements

### 📚 Documentation

- OpenAPI Specification
- Swagger UI
- ReDoc Documentation
- Postman Collection

---

# 🛠 Technologies Used

## Programming Languages

- Python

## Database

- SQLite
- SQLAlchemy

## Data Processing

- Pandas
- NumPy

## Visualization

- Streamlit
- Plotly
- Matplotlib

## API Development

- FastAPI
- Uvicorn
- Starlette

## Testing

- Pytest

## File Processing

- OpenPyXL

## Utilities

- Python-dotenv
- Requests

---

# ✨ Key Features

- Automated ETL Pipeline
- Financial Analytics Engine
- KPI Calculation Engine
- Data Validation Framework
- SQLite Database
- Interactive Dashboard
- Company Profile Analysis
- Stock Screener
- Profitability Intelligence
- Peer Group Analysis
- REST API
- Swagger Documentation
- OpenAPI Support
- Automated Testing
- Performance Optimization
- Report Generation

---

# 📁 Project Structure

```text
nifty100-project/
│
├── config/
│
├── db/
│   ├── nifty100.db
│   └── schema.sql
│
├── docs/
│   ├── openapi.json
│   └── postman_collection.json
│
├── output/
│
├── reports/
│
├── src/
│   │
│   ├── api/
│   │   ├── database.py
│   │   ├── main.py
│   │   ├── routers/
│   │   └── schemas/
│   │
│   ├── analytics/
│   │
│   ├── dashboard/
│   │   ├── app.py
│   │   ├── pages/
│   │   └── utils/
│   │
│   ├── etl/
│   │
│   └── nlp/
│
├── tests/
│
├── requirements.txt
├── README.md
└── Makefile
```

---

# ⚙️ Installation

## Clone the Repository

```bash
git clone <repository-url>
```

Move into the project directory.

```bash
cd nifty100-project
```

---

## Create Virtual Environment

### macOS / Linux

```bash
python3 -m venv venv
```

### Windows

```bash
python -m venv venv
```

---

## Activate Virtual Environment

### macOS / Linux

```bash
source venv/bin/activate
```

### Windows

```bash
venv\Scripts\activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🗄 Database

The project uses **SQLite** as the primary database.

Database location:

```text
db/nifty100.db
```

The database stores information related to:

- Companies
- Financial Ratios
- Balance Sheets
- Profit & Loss Statements
- Cash Flow Statements
- Stock Prices
- Market Capitalization
- Documents
- Sector Information
- Peer Groups
- Peer Percentiles

---

# 📦 ETL Pipeline

The ETL process performs the following operations:

- Extract raw financial data
- Clean missing values
- Normalize records
- Validate data quality
- Load data into SQLite
- Generate analytics datasets

Run the ETL pipeline:

```bash
make load
```

or

```bash
python -m src.etl.load_all
```

---

# ✅ Data Validation

Validate the processed data:

```bash
make validate
```

or

```bash
python -m src.etl.validator
```

---

# 🔍 Database Check

Verify database integrity:

```bash
make check
```

or

```bash
python -m src.etl.check_db
```

---

# ▶️ Running the Dashboard

Launch the Streamlit dashboard:

```bash
make dashboard
```

or

```bash
streamlit run src/dashboard/app.py
```

The dashboard will automatically open in your default web browser.

---

# 🌐 Running the REST API

Start the FastAPI server using Uvicorn:

```bash
uvicorn src.api.main:app --reload
```

The API will be available at:

```
http://127.0.0.1:8000
```

---

# 📖 API Documentation

FastAPI automatically generates interactive API documentation.

## Swagger UI

```
http://127.0.0.1:8000/docs
```

Features:

- Interactive API Testing
- Request Validation
- Response Schemas
- Try-It-Out Functionality

---

## ReDoc

```
http://127.0.0.1:8000/redoc
```

Provides clean and structured API documentation for developers.

---

# 📡 Available API Endpoints

## Health

| Method | Endpoint | Description |
|----------|-------------------------|-----------------------------|
| GET | `/health` | API Health Check |

---

## Companies

| Method | Endpoint | Description |
|----------|------------------------------|-----------------------------|
| GET | `/companies` | List all companies |
| GET | `/companies/{company_id}` | Company profile |

---

## Financial Ratios

| Method | Endpoint | Description |
|----------|--------------------------------------|---------------------------|
| GET | `/financial-ratios/{company_id}` | Financial ratios |

---

## Market Capitalization

| Method | Endpoint | Description |
|----------|-----------------------------------|---------------------------|
| GET | `/market-cap/{company_id}` | Market capitalization |

---

## Valuation

| Method | Endpoint | Description |
|----------|-------------------------------|----------------------------|
| GET | `/valuation/{company_id}` | Company valuation metrics |

---

## Risk

| Method | Endpoint | Description |
|----------|-------------------------|----------------------------|
| GET | `/risk/{company_id}` | Risk analysis |

---

## Analytics

| Method | Endpoint | Description |
|----------|------------------------------|----------------------------|
| GET | `/analytics/{company_id}` | Company analytics |

---

## Portfolio

| Method | Endpoint | Description |
|----------|-----------------------------|----------------------------|
| GET | `/portfolio` | Portfolio statistics |

---

## Sector Analysis

| Method | Endpoint | Description |
|----------|------------------------------|----------------------------|
| GET | `/sectors` | Sector-wise analytics |

---

## Screener

| Method | Endpoint | Description |
|----------|------------------------------|----------------------------|
| GET | `/screener` | Stock screener |

---

## Documents

| Method | Endpoint | Description |
|----------|------------------------------|----------------------------|
| GET | `/documents/{company_id}` | Company documents |

---

## Peer Analysis

| Method | Endpoint | Description |
|----------|-------------------------------------------|----------------------------|
| GET | `/peers/group/{group_name}` | Peer group comparison |
| GET | `/peers/company/{company_id}` | Company peer analysis |

---

# 📊 Dashboard Pages

## 🏠 Home Dashboard

- Overall Market Summary
- Total Companies
- Sector Distribution
- Key Financial KPIs
- Interactive Charts
- Market Overview

---

## 🏢 Company Profile

- Company Information
- Financial Ratios
- Revenue Analysis
- Profit Analysis
- Balance Sheet
- Cash Flow
- Pros & Cons
- Performance Indicators

---

## 🔍 Stock Screener

- Financial Filters
- Sector Filters
- Quality Score
- ROE
- ROCE
- Debt-to-Equity
- Revenue CAGR
- Export Results

---

# 🧪 Testing

The project includes automated testing to ensure data accuracy, API reliability, and overall application stability.

## Test Categories

### API Tests

- Company APIs
- Financial Ratio APIs
- Screener APIs
- Sector APIs
- Peer APIs
- Portfolio APIs
- Analytics APIs
- Documents APIs
- Health API

### ETL Tests

- Data Loading Validation
- Data Cleaning Validation
- Database Validation

### Data Quality Tests

- Missing Value Checks
- Duplicate Record Detection
- Schema Validation
- Data Consistency Checks

### KPI Validation

- Revenue CAGR
- PAT CAGR
- EPS CAGR
- ROE
- ROCE
- Debt-to-Equity
- Profitability Score
- Quality Score

---

## Running Tests

Execute all test cases:

```bash
make test
```

or

```bash
pytest -v
```

Generate an HTML report:

```bash
pytest --html=reports/pytest_report.html
```

---

# ⚡ Performance Optimization

Several optimizations have been implemented to improve database performance and API response times.

## Database Optimization

- SQLite Index Creation
- Query Optimization
- Reduced Query Execution Time
- Optimized Table Joins
- Improved Search Performance

Run index creation:

```bash
python -m src.etl.create_indexes
```

---

# 📊 Reports Generated

The platform generates multiple reports during execution.

## Financial Reports

- Financial Analytics Report
- Profitability Intelligence Report
- Peer Comparison Report

## Validation Reports

- Data Quality Report
- Validation Failure Report
- Database Integrity Report

## Testing Reports

- Pytest HTML Report
- API Test Results

---

# 📂 Output Files

Generated files are stored inside the following directories.

## Output

```text
output/
```

Contains:

- CSV Exports
- Analytics Results
- Summary Files

---

## Reports

```text
reports/
```

Contains:

- Excel Reports
- HTML Test Reports
- Performance Notes

---

## Documentation

```text
docs/
```

Contains:

- OpenAPI Specification
- Postman Collection

---

# 📬 API Testing

The REST API can be tested using:

- Swagger UI
- ReDoc
- Postman
- cURL
- Web Browser (GET Endpoints)

Example:

```bash
curl http://127.0.0.1:8000/api/v1/companies
```

---

# 📈 Performance Highlights

- Optimized SQLite Queries
- Indexed Database Tables
- Modular FastAPI Architecture
- RESTful API Design
- Automated Testing Pipeline
- Comprehensive API Documentation
- Efficient ETL Processing
- Scalable Project Structure

---

# 🔄 Project Workflow

The Nifty100 Analytics Platform follows a complete end-to-end data analytics pipeline.

```text
Raw Financial Data
        │
        ▼
Data Extraction
        │
        ▼
Data Cleaning
        │
        ▼
Data Validation
        │
        ▼
Data Normalization
        │
        ▼
SQLite Database
        │
        ▼
Financial Analytics
        │
        ▼
Profitability Intelligence
        │
        ▼
Peer Group Analysis
        │
        ▼
REST API Services
        │
        ▼
Interactive Dashboard
        │
        ▼
Reports & Visualizations
```

---

# 🛠️ Technologies Used

## Programming Languages

- Python
- SQL

## Database

- SQLite

## Backend Framework

- FastAPI
- Uvicorn

## Data Processing

- Pandas
- NumPy

## Data Visualization

- Plotly
- Matplotlib
- Streamlit

## Testing

- Pytest

## Database ORM

- SQLAlchemy

## File Handling

- OpenPyXL

## Environment Management

- Python-dotenv

---

# 🚀 Sprint Summary

## ✅ Sprint 1 – Data Foundation

- Environment Setup
- ETL Pipeline
- Data Cleaning
- Data Validation
- SQLite Database Design
- Automated Data Loading

---

## ✅ Sprint 2 – Financial Analytics

- Financial KPI Engine
- Revenue CAGR
- PAT CAGR
- EPS CAGR
- Composite Quality Score
- Master Analytics Dataset

---

## ✅ Sprint 3 – Analytics & Reporting

- Peer Group Analysis
- Company Comparison
- Radar Charts
- Excel Reports
- Data Quality Reports
- Company Insights

---

## ✅ Sprint 4 – Interactive Dashboard

- Streamlit Dashboard
- Company Profile
- Stock Screener
- Financial Charts
- Market Overview
- Interactive Visualizations

---

## ✅ Sprint 5 – Profitability Intelligence

- Operating Margin Analysis
- Net Profit Margin
- Gross Profit Margin
- EBITDA Margin
- ROE Analysis
- ROA Analysis
- ROCE Analysis
- Interest Coverage
- Profitability Ranking
- Earnings Quality Score

---

## ✅ Sprint 6 – REST API & Testing

- FastAPI Backend
- REST API Endpoints
- Company APIs
- Financial Ratio APIs
- Screener APIs
- Sector APIs
- Portfolio APIs
- Analytics APIs
- Peer APIs
- Automated API Testing
- Data Quality Validation
- Database Performance Optimization
- SQLite Indexing
- OpenAPI Documentation
- Swagger UI
- ReDoc
- Postman Collection

---

# 📌 Key Features

- Complete ETL Pipeline
- Automated Data Validation
- SQLite Database
- Financial KPI Engine
- Profitability Intelligence
- Peer Group Analytics
- Interactive Dashboard
- RESTful API
- Automated Testing
- Database Optimization
- API Documentation
- Exportable Reports
- Modular Project Architecture

---

# 🔮 Future Enhancements

Potential improvements for future versions include:

- User Authentication & Authorization
- Portfolio Watchlists
- Live Stock Market Data Integration
- AI-Based Stock Recommendations
- Predictive Analytics using Machine Learning
- Docker Containerization
- CI/CD Pipeline Integration
- Cloud Deployment (AWS, Azure, or GCP)
- PostgreSQL/MySQL Support
- Role-Based Access Control (RBAC)

---

# 📈 Project Highlights

- End-to-End Financial Analytics Platform
- Modular and Scalable Architecture
- Automated ETL Pipeline
- Interactive Streamlit Dashboard
- High-Performance REST APIs
- Comprehensive Testing Suite
- Production-Ready Project Structure
- Clean and Maintainable Codebase

---

# 🤝 Contributing

Contributions are welcome.

If you would like to improve this project:

1. Fork the repository
2. Create a feature branch

```bash
git checkout -b feature-name
```

3. Commit your changes

```bash
git commit -m "Add new feature"
```

4. Push the branch

```bash
git push origin feature-name
```

5. Open a Pull Request

---

# 📌 Repository Structure

```text
src/
├── analytics/
├── api/
├── dashboard/
├── data/
├── etl/
├── models/
├── nlp/
├── reports/
└── utils/

tests/
├── api/
├── etl/
└── analytics/

docs/
output/
reports/
db/
config/
```

---

# 📄 License

This project was developed for educational purposes as part of the **Bluestock Fintech Data Analytics Internship**.

Feel free to use the project for learning and educational purposes.

---

# 🙏 Acknowledgements

Special thanks to:

- Bluestock Fintech
- Internship Mentors
- Open Source Python Community
- FastAPI Community
- Streamlit Community
- Pandas & NumPy Contributors

---

# 👨‍💻 Author

**Ayush Jha**

**B.Tech – Computer Science & Engineering (AI & ML)**

MIT Academy of Engineering (MITAOE), Pune

Bluestock Fintech – Data Analytics Internship

### Connect

- GitHub: https://github.com/aj7611167-png
- LinkedIn: *(Add your LinkedIn profile here if available)*

---

# ⭐ Project Status

✅ Sprint 1 Completed

✅ Sprint 2 Completed

✅ Sprint 3 Completed

✅ Sprint 4 Completed

✅ Sprint 5 Completed

✅ Sprint 6 Completed

---

# 📬 Contact

For questions, suggestions, or collaboration, feel free to reach out through GitHub.

---

# ⭐ Support

If you found this project useful, consider giving the repository a **⭐ Star** on GitHub.

It helps others discover the project and supports future development.

---

## Thank You!

Thank you for exploring the **Nifty100 Analytics Platform**.

Happy Coding! 🚀