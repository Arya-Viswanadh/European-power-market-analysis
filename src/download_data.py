from pathlib import Path

import pandas as pd
import requests


# 1. Choose the German-Luxembourg electricity market.
BIDDING_ZONE = "DE-LU"

# 2. Request approximately one year of historical prices.
END_DATE = pd.Timestamp.now().date()
START_DATE = END_DATE - pd.Timedelta(days=365)

# 3. Build the API request.
url = "https://api.energy-charts.info/price"

params = {
    "bzn": BIDDING_ZONE,
    "start": START_DATE.isoformat(),
    "end": END_DATE.isoformat(),
}

print("Downloading electricity price data...")

response = requests.get(url, params=params, timeout=30)
response.raise_for_status()

data = response.json()

# 4. Check that price data was returned.
if not data.get("unix_seconds") or not data.get("price"):
    raise ValueError("The API returned no electricity price data.")

if len(data["unix_seconds"]) != len(data["price"]):
    raise ValueError("The timestamps and prices have different lengths.")

# 5. Create a structured table.
df = pd.DataFrame({
    "timestamp": pd.to_datetime(
        data["unix_seconds"],
        unit="s",
        utc=True
    ).tz_convert("Europe/Berlin"),
    "price_eur_mwh": data["price"],
})

# 6. Clean the data.
df = df.dropna(subset=["price_eur_mwh"])
df = df.sort_values("timestamp")
df = df.drop_duplicates(subset=["timestamp"])

# 7. Save the dataset in our project.
project_root = Path(__file__).resolve().parents[1]
output_path = project_root / "data" / "raw" / "germany_day_ahead_prices.csv"

output_path.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(output_path, index=False)

# 8. Display a summary.
print("\nDownload successful!")
print(f"Market: {BIDDING_ZONE}")
print(f"Period: {START_DATE} to {END_DATE}")
print(f"Observations: {len(df):,}")
print(f"Average price: €{df['price_eur_mwh'].mean():.2f}/MWh")
print(f"Minimum price: €{df['price_eur_mwh'].min():.2f}/MWh")
print(f"Maximum price: €{df['price_eur_mwh'].max():.2f}/MWh")
print(f"\nSaved to: {output_path}")
print(f"Data source: {data.get('license_info', 'Energy-Charts API')}")