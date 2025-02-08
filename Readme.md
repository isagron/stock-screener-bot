# Stock screener

## How to use it?
### Telegram
Join the channel
https://t.me/+cY_RLrky6bNlMWM0
The bot will send the stock list every 3 hours during market opening time.

## Strategy version #1
### Limitation
Only S&P stocks

### Description
1. Calculate 150 daily AVG
2. Verify the 150 daily moving AVG trend is going up.
3. Stock price is higher than the AVG but not more than 3%

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

