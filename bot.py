import re
from googletrans import Translator
from pyrogram import Client, Filters
import pymongo
# Connect to the MongoDB database
client = pymongo.MongoClient('mongodb://localhost:27017/')

# Get a reference to the database
db = client['my_database']

# Get a reference to the collection
collection = db['allowed_languages']
lives_collection = db['lives_collection']

# Function to handle the /start command
@Client.on_message(Filters.command('start'))
def start(client, message):
    message.reply_text('This is a language detection bot. It can delete messages that are not in the allowed language. The admin can use the /allow_language command to specify the list of allowed languages.')

# Function to handle the /help command
@Client.on_message(Filters.command('help'))
def help(client, message):
    # Reply with a message containing the guide for the available commands
    message.reply_text('Here is a guide for the available commands:\n\n'
                       '/start: This command is used to start the bot.\n\n'
                       '/allow_language: This command is used to specify the list of allowed languages for the current chat. Only the admin of the chat can use this command. The command should be followed by a list of language codes, separated by spaces. For example, to allow messages in English, Spanish, and German, the admin can use the following command: /allow_language en es de. After the command is used, the bot will reply with a message listing the allowed languages for the current chat.\n\n'
                       '/reset_allowed_languages: This command is used to reset the list of allowed languages for the current chat. After resetting the list, the bot will accept messages in all languages. Only the admin of the chat can use this command. When the /reset_allowed_languages command is used, the bot will reply with a message confirming that the list of allowed languages has been reset.\n\n'
                       '/help: This command is used to show the guide for the available commands.\n\n')

# Function to handle the /allow_language command
@Client.on_message(Filters.command('allow_language'))
def allow_language(client, message):
    # Get the chat id of the current chat
    chat_id = message.chat.id

    # If the user who sent the command is the admin, update the allowed languages
    # Otherwise, just show the list of allowed languages
    if message.from_user.status.admin_rights:
        # Update the document for the current chat
        # If no such document exists, insert a new one with the specified values
        collection.update_one({'_id': chat_id}, {'$set': {'languages': message.command[1:]}}, upsert=True)

        message.reply_text('The allowed languages for this chat have been updated to: {}'.format(', '.join(message.command[1:])))
    else:
        allowed_languages = collection.find_one({'_id': chat_id})
        message.reply_text('The allowed languages for this chat are: {}'.format(', '.join(allowed_languages['languages'])))


# Function to handle the /reset_allowed_languages command
@Client.on_message(Filters.command('reset_allowed_languages'))
def reset_allowed_languages(client, message):
    # Check if the user who sent the command is the admin
    if not message.from_user.status.admin_rights:
        message.reply_text('Sorry, only the admin can use the /reset_allowed_languages command.')
        return

    # Get the chat id of the current chat
    chat_id = message.chat.id

    # Reset the list of allowed languages for the current chat
    # Create a new document for the current chat
    new_document = {'_id': chat_id}

    # Insert the new document into the collection
    collection.delete_one(new_document)
    message.reply_text('The allowed languages for this chat have been reset to accept all languages.')

# Function to handle incoming messages
@Client.on_message()
def delete_message_if_not_allowed_language(client, message):
    if not message.from_user.status.admin_rights:
        # Use the Google Translate API to detect the language of the incoming message
        translator = Translator()
        detected_language = translator.detect(message.text).lang

        # Get the chat id of the current chat
        chat_id = message.chat.id

        # Check if the message contains emojis
        if re.search(r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF]', message.text):
            # If the message contains emojis, consider it as allowed and do not delete it
            return

        # Get the list of allowed languages for the current chat
        allowed_languages = collection.find_one({'_id': chat_id})

        # If the detected language is not in the list of allowed languages for the current chat,
        # give the user 3 lives and warn them every time they send a message in a language that is not allowed
        if detected_language not in allowed_languages['languages']:
            # Get the user's remaining lives from the database
            user_lives = lives_collection.find_one({'_id': message.from_user.id})

            # If the user does not have a record in the database, insert a new one with 3 lives
            if not user_lives:
                lives_collection.insert_one({'_id': message.from_user.id, 'lives': 3})
                user_lives = {'_id': message.from_user.id, 'lives': 3}

            # If the user has lives remaining, warn them and reduce their lives by 1
            if user_lives['lives'] > 0:
                message.reply_text('Sorry, your message was not in the allowed language. You have {} lives remaining.'.format(user_lives['lives']))
                lives_collection.update_one({'_id': message.from_user.id}, {'$inc': {'lives': -1}})

            # If the user has used all their lives, delete their message
            else:
                client.delete_messages(chat_id=message.chat.id, message_ids=[message.message_id])
                message.reply_text('Sorry, your message was deleted because it was not in the allowed language and you have used all your lives.')
