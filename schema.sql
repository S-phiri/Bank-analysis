DROP TABLE IF EXISTS bank_customers;

CREATE TABLE bank_customers (
    customer_id   INTEGER PRIMARY KEY,
    age           INTEGER,
    income        REAL,
    account_type  TEXT,
    balance       REAL,
    tenure_years  REAL,
    churned       INTEGER,
    branch        TEXT
);
