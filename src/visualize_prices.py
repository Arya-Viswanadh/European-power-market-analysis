from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

# Locate project files
project_root = Path(__file__).resolve().parents[1]

data_path = (
    project_root
    / "data"
    / "raw"
    / "germany_day_ahead_prices.csv"
)

output_dir = project_root / "outputs"
output_dir.mkdir(exist_ok=True)

# Load and prepare data
df = pd.read_csv(data_path)
df["timestamp"] = pd.to_datetime(
    df["timestamp"], utc=True
).dt.tz_convert("Europe/Berlin")

df = df.dropna(subset=["price_eur_mwh"])
df = df.sort_values("timestamp")

# Calculate daily statistics
df["date"] = df["timestamp"].dt.date

daily = df.groupby("date").agg(
    average_price=("price_eur_mwh", "mean"),
    minimum_price=("price_eur_mwh", "min"),
    maximum_price=("price_eur_mwh", "max"),
).reset_index()

# Plot daily average prices
plt.figure(figsize=(14, 6))

plt.plot(
    daily["date"],
    daily["average_price"],
    linewidth=1,
    label="Daily average price",
)

plt.axhline(
    0,
    linestyle="--",
    linewidth=1,
    label="Zero-price reference",
)

plt.title("German-Luxembourg Electricity Prices")
plt.xlabel("Date")
plt.ylabel("Price (€/MWh)")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()

# Save chart
chart_path = output_dir / "daily_average_prices.png"
plt.savefig(chart_path, dpi=200)
plt.close()

print(f"Chart saved to: {chart_path}")
# === DAILY PRICE EXTREMES ===

plt.figure(figsize=(14, 6))

plt.plot(
    daily["date"],
    daily["maximum_price"],
    label="Daily maximum",
    linewidth=1,
)

plt.plot(
    daily["date"],
    daily["minimum_price"],
    label="Daily minimum",
    linewidth=1,
)

plt.axhline(0, linestyle="--", linewidth=1)

plt.title("Daily Maximum and Minimum Electricity Prices")
plt.xlabel("Date")
plt.ylabel("Price (€/MWh)")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()

extremes_path = output_dir / "daily_price_extremes.png"
plt.savefig(extremes_path, dpi=200)
plt.close()

print(f"Extremes chart saved to: {extremes_path}")
# === INTRADAY PRICE EVENT: 1 MAY 2026 ===

event_day = df[
    df["timestamp"].dt.strftime("%Y-%m-%d") == "2026-05-01"
].copy()

plt.figure(figsize=(12, 5))

plt.plot(
    event_day["timestamp"],
    event_day["price_eur_mwh"],
    linewidth=1.5,
    marker=".",
    markersize=3,
)

plt.axhline(0, linestyle="--", linewidth=1)

plt.title("German-Luxembourg Electricity Prices — 1 May 2026")
plt.xlabel("Time (Europe/Berlin)")
plt.ylabel("Price (€/MWh)")
plt.xticks(rotation=30)
plt.grid(True, alpha=0.3)
plt.tight_layout()

event_path = output_dir / "negative_price_event_2026_05_01.png"
plt.savefig(event_path, dpi=200)
plt.close()

print(f"Event chart saved to: {event_path}")