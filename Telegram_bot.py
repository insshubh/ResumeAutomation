import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    ConversationHandler, ContextTypes, filters
)
from github_api import add_skill_to_github, add_certificate_to_github  # Ensure this file exists

# Load environment variables
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# States for conversation handler
ASK_SKILL, ASK_CERTIFICATE = range(2)


# Define the start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Hi! I am your Resume Bot. You can use /help to see what I can do.')


# Define the help command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('You can use the following commands:\n'
                                    '/add_skill - Add a skill to your resume\n'
                                    '/add_certificate - Add a certificate to your resume')


# Define the add skill command
async def add_skill(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text('Please enter the name of the skill you want to add:')
    return ASK_SKILL


# Handle the skill name input
async def handle_skill_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    skill = update.message.text
    await update.message.reply_text(f'Adding skill "{skill}" to your resume.')

    try:
        add_skill_to_github(skill)  # Add the skill to GitHub
        await update.message.reply_text(f'Skill "{skill}" has been added to your GitHub repository.')
    except ValueError as e:
        await update.message.reply_text(f"Error: {e}")

    return ConversationHandler.END


# Define the add certificate command
async def add_certificate(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text('Please enter the name of the certificate you want to add:')
    return ASK_CERTIFICATE


# Handle the certificate name input
async def handle_certificate_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    certificate = update.message.text
    await update.message.reply_text(f'Adding certificate "{certificate}" to your resume.')

    try:
        add_certificate_to_github(certificate)  # Add the certificate to GitHub
        await update.message.reply_text(f'Certificate "{certificate}" has been added to your GitHub repository.')
    except ValueError as e:
        await update.message.reply_text(f"Error: {e}")

    return ConversationHandler.END


# Define the main function
def main() -> None:
    # Create the Application and pass it your bot's token
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Create the conversation handler for adding a skill
    skill_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("add_skill", add_skill)],
        states={
            ASK_SKILL: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_skill_name)],
        },
        fallbacks=[]
    )

    # Create the conversation handler for adding a certificate
    cert_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("add_certificate", add_certificate)],
        states={
            ASK_CERTIFICATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_certificate_name)],
        },
        fallbacks=[]
    )

    # Register the command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(skill_conv_handler)
    application.add_handler(cert_conv_handler)

    # Start the Bot
    application.run_polling()


if __name__ == '__main__':
    main()
