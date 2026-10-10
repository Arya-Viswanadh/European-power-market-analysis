# European Power Market Analysis
### German-Luxembourg Day-Ahead Electricity Prices

## 1. Project Objective

This project analyses electricity-price behaviour in the German-Luxembourg bidding zone, focusing on price distributions, negative-price intervals, extreme price movements and potential commercial implications.

The objective is to demonstrate practical skills in Python-based data analysis, market monitoring, quantitative reasoning and communicating findings relevant to electricity trading.

## 2. Data and Methodology

- Market: German-Luxembourg bidding zone (DE-LU)
- Period: 10 October 2025–10 October 2026
- Frequency: 15-minute intervals
- Observations: 35,136
- Tools: Python, pandas, NumPy and Matplotlib

The analysis calculates descriptive statistics, identifies extreme prices, measures the frequency of negative prices, aggregates prices by delivery date and checks timestamp consistency.

The number of observations per local day varies because of European daylight-saving-time changes.

## 3. Market Overview

| Metric | Result |
|---|---:|
| Mean price | €106.00/MWh |
| Median price | €105.29/MWh |
| Standard deviation | €63.87/MWh |
| Maximum observed price | €747.10/MWh |
| Minimum observed price | −€499.99/MWh |
| Negative-price intervals | 1,904 |
| Share of negative-price intervals | 5.42% |

The observed minimum and maximum demonstrate substantial price extremes. Negative prices occur often enough in this sample to merit dedicated analysis.

## 4. Case Study: 1 May 2026

| Metric | Result |
|---|---:|
| Average daily price | −€2.08/MWh |
| Minimum price | −€499.99/MWh |
| Maximum price | €232.99/MWh |
| Negative-price intervals | 32 of 96 |
| Duration with negative prices | 8 hours |
| Intervals at or below −€400/MWh | 10 |
| Duration at or below −€400/MWh | 2.5 hours |

The lowest prices occurred between 12:45 and 15:00 local time. Five consecutive intervals recorded a price of −€499.99/MWh.

This illustrates why intraday price distributions can reveal important market behaviour that daily averages alone may conceal.

## 5. Potential Commercial Interpretation

Negative prices can occur when electricity supply temporarily exceeds demand. High solar generation, lower demand, network constraints and limited flexibility in conventional generation can contribute to these conditions.

These are potential explanatory factors, not conclusions established by the price series alone. Confirming the drivers requires corroborating generation, demand, weather and system information.

From a trading perspective, analysts may monitor renewable-generation forecasts, demand forecasts, generation availability, interconnector flows and intraday price developments.

## 6. Data Quality and Limitations

The dataset contains no duplicate timestamps, and consecutive observations are separated by 15 minutes.

The number of intervals per calendar date varies because of daylight-saving-time transitions.

The repeated prices close to −€500/MWh should be independently checked against an authoritative market-data source before being treated as fully validated observations.

This is a historical descriptive analysis, not a trading strategy or evidence of achievable trading profits. Transaction costs, execution constraints and forecast-based entry and exit rules have not been modelled.

## 7. Next Steps

1. Independently validate the extreme-price observations.
2. Add generation, demand and weather data to investigate potential price drivers.
3. Examine relationships between renewable generation and negative-price frequency.
4. Document the data sources and make the analysis reproducible.
5. Explore whether market fundamentals can help explain or anticipate extreme-price intervals.

## 8. Key Takeaway

The analysis identifies substantial price variation and a concentrated period of extreme negative prices in the German-Luxembourg electricity market. It establishes a foundation for further research into the relationship between power-system fundamentals and price formation.