import requests
from sqlalchemy import text


def update_exchange_rates(engine, base_currency="USD"):
    url = f"https://api.frankfurter.app/latest?from={base_currency}"
    response = requests.get(url).json()

    rates = response.get("rates", {})

    # Prepare the UPSERT query
    query = text("""
        INSERT INTO Records.ExchangeRates (source_currency, target_currency, exchange_rate, last_updated)
        VALUES (:source, :target, :rate, CURRENT_TIMESTAMP)
        ON CONFLICT (source_currency, target_currency) 
        DO UPDATE SET 
            exchange_rate = EXCLUDED.exchange_rate,
            last_updated = EXCLUDED.last_updated;
    """)

    with engine.begin() as conn:
        for target, rate in rates.items():
            conn.execute(
                query, {"source": base_currency, "target": target, "rate": rate}
            )
    print(f"Successfully updated {len(rates)} currency pairs.")
