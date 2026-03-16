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