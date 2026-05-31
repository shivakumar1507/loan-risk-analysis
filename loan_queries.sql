-- ============================================================
-- Loan Portfolio Risk Analysis — SQL Queries
-- Dataset : loan_cleaned.csv (output from Python script)
-- Author  : Shiva Kumar Devatha
-- DB      : SQL Server / PostgreSQL / MySQL compatible
-- ============================================================

-- ── SETUP: Create Table ─────────────────────────────────────
-- Run this first to create the table after importing the CSV

CREATE TABLE loan_data (
    loan_amnt        DECIMAL(12,2),
    funded_amnt      DECIMAL(12,2),
    term             INT,
    int_rate         DECIMAL(5,2),
    installment      DECIMAL(10,2),
    grade            VARCHAR(5),
    sub_grade        VARCHAR(5),
    emp_length       VARCHAR(20),
    emp_length_num   INT,
    home_ownership   VARCHAR(20),
    annual_inc       DECIMAL(15,2),
    verification_status VARCHAR(30),
    loan_status      VARCHAR(80),
    purpose          VARCHAR(50),
    addr_state       VARCHAR(5),
    dti              DECIMAL(8,2),
    open_acc         INT,
    total_pymnt      DECIMAL(12,2),
    total_rec_prncp  DECIMAL(12,2),
    total_rec_int    DECIMAL(12,2),
    recoveries       DECIMAL(12,2),
    is_default       INT,
    risk_tier        VARCHAR(20),
    dti_band         VARCHAR(10),
    income_band      VARCHAR(15),
    recovery_rate    DECIMAL(8,2),
    emp_stable       INT,
    high_income      INT,
    issue_year       INT,
    issue_month      INT
);


-- ============================================================
-- QUERY 1: Overall Portfolio Summary (KPI Cards in Power BI)
-- ============================================================
SELECT
    COUNT(*)                                        AS total_loans,
    ROUND(SUM(loan_amnt) / 1000000.0, 2)           AS total_disbursed_M,
    ROUND(AVG(loan_amnt), 2)                        AS avg_loan_amount,
    ROUND(AVG(int_rate), 2)                         AS avg_interest_rate,
    ROUND(SUM(is_default) * 100.0 / COUNT(*), 2)   AS default_rate_pct,
    ROUND(AVG(dti), 2)                              AS avg_dti,
    ROUND(SUM(total_pymnt) / 1000000.0, 2)         AS total_repaid_M,
    ROUND(SUM(recoveries) / 1000000.0, 2)          AS total_recovered_M
FROM loan_data;


-- ============================================================
-- QUERY 2: Default Rate by Loan Grade
-- (Bar chart — Risk Analysis page)
-- ============================================================
SELECT
    grade,
    COUNT(*)                                        AS total_loans,
    SUM(is_default)                                 AS defaults,
    ROUND(SUM(is_default) * 100.0 / COUNT(*), 2)   AS default_rate_pct,
    ROUND(AVG(int_rate), 2)                         AS avg_interest_rate,
    ROUND(AVG(loan_amnt), 2)                        AS avg_loan_amount
FROM loan_data
GROUP BY grade
ORDER BY grade;


-- ============================================================
-- QUERY 3: Default Rate by Loan Purpose
-- (Horizontal bar chart — Risk Analysis page)
-- ============================================================
SELECT
    purpose,
    COUNT(*)                                        AS total_loans,
    SUM(is_default)                                 AS defaults,
    ROUND(SUM(is_default) * 100.0 / COUNT(*), 2)   AS default_rate_pct,
    ROUND(AVG(loan_amnt), 2)                        AS avg_loan_amount
FROM loan_data
GROUP BY purpose
ORDER BY default_rate_pct DESC;


-- ============================================================
-- QUERY 4: Monthly Loan Disbursement Trend
-- (Line chart — Portfolio Trends page)
-- ============================================================
SELECT
    issue_year,
    issue_month,
    printf(
        '%04d-%02d',
        issue_year,
        issue_month
    ) AS year_month,
    COUNT(*) AS loan_count,
    ROUND(
        SUM(loan_amnt) / 1000000.0,
        2
    ) AS disbursed_M,
    ROUND(
        SUM(is_default) * 100.0 / COUNT(*),
        2
    ) AS default_rate_pct
FROM loan_data
WHERE issue_year IS NOT NULL
GROUP BY issue_year, issue_month
ORDER BY issue_year, issue_month;


-- ============================================================
-- QUERY 5: State-wise Loan Performance
-- (Map visual — Portfolio Trends page)
-- ============================================================
SELECT
    addr_state                                       AS state,
    COUNT(*)                                         AS total_loans,
    ROUND(SUM(loan_amnt) / 1000000.0, 2)            AS total_disbursed_M,
    ROUND(SUM(is_default) * 100.0 / COUNT(*), 2)    AS default_rate_pct,
    ROUND(AVG(annual_inc), 2)                        AS avg_income
FROM loan_data
WHERE addr_state IS NOT NULL
GROUP BY addr_state
ORDER BY total_loans DESC;


-- ============================================================
-- QUERY 6: Employment Stability vs Default Rate
-- (Key insight query — for storytelling)
-- ============================================================
SELECT
    grade,
    CASE WHEN emp_stable = 1 THEN 'Stable (5+ yrs)'
         ELSE 'Unstable (<5 yrs)' END               AS employment_stability,
    COUNT(*)                                         AS total_loans,
    ROUND(SUM(is_default) * 100.0 / COUNT(*), 2)    AS default_rate_pct,
    ROUND(AVG(loan_amnt), 2)                         AS avg_loan_amount
FROM loan_data
GROUP BY grade, emp_stable
ORDER BY grade, emp_stable DESC;


-- ============================================================
-- QUERY 7: Income Band vs Default Rate
-- (Matrix visual — Risk Analysis page)
-- ============================================================
SELECT
    income_band,
    risk_tier,
    COUNT(*)                                         AS total_loans,
    ROUND(SUM(is_default) * 100.0 / COUNT(*), 2)    AS default_rate_pct,
    ROUND(AVG(dti), 2)                               AS avg_dti
FROM loan_data
WHERE income_band IS NOT NULL
GROUP BY income_band, risk_tier
ORDER BY income_band, risk_tier;


-- ============================================================
-- QUERY 8: DTI Band Analysis
-- (Bar chart — Risk Analysis page)
-- ============================================================
SELECT
    dti_band,
    COUNT(*)                                         AS total_loans,
    ROUND(SUM(is_default) * 100.0 / COUNT(*), 2)    AS default_rate_pct,
    ROUND(AVG(loan_amnt), 2)                         AS avg_loan_amount,
    ROUND(AVG(int_rate), 2)                          AS avg_interest_rate
FROM loan_data
WHERE dti_band IS NOT NULL
GROUP BY dti_band
ORDER BY dti_band;


-- ============================================================
-- QUERY 9: Top 10 High-Risk Segments
-- (Table visual — Executive Summary page)
-- ============================================================
SELECT TOP 10
    grade,
    purpose,
    dti_band,
    COUNT(*)                                         AS loan_count,
    ROUND(SUM(is_default) * 100.0 / COUNT(*), 2)    AS default_rate_pct,
    ROUND(AVG(loan_amnt), 2)                         AS avg_loan_amount
FROM loan_data
GROUP BY grade, purpose, dti_band
HAVING COUNT(*) > 100
ORDER BY default_rate_pct DESC;


-- ============================================================
-- QUERY 10: Recovery Rate by Risk Tier
-- (KPI / gauge — Executive Summary page)
-- ============================================================
SELECT
    risk_tier,
    COUNT(*)                                         AS defaulted_loans,
    ROUND(AVG(recovery_rate), 2)                     AS avg_recovery_rate_pct,
    ROUND(SUM(recoveries) / 1000000.0, 2)            AS total_recovered_M
FROM loan_data
WHERE is_default = 1
GROUP BY risk_tier
ORDER BY avg_recovery_rate_pct DESC;

-- ============================================================
-- QUERY 11: States Above Portfolio Average Default Rate
-- (CTE Example)
-- ============================================================

WITH portfolio_avg AS (
    SELECT AVG(is_default * 100.0) AS avg_default_rate
    FROM loan_data
)

SELECT
    addr_state,
    COUNT(*) AS total_loans,
    ROUND(AVG(is_default) * 100, 2) AS default_rate_pct
FROM loan_data
GROUP BY addr_state
HAVING AVG(is_default) * 100 >
(
    SELECT avg_default_rate
    FROM portfolio_avg
)
ORDER BY default_rate_pct DESC;

-- ============================================================
-- QUERY 12: Top Loan Purpose Within Each Grade
-- (Window Function Example)
-- ============================================================

WITH purpose_rank AS (

    SELECT
        grade,
        purpose,
        COUNT(*) AS total_loans,

        RANK() OVER(
            PARTITION BY grade
            ORDER BY COUNT(*) DESC
        ) AS purpose_rank

    FROM loan_data
    GROUP BY grade, purpose
)

SELECT *
FROM purpose_rank
WHERE purpose_rank = 1
ORDER BY grade;

-- ============================================================
-- QUERY 13: Month-over-Month Loan Growth
-- ============================================================

WITH monthly_loans AS (

    SELECT
        issue_year,
        issue_month,
        COUNT(*) AS loan_count
    FROM loan_data
    GROUP BY issue_year, issue_month
)

SELECT
    issue_year,
    issue_month,
    loan_count,

    LAG(loan_count) OVER(
        ORDER BY issue_year, issue_month
    ) AS previous_month_loans,

    ROUND(
        (
            loan_count -
            LAG(loan_count) OVER(
                ORDER BY issue_year, issue_month
            )
        ) * 100.0
        /
        NULLIF(
            LAG(loan_count) OVER(
                ORDER BY issue_year, issue_month
            ),
            0
        ),
        2
    ) AS mom_growth_pct

FROM monthly_loans
ORDER BY issue_year, issue_month;
