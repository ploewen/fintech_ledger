CREATE SCHEMA Records;

CREATE FUNCTION Records.gen_account_number()
RETURNS VARCHAR(12) AS $$
-- Generates an account ID for a user.
BEGIN
    RETURN lpad(floor(random()*10^12)::VARCHAR, 12, '0');
END;
$$ LANGUAGE plpgsql;

CREATE TABLE Records.Users (
    user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email_address VARCHAR(255) UNIQUE NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    kyc_status VARCHAR(20) DEFAULT 'Pending',
    country_code CHAR(2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOL DEFAULT TRUE
);

CREATE TABLE Records.Accounts (
    account_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES Records.Users(user_id) ON DELETE CASCADE,
    account_number VARCHAR(12) UNIQUE NOT NULL DEFAULT Records.gen_account_number(),
    currency_code CHAR(3) NOT NULL,
    balance DEC(19, 4) NOT NULL DEFAULT 0.0000,
    pending_balance DEC(19, 4) NOT NULL DEFAULT 0.0000,
    account_status VARCHAR(20) DEFAULT 'Active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT positive_balance CHECK (balance >= 0)
);

CREATE TABLE Records.Transactions (
    transaction_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    sender_account_id UUID NOT NULL REFERENCES Records.Accounts(account_id),
    receiver_account_id UUID NOT NULL REFERENCES Records.Accounts(account_id),
    base_amount DEC(19, 4) NOT NULL,
    source_currency CHAR(3) NOT NULL,
    target_currency CHAR(3) NOT NULL,
    exchange_rate DEC(19, 9) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT positive_amount CHECK (base_amount > 0)
);

CREATE TABLE Records.ExchangeRates (
    source_currency CHAR(3) NOT NULL,
    target_currency CHAR(3) NOT NULL,
    exchange_rate DEC(19, 9) NOT NULL,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (source_currency, target_currency)
)