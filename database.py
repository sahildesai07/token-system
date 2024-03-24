from telegram.ext import Updater, CommandHandler
from pymongo import MongoClient
from urllib.parse import quote_plus
import random
import string
import logging

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Replace this with your MongoDB connection URI
DATABASE_URI = "mongodb+srv://Cluster0:Cluster0@cluster0.c07xkuf.mongodb.net/?retryWrites=true&w=majority"

# Initialize MongoDB client and database
client = MongoClient(DATABASE_URI)
db = client.get_default_database()
collection = db['tokens']

# Function to generate a random token
def generate_token():
    # Generate a random string of characters for the token
    token = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    return token

# Function to save token to MongoDB
def save_token_to_db(user_id, token):
    # Insert token into the database
    token_doc = {'user_id': user_id, 'token': token}
    collection.insert_one(token_doc)

# Function to handle /start command
def start(update, context):
    user_id = update.message.from_user.id
    logger.info(f"User {user_id} requested /start")

    # Check if the user already has a token
    existing_token = collection.find_one({'user_id': user_id})

    if existing_token:
        token = existing_token['token']
        logger.info(f"User {user_id} already has token: {token}")
        update.message.reply_text(f'You already have a token: {token}')
    else:
        # Generate token
        token = generate_token()
        logger.info(f"Generated new token for user {user_id}: {token}")

        # Save token to database
        save_token_to_db(user_id, token)

        # Provide token through link
        bot_username = context.bot.username
        token_encoded = quote_plus(token)
        link = f"https://t.me/terabox_sis_bot?start=token_{token_encoded}"
        update.message.reply_text(f'Use this link to verify: {link}')
        logger.info(f"Sent verification link to user {user_id}")

# Function to start the bot
def main():
    # Create the Updater and pass it your bot's token
    updater = Updater("7062468773:AAHQTrhqussRoplB365l6XwdZKaYO_WSAm0", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Register the command handler for the /start command
    dp.add_handler(CommandHandler("start", start))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C
    updater.idle()

if __name__ == '__main__':
    main()

