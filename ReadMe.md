# Language Detection Bot

This is a Python-based language detection bot that uses the pyrogram library to connect to Telegram and handle incoming messages. The bot can be used to delete messages that are not in the list of allowed languages for a chat. The admin of a chat can use the `/allow_language` command to specify the list of allowed languages. The bot uses the Google Translate API to detect the language of incoming messages and compares it to the list of allowed languages for the current chat. If the language of the message is not in the allowed list, the bot will delete the message.

## Requirements

To run this bot, you will need the following:

- Python 3.6 or higher
- The pyrogram library
- The googletrans library
- A MongoDB database

## How to Use

To use this bot, you will need to do the following:

1. Install the required libraries using pip:

pip install pyrogram googletrans pymongo

Copy code

2. Start the MongoDB database.

3. Set the `APP_ID` and `API_HASH` environment variables. These are used by the pyrogram library to connect to Telegram.

4. Start the bot using the following command:

```
python language_detection_bot.py
```

5. Use the `/start` command in a Telegram chat to start the bot.

6. Use the `/allow_language` command to specify the list of allowed languages for the current chat. For example, to allow messages in English, Spanish, and German, you can use the following command:
```
/allow_language en es de
```
The bot will reply with a message listing the allowed languages for the current chat.

7. Any messages in languages that are not in the allowed list will be automatically deleted by the bot.

## Available Commands

- `/start`: This command is used to start the bot.
- `/allow_language`: This command is used to specify the list of allowed languages for the current chat. Only the admin of the chat can use this command. The command should be followed by a list of language codes, separated by spaces. For example, to allow messages in English, Spanish, and German, the admin can use the following command: `/allow_language en es de`. After the command is used, the bot will reply with a message listing the allowed languages for the current chat.
- `/reset_allowed_languages`: This command is used to reset the list of allowed languages for the current chat. After resetting the list, the bot will accept messages in all languages. Only the admin of the chat can use this command. When the `/reset_allowed_languages` command is used, the bot will reply with a message confirming that the list of allowed languages has been reset.
- `/help`: This command is used to show the guide for the available commands.