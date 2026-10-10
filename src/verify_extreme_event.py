import requests
import pandas as pd

url = "https://api.energy-charts.info/price"

params = {
    "bzn": "DE-LU",
    "start": "2026-05-01",
    "end": "2026-05-02",
}

print("Requesting original market data...")

response = requests.get(url, params=params, timeout=30)
response.raise_for_status()

data = response.json()

df = pd.DataFrame({
    "timestamp": pd.to_datetime(
        data["unix_seconds"],
        unit="s",
        utc=True
    ).tz_convert("Europe/Berlin"),
    "price_eur_mwh": data["price"],
})

print("\n=== API VERIFICATION ===")
print(f"Observations returned: {len(df)}")
print(f"Minimum price: €{df['price_eur_mwh'].min():.2f}/MWh")
print(f"Maximum price: €{df['price_eur_mwh'].max():.2f}/MWh")

print("\n=== PRICES AT OR BELOW -€400/MWh ===")

extreme = df[df["price_eur_mwh"] <= -400]

if extreme.empty:
    print("No intervals at or below -€400/MWh were returned.")
else:
    print(extreme.to_string(index=False))
