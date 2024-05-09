import os
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, CallbackContext
import requests
import queue

API_KEY = os.getenv('WEATHER_API_KEY')
BOT_TOKEN =os.getenv('TELEGRAM_BOT_TOKEN')

def start(update: Update, context: CallbackContext):
    update.message.reply_text('Hello! Use /weather_latlong <lat> <long> or /weather_locality <locality_id> to get weather updates.')

def weather_latlong(update: Update, context: CallbackContext):
    try:
        latitude = context.args[0]
        longitude = context.args[1]
        url = f'https://weatherunion.com/gw/weather/external/v0/get_weather_data?latitude={latitude}&longitude={longitude}'
        headers = {'content-type': 'application/json', 'x-zomato-api-key': API_KEY}
        response = requests.get(url, headers=headers)
        weather_data = response.json()
        update.message.reply_text(f"Weather Data: {weather_data}")
    except (IndexError, ValueError):
        update.message.reply_text("Usage: /weather_latlong <latitude> <longitude>")

def weather_locality(update: Update, context: CallbackContext):
    try:
        locality_id = context.args[0]
        url = f'https://weatherunion.com/gw/weather/external/v0/get_locality_weather_data?locality_id={locality_id}'
        headers = {'content-type': 'application/json', 'x-zomato-api-key': API_KEY}
        response = requests.get(url, headers=headers)
        weather_data = response.json()
        update.message.reply_text(f"Weather Data: {weather_data}")
    except IndexError:
        update.message.reply_text("Usage: /weather_locality <locality_id>")

def main():
    # Create the Updater with your bot's token
    bot = Bot(token=BOT_TOKEN)
   # update_queue = queue.Queue()
    updater = Updater(bot=bot,use_context=True)
    
    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    
    # Add command handlers
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('weather_latlong', weather_latlong,pass_args=True))
    dp.add_handler(CommandHandler('weather_locality', weather_locality,pass_args=True))
    
    # Start the Bot
    updater.start_polling()
    
    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()

if __name__ == '__main__':
    main()
