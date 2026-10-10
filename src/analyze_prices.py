from pathlib import Path

import pandas as pd

# Find the project folder.
project_root = Path(__file__).resolve().parents[1]

# Load the electricity price data.
data_path = project_root / "data" / "raw" / "germany_day_ahead_prices.csv"
df = pd.read_csv(data_path)
df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True).dt.tz_convert("Europe/Berlin")

# Remove observations without a recorded price.
df = df.dropna(subset=["price_eur_mwh"])

# Display basic statistics.
print("\n=== ELECTRICITY MARKET OVERVIEW ===")
print(f"Observations: {len(df):,}")
print(f"Average price: €{df['price_eur_mwh'].mean():.2f}/MWh")
print(f"Median price: €{df['price_eur_mwh'].median():.2f}/MWh")
print(f"Standard deviation: €{df['price_eur_mwh'].std():.2f}/MWh")

# Identify the 10 highest-price intervals.
highest = df.nlargest(10, "price_eur_mwh")

print("\n=== 10 HIGHEST-PRICE INTERVALS ===")
print(highest[["timestamp", "price_eur_mwh"]].to_string(index=False))

# Identify the 10 lowest-price intervals.
lowest = df.nsmallest(10, "price_eur_mwh")

print("\n=== 10 LOWEST-PRICE INTERVALS ===")
print(lowest[["timestamp", "price_eur_mwh"]].to_string(index=False))

# Count negative-price intervals.
negative_prices = df[df["price_eur_mwh"] < 0]

print("\n=== NEGATIVE-PRICE ANALYSIS ===")
print(f"Negative-price intervals: {len(negative_prices):,}")
print(f"Percentage of observations: {len(negative_prices) / len(df) * 100:.2f}%")

# === DAILY PRICE ANALYSIS ===

df["date"] = df["timestamp"].dt.date

daily = df.groupby("date").agg(
    average_price=("price_eur_mwh", "mean"),
    minimum_price=("price_eur_mwh", "min"),
    maximum_price=("price_eur_mwh", "max"),
    negative_intervals=(
        "price_eur_mwh",
        lambda prices: (prices < 0).sum()
    ),
    observations=("price_eur_mwh", "count")
).reset_index()

print("\n=== 10 DAYS WITH HIGHEST MAXIMUM PRICE ===")
print(
    daily.nlargest(10, "maximum_price")[
        ["date", "maximum_price", "average_price", "negative_intervals"]
    ].to_string(index=False)
)

print("\n=== 10 DAYS WITH LOWEST MINIMUM PRICE ===")
print(
    daily.nsmallest(10, "minimum_price")[
        ["date", "minimum_price", "average_price", "negative_intervals"]
    ].to_string(index=False)
)

print("\n=== DAILY DATA QUALITY CHECK ===")
print(f"Number of days: {len(daily)}")
print(f"Minimum observations per day: {daily['observations'].min()}")
print(f"Maximum observations per day: {daily['observations'].max()}")
# === TIMESTAMP QUALITY CHECK ===

df = df.sort_values("timestamp")

time_differences = df["timestamp"].diff()

print("\n=== TIMESTAMP QUALITY CHECK ===")
print(f"Duplicate timestamps: {df['timestamp'].duplicated().sum()}")
print("\nMost common time differences:")
print(time_differences.value_counts().head(10))

print("\nDays with fewer than 96 observations:")
print(
    daily[daily["observations"] < 96][
        ["date", "observations"]
    ].to_string(index=False)
)

print("\nDays with more than 96 observations:")
print(
    daily[daily["observations"] > 96][
        ["date", "observations"]
    ].to_string(index=False)
)
# === INVESTIGATE 1 MAY 2026 ===

event_day = df[
    df["timestamp"].dt.strftime("%Y-%m-%d") == "2026-05-01"
].copy()

print("\n=== 1 MAY 2026: PRICE EVENT ===")
print(f"Observations: {len(event_day)}")
print(f"Average price: €{event_day['price_eur_mwh'].mean():.2f}/MWh")
print(f"Minimum price: €{event_day['price_eur_mwh'].min():.2f}/MWh")
print(f"Maximum price: €{event_day['price_eur_mwh'].max():.2f}/MWh")
print(
    f"Negative-price intervals: "
    f"{(event_day['price_eur_mwh'] < 0).sum()}"
)

print("\nLowest-price intervals:")
print(
    event_day.nsmallest(10, "price_eur_mwh")[
        ["timestamp", "price_eur_mwh"]
    ].to_string(index=False)
)
# === INVESTIGATE EXTREME NEGATIVE PRICES ===

event = df[
    (df["timestamp"].dt.strftime("%Y-%m-%d") == "2026-05-01")
    & (df["price_eur_mwh"] <= -400)
]

print("\n=== EXTREME NEGATIVE-PRICE INTERVALS ===")
print(event[["timestamp", "price_eur_mwh"]].to_string(index=False))

print("\nNumber of intervals at or below -€400/MWh:", len(event))
print("Distinct prices in these intervals:")
print(sorted(event["price_eur_mwh"].unique()))
# === EXTREME PRICE EVENT SUMMARY ===

event_day = df[
    df["timestamp"].dt.strftime("%Y-%m-%d") == "2026-05-01"
].copy()

negative = event_day[event_day["price_eur_mwh"] < 0]
extreme = event_day[event_day["price_eur_mwh"] <= -400]

print("\n=== COMMERCIAL EVENT SUMMARY ===")
print("Market: Germany-Luxembourg day-ahead electricity")
print("Delivery date: 1 May 2026")
print(f"Average daily price: €{event_day['price_eur_mwh'].mean():.2f}/MWh")
print(f"Minimum price: €{event_day['price_eur_mwh'].min():.2f}/MWh")
print(f"Maximum price: €{event_day['price_eur_mwh'].max():.2f}/MWh")
print(f"Negative-price intervals: {len(negative)}")
print(f"Negative-price duration: {len(negative) * 15 / 60:.2f} hours")
print(f"Intervals at or below -€400/MWh: {len(extreme)}")
print(
    "Duration at or below -€400/MWh: "
    f"{len(extreme) * 15 / 60:.2f} hours"
)