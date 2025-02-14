# Stock screener

## How to use it?
### Telegram
Join the channel
https://t.me/+cY_RLrky6bNlMWM0
The bot will send the stock list every 3 hours during market opening time.

## Strategy
### Strategy version #2
#### Limitation
Only S&P and Russell stocks

#### Description
1. Minimum price, default 10$
2. Minimum volume, default 1M
2. Max RSI, default 30
3. 150 DAILY avg trend, default Up
4. Gap from 150AVG, default 3

#### How to use it?
```python

sp_index_name = "S&P"
russel_index_name = "Russell"
custom_index_name = "Custom"

find_stocks([sp_index_name, russel_index_name], ScanConfig())
```

#### Example output
```
🚀 Stocks matching criteria:
StockData(symbol=BX, last_close=160.47999572753906, avg_150_today=159.81351791381837, avg_150_yesterday=159.5561091105143, avg_volume=3387196.0, trend=Trend.UP, rsi=18.15)
StockData(symbol=CAT, last_close=353.70001220703125, avg_150_today=367.7413568115234, avg_150_yesterday=367.5485955810547, avg_volume=2357915.3333333335, trend=Trend.UP, rsi=15.04)
StockData(symbol=BDX, last_close=225.00999450683594, avg_150_today=232.70280446370444, avg_150_yesterday=232.68208485921224, avg_volume=1672986.0, trend=Trend.UP, rsi=28.79)
StockData(symbol=A, last_close=136.4499969482422, avg_150_today=138.64731775919597, avg_150_yesterday=138.58187759399414, avg_volume=1639674.0, trend=Trend.UP, rsi=20.89)
```



### Strategy version #1
#### Limitation
Only S&P stocks

#### Description
1. Calculate 150 daily AVG
2. Verify the 150 daily moving AVG trend is going up.
3. Stock price is higher than the AVG but not more than 3%

## Run
### Run locally
1. Create virtual environment
2. Install the requirements from requirement.txt
4. Run the code with arg "local"

### Run with telegram
1. Create a telegram bot
2. Create a channel
3. create .env file
4. add the bot token and your channel id

```commandline
TELEGRAM_BOT_TOKEN=778...
CHANNEL_CHAT_ID=-100...
```

