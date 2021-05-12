---
operator: local.MaterializedPostgresOperator
description: Cleaning the stock data for our model
fields:
    - date: Date of market data
    - open: Stock price at open
    - high: High of stock price for the day
    - low: Low of stock price for the day
    - close: Stock price at close
    - volume: Total amount of stock traded for the day
---

SELECT
  DATE(date) AS date,
  open,
  high,
  low,
  close,
  volume
FROM views.stock_data
WHERE close IS NOT NULL
