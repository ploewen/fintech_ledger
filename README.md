# Fintech Ledger Simulator

![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white) ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

This project demonstrates the implementation of a relational database schema in PostgreSQL and a data-seeding pipeline in Python that models realistic financial behavior.

## Key Features

- Relational Schema Design: I have implemented a multi-table structure with strict data integrity, including foreign key constraints and custom PostgreSQL functions for automatic account number generation.

- Realistic Seeding: To generate user balances I have utilized Log-Normal distributions to simulate real-world wealth inequality, moving beyond basic uniform random generation.

## Tech Stack
- Database: PostgreSQL
- Language: Python3.13
- Libraries: psycopg2-binary (Postgres driver), random (Statistical modelling)
- GUI: DBeaver

## Database Analysis

A comprehensive analysis of the fintech platform's financial database has been conducted to examine critical operational metrics. The analysis (`analysis/db_analysis.ipynb`) includes:

### Key Analysis Areas

1. **High-Value Customer Identification** - Identifies accounts with the largest balances on the platform, essential for understanding wealth concentration and customer segmentation strategies.

2. **Geographic Distribution of Wealth** - Analyzes average account balances by country to identify regional market opportunities and purchasing power variations.

3. **Transaction Activity Analysis** - Examines transaction patterns including:
   - Total transaction participation (inbound + outbound transfers)
   - Network hub identification based on unique recipient reach
   - Cross-border transaction leaders

4. **Exchange Rate Integrity Assessment** - Evaluates the platform's multi-currency capabilities by identifying triangular arbitrage opportunities, revealing that current exchange rate precision (5 decimal places) permits modest but material inefficiencies (~0.01-0.02% variation per dollar).

### Key Findings

- **Wealth Concentration**: Platform demonstrates successful acquisition of high-value users with significant geographic variation in average balances
- **Activity Patterns**: Complete inter-user connectivity in test data reveals robust transaction processing; production systems will exhibit more realistic clustering patterns
- **International Reach**: Cross-border transactions represent a distinct strategic category, particularly important for revenue generation and regulatory compliance
- **Risk Management**: Exchange rate precision gaps present the most urgent operational vulnerability requiring immediate remediation through increased decimal precision or real-time rate updating

## Repository Structure

```
fintech/
├── pyproject.toml                     # Project configuration
├── README.md                          # This file
├── analysis/ 
│   └── db_analysis.ipynb              # Comprehensive financial analysis report
└── databse/
    ├── make_schema.sql                # Database schema definition
    ├── make_transactions.py           # Transaction generation script
    ├── populate_db.py                 # Database population pipeline
    └── update_exchange_rates.py       # Exchange rate management utility

```