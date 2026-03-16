import numpy as np
import psycopg2
import random

from unidecode import unidecode

first_names = [
    "Jacob",
    "Augustin",
    "Peter",
    "Leonhard",
    "Évariste",
    "David",
    "Henri",
    "Andrei",
    "Bernhard",
    "Karl",
    "Marie",
    "Rosa",
    "Margaret",
    "Florence",
    "Marie",
    "Jeanne",
    "Simone",
    "Frida",
    "Catherine",
    "Elizabeth",
]

last_names = [
    "Bernoulli",
    "Cauchy",
    "Dirichlet",
    "Euler",
    "Galois",
    "Hilbert",
    "Lebesgue",
    "Markov",
    "Riemann",
    "Weierstrass",
    "Curie",
    "Parks",
    "Thatcher",
    "Nightingale",
    "Antoinette",
    "Shelly",
    "d'Arc",
    "de Beauvoir",
    "Kalo",
    "de Medici",
]

email_providers = [
    "gmail.com",
    "outlook.com",
    "yahoo.com",
    "icloud.com",
]

country_codes = ["CA", "FR", "DE", "US"]

currencies = {"CA": "CAD", "FR": "EUR", "DE": "EUR", "US": "USD"}

NUM_USERS = 50


def make_user_email(first_name, last_name, i):
    """
    Makes a random email for the user.

    Args:
        first_name (str): User's first name.
        last_name (str): User's last name.
        i (int): Index used to help generate a unique email address for the user.
    """
    bad_chars = [" ", "'", "-", "."]

    provider = random.choice(email_providers)

    email = f"{first_name}{last_name}{i}@{provider}"

    for char in bad_chars:
        email = email.replace(char, "")

    return unidecode(email.lower())


def create_user_record(cursor, i):
    """
    Creates a user records in the database.

    Args:
        cursor: A database cursor object used to execute SQL queries.
        i (int): Index used to help generate a unique email address for the user.
    """

    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    email_address = make_user_email(first_name, last_name, i)
    country_code = random.choice(country_codes)
    currency_code = currencies[country_code]
    balance = round(random.lognormvariate(np.log(2000), 1), 4)

    cursor.execute(
        """
        INSERT INTO Records.Users (email_address, first_name, last_name, country_code)
        VALUES (%s, %s, %s, %s) RETURNING user_id;
        """,
        (email_address, first_name, last_name, country_code),
    )

    user_id = cursor.fetchone()[0]
    cursor.execute(
        """
        INSERT INTO Records.Accounts (user_id, currency_code, balance)
        VALUES (%s, %s, %s);
        """,
        (user_id, currency_code, balance),
    )


def seed_db():
    """
    Connects to the database and populates user and account tables.
    """
    random.seed(1021)
    connection = None
    try:
        connection = psycopg2.connect(
            user="philiploewen",
            password="",
            host="127.0.0.1",
            port="5432",
            database="Fintech",
        )

        cursor = connection.cursor()

        for i in range(NUM_USERS):
            create_user_record(cursor, i)

        connection.commit()
        print(f"Successfully seeded {NUM_USERS} users and accounts.")
    except psycopg2.Error as e:
        print(f"A database error occurred: {e}")
        if connection:
            connection.rollback()
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Connection closed.")


if __name__ == "__main__":
    seed_db()
