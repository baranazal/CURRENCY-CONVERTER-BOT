import requests
import re
import logging
import telegram

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


def start(update, context):
  context.bot.send_message(
    chat_id=update.message.chat_id,
    text=
    "Welcome to the Currency Converter Bot! To use me, please send me a message with the amount you want to convert and the currencies you want to convert between, for example: '100 USD to EUR'.\n\n"
    "Here's a list of some of the supported currencies and their codes:\n\n"
    "USD - United States Dollar\n"
    "JOD - Jordanian Dinar\n"
    "EUR - Euro\n"
    "SUR - Syrian Pound\n"
    "AED - United Arab Emirates Dirham\n"
    "\nTo view more currencies Type \"currencies\" \n"
    "\nor u just can visit us here :\nhttps://docs.openexchangerates.org/reference/supported-currencies"
  )


def convert_currency(amount, from_currency, to_currency):
  """
    Convert an amount from one currency to another using the Open Exchange Rates API.
    """
  API_KEY = "API_TOKEN" # Here you can add your token from https://openexchangerates.org/
  API_URL = f"https://openexchangerates.org/api/latest.json?app_id={API_KEY}"

  response = requests.get(API_URL)
  data = response.json()
  rates = data["rates"]

  from_rate = rates[from_currency]
  to_rate = rates[to_currency]

  converted_amount = amount / from_rate * to_rate
  return converted_amount


def handle_message(update, context):
  """
    Handle a user's message and return a response.
    """
  text = update.message.text.strip().lower()

  # Check if the user is asking for supported currencies
  if text == "currencies":
    response = "Here's a list of supported currencies and their codes:\n\n" \
               "USD - United States Dollar\n" \
               "EUR - Euro\n" \
               "GBP - British Pound\n" \
               "JPY - Japanese Yen\n" \
               "..."
    context.bot.send_message(chat_id=update.message.chat_id, text=response)
    return

  # Extract the amount, from currency, and to currency from the user's message
  match = re.match(r"(\d+) (\w+) to (\w+)", text)
  if match:
    amount = float(match.group(1))
    from_currency = match.group(2).upper()
    to_currency = match.group(3).upper()

    # Perform the currency conversion
    converted_amount = convert_currency(amount, from_currency, to_currency)
    response = f"{amount} {from_currency} is equivalent to {converted_amount} {to_currency}"
    context.bot.send_message(chat_id=update.message.chat_id, text=response)
  else:
    response = "I'm sorry, I don't understand your message. Please send me a message in the following format: " \
               "[amount] [from currency] to [to currency]. " \
               "Type 'currencies' to see a list of supported currencies."
    context.bot.send_message(chat_id=update.message.chat_id, text=response)


def main():
  """
    Start the bot.
    """
  # Set up logging
  logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

  # Get the bot's token from an environment variable
  BOT_TOKEN = "TELEGRAM_BOT_TOKEN" # Here you can add your token from BotFather

  # Initialize the bot
  updater = Updater(token=BOT_TOKEN, use_context=True)

  # Add the handlers
  dispatcher = updater.dispatcher
  start_handler = CommandHandler('start', start)
  dispatcher.add_handler(start_handler)
  message_handler = MessageHandler(Filters.text, handle_message)
  dispatcher.add_handler(message_handler)

  # Start the bot
  updater.start_polling()
  updater.idle()


if __name__ == '__main__':
  main()
