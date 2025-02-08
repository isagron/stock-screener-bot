import datetime
import json
import time
import asyncio
import os
import sys

from dotenv import load_dotenv

import pandas as pd
import requests
from telegram import Bot
import yfinance as yf


sp500 = ["AAPL", "MSFT", "NVDA", "AMZN", "GOOGL", "GOOG", "META", "TSLA", "BRK.B", "AVGO",
    "WMT", "JPM", "LLY", "V", "MA", "UNH", "XOM", "ORCL", "COST", "NFLX",
    "HD", "PG", "JNJ", "BAC", "CRM", "ABBV", "CVX", "TMUS", "KO", "WFC",
    "MRK", "CSCO", "NOW", "ACN", "BX", "MS", "ABT", "AXP", "TMO", "GS",
    "GE", "IBM", "PEP", "MCD", "LIN", "ISRG", "DIS", "PM", "ADBE", "AMD",
    "CAT", "HON", "NKE", "MDT", "NEE", "AMGN", "TXN", "LOW", "SPGI", "INTC",
    "QCOM", "UNP", "UPS", "SCHW", "PLD", "RTX", "CVS", "BLK", "T", "MMM",
    "MO", "C", "BA", "DE", "LMT", "AMT", "DUK", "SO", "USB", "CCI",
    "CL", "DHR", "ELV", "BDX", "SYK", "TJX", "ZTS", "ADP", "CI", "MMC",
    "PNC", "BKNG", "ITW", "WM", "APD", "FIS", "FISV", "MET", "AON", "ICE",
    "GILD", "NSC", "TFC", "HUM", "PSA", "CME", "MCO", "AEP", "ADI", "MSI",
    "ROP", "SBUX", "MDLZ", "VRTX", "REGN", "ADSK", "CDNS", "SNPS", "FTNT", "MNST",
    "CTAS", "KLAC", "IDXX", "MRNA", "LRCX", "NXPI", "PAYX", "TRV", "ORLY", "CTSH",
    "SPG", "KMB", "STZ", "AIG", "PRU", "ALL", "WBA", "AFL", "A", "AKAM",
    "ALB", "ARE", "ALGN", "ALLE", "LNT"]

if os.getenv("AWS_EXECUTION_ENV") is None:
    load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHANNEL_CHAT_ID = os.getenv("CHANNEL_CHAT_ID")

if not BOT_TOKEN:
    raise ValueError("Missing TELEGRAM_BOT_TOKEN in environment variables!")

print(f"Loaded bot token: {BOT_TOKEN[:5]}... (hidden for security)")

def get_150_day_average(symbol):
    stock = yf.Ticker(symbol)
    data = stock.history(period="152d")  # Fetch last 152 days

    if data.empty or "Close" not in data:
        raise ValueError(f"No data found for {symbol}")

    last_150_days_avg = float(data["Close"].iloc[-150:].mean())
    last_150_days_avg_yesterday = float(data["Close"].iloc[-151:-1].mean())

    return [last_150_days_avg, last_150_days_avg_yesterday]  # Calculate average closing price


def get_real_time_price(symbol):
    stock = yf.Ticker(symbol)
    return stock.info.get("currentPrice", None)


def find_stocks_above_ma150(tickers):
    results = []
    retry_delay = 1
    for ticker in tickers:
        print(f"Checking stock: {ticker}")
        try:
            latest_close = get_real_time_price(ticker)
            if latest_close is not None and latest_close > 10:
                ma150_data = get_150_day_average(ticker)
                if latest_close > ma150_data[0] > ma150_data[1]:
                    diff_percentage = ((latest_close - ma150_data[0]) / ma150_data[0]) * 100
                    if diff_percentage <= 3:
                        print(f"Add: {ticker} to the list")
                        results.append((ticker, latest_close, ma150_data[0], round(diff_percentage, 2)))

        except Exception as e:
            print(f"⚠️ Error processing {ticker}: {e}")
            time.sleep(retry_delay)
            retry_delay *= 2

    return results


def is_market_open():
    now = datetime.datetime.now()
    market_open_time = datetime.time(16, 30)  # 16:30 PM EST
    market_close_time = datetime.time(23, 0)  # 23:00 PM EST
    return now.weekday() < 5 and market_open_time <= now.time() <= market_close_time


# Main function
async def send_telegram_message(message):
    # Replace 'YOUR_API_TOKEN' with the token you got from BotFather
    bot = Bot(token=BOT_TOKEN)

    # Send the message
    result = await bot.send_message(chat_id=CHANNEL_CHAT_ID, text=message)



async def find_chat_id():
    bot = Bot(token=BOT_TOKEN)

    # Get updates from the bot
    updates = await bot.get_updates()

    # Print the chat ID of the last message received
    if updates:
        chat_id = updates[-1].message.chat_id
        print(f"Your chat ID is: {chat_id}")
    else:
        print("No updates found. Make sure you've sent a message to your bot.")

def lambda_handler(event, context):
    # Your script logic goes here
    main()
    return "Execution successful"


def should_send_message_to_telegram_channel():
    if len(sys.argv) > 1:
        arg1 = sys.argv[1]
        return arg1 == "local"
    return True


def main():
    # if not is_market_open():
    #     print("📉 Market is closed. Skipping execution.")
    #     return
    # chatId = asyncio.run(find_chat_id())
    # asyncio.run(send_telegram_message("hello"))
    tickers = sp500
    matching_stocks = find_stocks_above_ma150(tickers)

    if matching_stocks:
        message = "🚀 Stocks matching criteria:\n"
        for stock in matching_stocks:
            message += f"{stock[0]} - Close: {stock[1]:.2f}, MA150: {stock[2]:.2f}, Diff: {stock[3]}%\n"
        print(message)
        if should_send_message_to_telegram_channel():
            asyncio.run(send_telegram_message(message))
    else:
        print("✅ No stocks found matching the criteria.")


if __name__ == "__main__":
    main()
