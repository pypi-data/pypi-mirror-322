import json
import redis
import telebot
import os
import logging
from termcolor import colored
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.formatting import escape_markdown

from bot_audio import audio_add
from bot_text import text_add
from ai.ask import ai_assistent,AIAssistant

class MyBot:
    def __init__(self,ai_reset:bool=False):
        # Initialize logging
        logging.basicConfig(level=logging.INFO, format='%(message)s')
        self.logger = logging.getLogger(__name__)

        # Initialize Redis connection   
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0)

        # Initialize Telegram bot
        self.telebotkey = os.getenv("TELEBOT")
        if self.telebotkey:
            self.logger.info(colored("TELEBOT key set", "green"))
            self.bot = telebot.TeleBot(self.telebotkey)
        else:
            raise Exception("can't find TELEBOT in ENV")

        # Set up message handlers
        self.setup_handlers()
        audio_add(self)
        text_add(self,reset=ai_reset)

    def setup_handlers(self):
        @self.bot.message_handler(commands=['help'])
        def send_welcome(message):
            self.bot.reply_to(message, """\
Hi there, I am your hero.
Just speak to me or do /start or /help
""")

        @self.bot.message_handler(commands=['start'])
        def start_command(message):
            chat_id = message.chat.id

            keyboard = InlineKeyboardMarkup()
            subscribe_button = InlineKeyboardButton("Subscribe to Updates", callback_data='subscribe')
            unsubscribe_button = InlineKeyboardButton("Unsubscribe from Updates", callback_data='unsubscribe')
            keyboard.row(subscribe_button, unsubscribe_button)

            self.bot.reply_to(message, "Please choose an option:", reply_markup=keyboard)

        @self.bot.callback_query_handler(func=lambda call: True)
        def callback_query(call):
            chat_id = call.message.chat.id

            if call.data == 'subscribe':
                self.redis_client.hset('subscribed_chats', chat_id, '1')
                self.bot.answer_callback_query(call.id, "You have subscribed to updates.")
                print(f"User subscribed to updates: {chat_id}")
            elif call.data == 'unsubscribe':
                self.redis_client.hdel('subscribed_chats', chat_id)
                self.bot.answer_callback_query(call.id, "You have unsubscribed from updates.")
                print(f"User unsubscribed from updates: {chat_id}")

    def send_message_to_subscribers(self, message):
        subscribed_chats = self.redis_client.hgetall('subscribed_chats')
        for chat_id in subscribed_chats:
            try:
                self.bot.send_message(chat_id.decode('utf-8'), message)
            except Exception as e:
                print(f"Failed to send message to chat {chat_id}: {str(e)}")

    def send_error_to_telegram(self,chat_id, error_message):
        # Format the error message for Telegram
        telegram_message = f"🚨 Error Occurred 🚨\n\n"
        telegram_message += f"app: {escape_markdown(error_message['app'])}\n"
        telegram_message += f"Function: {escape_markdown(error_message['function'])}\n"
        telegram_message += f"msg: {escape_markdown(error_message['msg'])}\n"
        telegram_message += f"Exception Type: {escape_markdown(error_message['exception_type'])}\n"
        telegram_message += f"Exception Message: ```\n{escape_markdown(error_message['exception_message'])}\n```\n"
        if 'traceback' in error_message:
            telegram_message += f"Traceback:\n```\n{escape_markdown(error_message['traceback'])}\n```"
        # Send the error message to the subscribed chat
        self.bot.send_message(chat_id, telegram_message, parse_mode='Markdown')


    def start(self):
        print("Bot started")
        # Start the bot
        self.bot.polling()
        
        
def bot_new() -> MyBot:
    return MyBot()

# Usage
if __name__ == "__main__":
    my_bot = bot_new()
    my_bot.start()