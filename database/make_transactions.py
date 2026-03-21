import numpy as np
import pandas as pd
import psycopg2
import random

from sqlalchemy import create_engine, text


def get_accounts_data(engine):
    """
    Retrieve all accounts data from the database.
    Args:
        engine: A database connection engine used to execute the SQL query.
    Returns:
        pd.DataFrame: A DataFrame containing all columns and rows from the
                      Records.Accounts table.
    """

    get_accounts_data_query = """
    SELECT *
    FROM Records.Accounts
    """

    df = pd.read_sql(get_accounts_data_query, engine)

    return df


def generate_transation(engine, accounts):
    """
    Generates a random transaction between two accounts in the dataframe

    Args:
        engine: A database connection engine used to execute the SQL query.
        accounts (list): A list of all account IDs
    """
    sender_receiver = random.sample(accounts, 2)
    sender = sender_receiver[0]
    receiver = sender_receiver[1]

    amount = round(random.lognormvariate(np.log(300), 0.8), 4)

    try:
        send_funds(engine, sender, receiver, amount)

    except ValueError as e:
        print(f"An error has occured: {e}")


def send_funds(engine, sender, receiver, amount):
    """
    Sends the funds from the senders count to the receivers account

    Args:
        engine: A database connection engine used to execute the SQL query.
        sender (UUID): Sender account UUID.
        receiver (UUID): receiver account UUID.
        amount (float): Amount to transfer.
    """

    send_funds_query = """
    WITH Currencies AS (
        SELECT 
            (SELECT currency_code FROM Records.Accounts WHERE account_id = :sender) as src,
            (SELECT currency_code FROM Records.Accounts WHERE account_id = :receiver) as tgt
            ),
    Rate AS (
        SELECT COALESCE(
                (SELECT exchange_rate FROM Records.ExchangeRates 
                WHERE source_currency = (SELECT src FROM Currencies) 
                AND target_currency = (SELECT tgt FROM Currencies)),
                1.0
            ) as factor
        ),
    Debit AS (
        UPDATE Records.Accounts
        SET balance = balance - :amount
        WHERE account_id = :sender AND balance >= :amount
        RETURNING account_id
    ),
    LogTransaction AS (
        INSERT INTO Records.Transactions (
            sender_account_id, 
            receiver_account_id, 
            base_amount, 
            source_currency,
            target_currency,
            exchange_rate
        )
        SELECT 
            :sender, 
            :receiver, 
            :amount,
            (SELECT src FROM Currencies),
            (SELECT tgt FROM Currencies), 
            (SELECT factor FROM Rate)
        WHERE EXISTS (SELECT 1 FROM Debit)
    )   
    
    UPDATE Records.Accounts
    SET balance = balance + (:amount * (SELECT factor FROM Rate))
    WHERE account_id = :receiver
    AND EXISTS (SELECT 1 FROM Debit);
    """
    with engine.begin() as conn:
        conn.execute(
            text(send_funds_query),
            {"sender": sender, "receiver": receiver, "amount": amount},
        )


if __name__ == "__main__":
    random.seed(1021)
    try:
        engine = create_engine(
            "postgresql+psycopg2://philiploewen:@localhost:5432/Fintech"
        )

        accounts_data = get_accounts_data(engine)
        account_ids = accounts_data["account_id"].to_list()

        for _ in range(50000):
            generate_transation(engine, account_ids)

    except psycopg2.Error as e:
        print(f"A database error occurred: {e}")
