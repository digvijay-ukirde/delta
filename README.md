# Intraduction

This project is used to understand Dadus's requirements.

## Notes

1. Default Quota is 10000 for a fixed 5 minute window (2000/min, 33/sec). 
Rate Limit quota resets to full every 5 mins.
We have also introduced rate limits to manage operations within the matching engine. The current rate limit is set at 500 operations per second for each product. For example, placing 50 orders in a batch counts as 50 operations, as each individual order will be processed by the matching engine.

2. Table

| Weight Slab |	API Endpoints                                                                              |
| ------------|--------------------------------------------------------------------------------------------|
| 3	          | Get Products, Orderbook, Tickers, Open Orders, Open Postions, Balances, OHLC Candles       |
| 5	          | Place/Edit/Delete Order, Add Position Margin                                               |
| 10	      | Get Order History, Get Fills, Get Txn Logs                                                 |
| 25	      | Batch Order Apis                                                                           |

