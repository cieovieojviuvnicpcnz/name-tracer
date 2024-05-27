from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import json
import os
from datetime import datetime

# Remplacez 'YOUR_TOKEN' par le token de votre bot
TOKEN = os.getenv('TOKEN')

# Dossier pour stocker les fichiers d'historique des utilisateurs
HISTORY_FOLDER = 'history'

if not os.path.exists(HISTORY_FOLDER):
    os.makedirs(HISTORY_FOLDER)

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Bonjour! Je suis votre bot de notification de changement d\'@.')

def save_user_info(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    user_info_path = os.path.join(HISTORY_FOLDER, f"history_{user.id}.txt")
    if not os.path.exists(user_info_path):
        with open(user_info_path, 'w') as file:
            file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} : {user.first_name}, @{user.username}\n")

def check_user(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    user_info_path = os.path.join(HISTORY_FOLDER, f"history_{user.id}.txt")
    if user.id in context.user_data:
        saved_info = context.user_data[user.id]
        if user.username != saved_info['username']:
            update.message.reply_text(f"@{saved_info['username']} a changé de nom d'utilisateur pour @{user.username}")
            saved_info['username'] = user.username
            save_user_info_to_file(user_info_path, user.first_name, user.username)
        if user.first_name != saved_info['name']:
            update.message.reply_text(f"{saved_info['name']} a changé de nom pour {user.first_name}")
            saved_info['name'] = user.first_name
            save_user_info_to_file(user_info_path, user.first_name, user.username)
    else:
        context.user_data[user.id] = {'id': user.id, 'name': user.first_name, 'username': user.username}
        save_user_info_to_file(user_info_path, user.first_name, user.username)
        update.message.reply_text("Bienvenue au nouveau membre!")

def save_user_info_to_file(file_path: str, name: str, username: str) -> None:
    with open(file_path, 'a') as file:
        file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} : {name}, @{username}\n")

def main() -> None:
    updater = Updater(TOKEN, use_context=True)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.status_update.new_chat_members, save_user_info))
    dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), check_user))

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()
