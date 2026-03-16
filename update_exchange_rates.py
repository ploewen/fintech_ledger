import json
import requests

from decimal import Decimal
from sqlalchemy import create_engine, text


def update_all_exchange_rates(engine):
    supported_currencies = ["USD", "EUR", "CAD"]

    query = text("""
        INSERT INTO Records.ExchangeRates (source_currency, target_currency, exchange_rate, last_updated)
        VALUES (:source, :target, :rate, CURRENT_TIMESTAMP)
        ON CONFLICT (source_currency, target_currency) 
        DO UPDATE SET 
            exchange_rate = EXCLUDED.exchange_rate,
            last_updated = EXCLUDED.last_updated;
    """)

    with engine.begin() as conn:
        for base in supported_currencies:
            url = f"https://api.frankfurter.app/latest?from={base}"
            response = json.loads(requests.get(url).text, parse_float=Decimal)
            rates = response.get("rates", {})

            for target, rate in rates.items():
                if target in supported_currencies:
                    conn.execute(
                        query, {"source": base, "target": target, "rate": rate}
                    )
            print(f"Updated rates with {base} as base currency.")


if __name__ == "__main__":
    engine = create_engine("postgresql+psycopg2://philiploewen:@localhost:5432/Fintech")
    update_all_exchange_rates(engine)
