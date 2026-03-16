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
        check_sufficient_balance(engine, sender, amount)

        send_funds(engine, sender, receiver, amount)

        record_transaction(engine, sender, receiver, amount)
    except ValueError as e:
        print(f"An error has occured: {e}")


def check_sufficient_balance(engine, sender, amount):
    """
    Verifies that the sender has the required funds for the transfer.

    Args:
        engine: A database connection engine used to execute the SQL query.
        sender (UUID): Sender account UUID.
        amount (float): Amount to transfer.
    """
    get_accounts_data_query = """
    SELECT CASE
           WHEN balance >= :amount THEN TRUE
                ELSE FALSE
           END AS fund_status
    FROM Records.Accounts
    WHERE account_id = :sender
    """
    cond = pd.read_sql_query(
        text(get_accounts_data_query),
        engine,
        params={"sender": sender, "amount": amount},
    )

    if not cond.iloc[0, 0]:
        raise ValueError("Not enough funds.")


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
    UPDATE Records.Accounts
    SET balance = balance - :amount
    WHERE account_id = :sender;
    
    UPDATE Records.Accounts
    SET balance = balance + :amount
    WHERE account_id = :receiver;
    """

    with engine.begin() as conn:
        conn.execute(
            text(send_funds_query),
            {"sender": sender, "receiver": receiver, "amount": amount},
        )


def record_transaction(engine, sender, receiver, amount):
    """
    Records transaction in transactions table.

    Args:
        engine: A database connection engine used to execute the SQL query.
        sender (UUID): Sender account UUID.
        receiver (UUID): receiver account UUID.
        amount (float): Amount transfered.
    """

    record_transaction_query = """
    INSERT INTO Records.Transactions (sender_account_id, receiver_account_id, amount)
    VALUES (:sender, :receiver, :amount);
    """

    with engine.begin() as conn:
        conn.execute(
            text(record_transaction_query),
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

        for _ in range(500):
            generate_transation(engine, account_ids)

    except psycopg2.Error as e:
        print(f"A database error occurred: {e}")
