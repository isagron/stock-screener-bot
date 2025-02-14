import asyncio
import os
import sys

from dotenv import load_dotenv
from telegram import Bot

from src.stock_scanner import find_stocks

if os.getenv("AWS_EXECUTION_ENV") is None:
    load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHANNEL_CHAT_ID = os.getenv("CHANNEL_CHAT_ID")

if not BOT_TOKEN:
    raise ValueError("Missing TELEGRAM_BOT_TOKEN in environment variables!")

print(f"Loaded bot token: {BOT_TOKEN[:5]}... (hidden for security)")


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
    matching_stocks = find_stocks()

    if matching_stocks:
        message = "🚀 Stocks matching criteria:\n"
        for stock in matching_stocks:
            message += f"{stock}\n"
        print(message)
        if should_send_message_to_telegram_channel():
            asyncio.run(send_telegram_message(message))
    else:
        print("✅ No stocks found matching the criteria.")


if __name__ == "__main__":
    main()
