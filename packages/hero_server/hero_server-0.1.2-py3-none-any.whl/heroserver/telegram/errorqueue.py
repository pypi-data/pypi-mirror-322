import json
import redis
import telebot
import threading
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import time
from telebot.formatting import escape_markdown
import os
from telegram.bot import send_error_to_telegram

# Initialize Redis connection
redis_client = redis.Redis(host='localhost', port=6379, db=0)

#get errors from redis and send them to bot if subscription done
def process_error_queue():
    while True:
        # Pop an error message from the Redis queue
        error_json = redis_client.lpop('error_queue')

        if error_json:
            # Deserialize the error message from JSON
            error_message = json.loads(error_json)

            # Get all subscribed chat IDs from Redis
            subscribed_chats = redis_client.hgetall('subscribed_chats')

            # Send the error message to all subscribed chats
            for chat_id in subscribed_chats.keys():
                send_error_to_telegram(int(chat_id), error_message)
        else:
            # If the queue is empty, wait for a short interval before checking again
            time.sleep(1)

# Start processing the error queue
process_error_queue_thread = threading.Thread(target=process_error_queue)
process_error_queue_thread.start()