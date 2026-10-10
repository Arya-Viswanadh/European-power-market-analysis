# European Electricity Market Analysis

## Overview

This project analyses German-Luxembourg day-ahead electricity prices using Python and real market data from the Energy-Charts API.

The goal is to identify price extremes, negative-price periods, and potentially useful patterns in electricity markets, then translate the results into commercially relevant insights.

## Questions Explored

- What are the typical and extreme electricity prices over the study period?
- How frequently do negative prices occur?
- When do unusually high or low prices appear?
- What can intraday price movements tell us about market conditions?

## Data

- **Market:** Germany-Luxembourg bidding zone (DE-LU)
- **Period:** 10 October 2025 – 10 October 2026
- **Source:** Energy-Charts API
- **Observations:** 35,136 price intervals
- **Time interval:** 15 minutes, as inferred from the timestamps
- **Price unit:** EUR/MWh

The data contains daylight-saving-time changes, so some local calendar days contain fewer or more than 96 observations.

## Key Findings

- Average observed price: approximately €106.00/MWh.
- Median observed price: approximately €105.29/MWh.
- Standard deviation: approximately €63.87/MWh.
- Negative prices occurred in 1,904 intervals, approximately 5.42% of observations.
- The highest observed interval price was €747.10/MWh.
- The lowest observed interval price was -€499.99/MWh.

These are descriptive statistics for the downloaded dataset, not trading recommendations.

## Case Study: Negative Prices on 1 May 2026

On 1 May 2026, the daily average price was approximately -€2.08/MWh.

- Minimum price: -€499.99/MWh.
- Maximum price: €232.99/MWh.
- Negative-price intervals: 32, equivalent to 8 hours of intervals.
- Intervals at or below -€400/MWh: 10, equivalent to 2.5 hours of intervals.

The intraday chart illustrates how prices varied throughout the day. These observations identify an event worth investigating; explaining its causes would require additional evidence about generation, demand, weather, and market conditions.

## Visualisations

The project generates:

- `outputs/daily_average_prices.png` — daily average prices.
- `outputs/daily_price_extremes.png` — daily minimum and maximum prices.
- `outputs/negative_price_event_2026_05_01.png` — intraday prices on 1 May 2026.

## Project Structure

```text
European-power-market-analysis/
├── data/
│   ├── raw/
│   └── processed/
├── outputs/
├── src/
│   ├── download_data.py
│   ├── analyze_prices.py
│   ├── market_analysis.py
│   └── visualize_prices.py
├── MARKET_INSIGHTS.md
└── README.md