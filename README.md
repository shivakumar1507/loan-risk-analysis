# Lending Club Loan Portfolio Analytics Dashboard

### Credit Risk & Portfolio Performance Analysis using Python, SQL & Power BI

An end-to-end analytics project that simulates a real-world lending portfolio monitoring solution. This project leverages Lending Club loan data to analyze borrower behavior, portfolio performance, default risk drivers, recovery rates, and geographic lending trends through data engineering, SQL analytics, and interactive Power BI reporting.

---

## Project Overview

Financial institutions must continuously monitor loan portfolios to identify emerging credit risks, improve underwriting decisions, and optimize portfolio performance.

This project demonstrates how raw lending data can be transformed into actionable business insights through:

* Data cleaning and feature engineering using Python
* Portfolio analysis using SQL
* Interactive executive dashboards using Power BI
* Credit risk assessment and borrower segmentation
* Business storytelling through data visualization

---

## Business Questions

This analysis aims to answer:

* Which borrower segments exhibit the highest default risk?
* How do loan grade, income, employment history, and debt burden affect repayment behavior?
* Which loan purposes contribute the most risk to the portfolio?
* How has lending activity evolved over time?
* Which states represent the largest exposure concentrations?
* What percentage of defaulted loans is ultimately recovered?

---

## Dataset

**Source:** Lending Club Loan Dataset (Kaggle)

**Domain:** Banking, Financial Services & Insurance (BFSI)

**Records Analyzed:** 225,000+ Loans

**Portfolio Value:** $3.37 Billion

The dataset contains borrower demographics, loan characteristics, repayment history, credit information, and recovery metrics.

---

## Technology Stack

| Tool                   | Purpose                                 |
| ---------------------- | --------------------------------------- |
| Python (Pandas, NumPy) | Data Cleaning & Feature Engineering     |
| SQL (SQLite)           | Portfolio Analytics & Risk Queries      |
| Power BI               | Dashboard Development                   |
| DAX                    | KPI & Business Measure Creation         |
| GitHub                 | Project Documentation & Version Control |

---

## Project Architecture

```text
Loan-Portfolio-Risk-Dashboard/
│
├── data/
│   └── loan_cleaned.csv
│
├── python/
│   └── loan_cleaning.py
│
├── sql/
│   └── loan_queries.sql
│
├── powerbi/
│   ├── loan_dashboard.pbix
│   └── loan_dax_measures.dax
│
├── screenshots/
│   ├── executive_summary.png
│   ├── risk_analysis.png
│   └── portfolio_trends.png
│
└── README.md
```

---

## Data Engineering & Feature Creation

### Data Cleaning

* Removed duplicates
* Handled missing values
* Standardized categorical fields
* Converted date fields
* Corrected data types

### Feature Engineering

Created several business-focused analytical fields:

| Feature       | Description                             |
| ------------- | --------------------------------------- |
| is_default    | Defaulted loan indicator                |
| risk_tier     | Low / Medium / High risk classification |
| dti_band      | Debt-to-income segmentation             |
| income_band   | Borrower income segmentation            |
| recovery_rate | Recovery percentage after charge-off    |
| emp_stable    | Employment stability flag               |
| high_income   | High-income borrower flag               |

---

## SQL Analysis

Developed analytical queries covering:

* Portfolio KPI Summary
* Default Rate by Grade
* Default Rate by Purpose
* DTI Risk Analysis
* Income Band Analysis
* Employment Stability Impact
* Recovery Rate by Risk Tier
* Geographic Portfolio Performance
* Monthly Disbursement Trends
* High-Risk Segment Identification

---

## Power BI Dashboard

### Page 1 — Executive Summary

Executive-level overview of portfolio performance.

Includes:

* Total Loans
* Total Disbursed Amount
* Default Rate
* Recovery Rate
* Interest Rate Analysis
* Risk Tier Distribution
* High-Risk Segment Summary

---

### Page 2 — Credit Risk Analysis

Focused analysis of borrower and portfolio risk.

Includes:

* Default Rate by Grade
* Default Rate by Loan Purpose
* Income vs Risk Matrix
* Debt-to-Income Analysis
* Employment Stability Comparison
* Risk Segmentation Insights

---

### Page 3 — Portfolio Trends & Geographic Analysis

Portfolio growth and exposure monitoring.

Includes:

* Loan Volume Trends
* Default Rate Trends
* State-Level Exposure Analysis
* Loan Purpose Evolution
* Portfolio Growth Monitoring

---

## Key Business Insights

### Credit Risk Insights

* Grade G loans exhibit a default rate of approximately 40%, compared to approximately 3% for Grade A loans, confirming loan grade as the strongest default predictor.
* Borrowers with higher debt-to-income ratios demonstrate significantly higher default probabilities.
* Employment stability correlates strongly with repayment performance.
* High-risk loan segments contribute disproportionately to portfolio losses.

### Portfolio Insights

* Debt Consolidation remains the dominant loan purpose across the portfolio.
* Portfolio disbursement volume increased significantly over time while maintaining relatively stable default rates.
* Geographic exposure is concentrated in a limited number of states, increasing concentration risk.
* Recovery rates remain low, highlighting the importance of proactive risk management.

---

## Skills Demonstrated

* Data Cleaning & Transformation
* Exploratory Data Analysis
* Feature Engineering
* SQL Query Development
* Credit Risk Analytics
* Business Intelligence Reporting
* DAX Measures
* Dashboard Design
* Data Storytelling
* BFSI Domain Analytics

---

## Dashboard Screenshots

### Executive Summary

<img width="1351" height="753" alt="Executive Summary" src="https://github.com/user-attachments/assets/7f5be87d-a42f-4ef4-a8dd-2d66e5e34392" />

### Credit Risk Analysis

<img width="1374" height="746" alt="Credit Risk Analysis" src="https://github.com/user-attachments/assets/77be1f62-ab66-4261-836b-b81aa38bdc0e" />


### Portfolio Trends & Geographic Analysis

<img width="1370" height="739" alt="Portfolio Trends   Geographic Analysis" src="https://github.com/user-attachments/assets/808224f7-bbb0-40e2-8002-fb5ef061a431" />


---

## How to Run

1. Download Lending Club Loan Dataset from Kaggle
2. Run `loan_cleaning.py`
3. Generate `loan_cleaned.csv`
4. Execute SQL analysis queries
5. Load data into Power BI
6. Import DAX measures
7. Refresh dashboard

---

## Author

### Shiva Kumar Devatha

Data Analyst | SQL | Power BI | Python | ETL | BFSI Analytics

GitHub: https://github.com/shivakumar1507

LinkedIn: [https://linkedin.com/in/shivakumardevatha](https://www.linkedin.com/in/contact-shivakumar/)
