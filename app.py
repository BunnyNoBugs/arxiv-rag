#!/usr/bin/env python
# pylint: disable=unused-argument

"""
Bot to reply to Telegram messages.
"""

import logging
import os

from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

from dotenv import load_dotenv

from rag.rag import RAG, GPTunnelLLM
from langchain_community.retrievers import ArxivRetriever
from langchain_mistralai import ChatMistralAI

load_dotenv('../.env')

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help Me!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(update.message.text)


async def rag_reply(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Returns the reply to user after getting reply from Agent"""

    logger.info("Question from User: %s", update.message.text)
    retriever = ArxivRetriever(
        top_k_results=3,
        get_full_documents=False,  # gives errors with MuPDF when True
        doc_content_chars_max=10000000000
    )

    mistral_llm = ChatMistralAI(
        model="mistral-large-latest",
        temperature=0,
        max_retries=2,
        # other params...
    )

    assistant = RAG(llm=mistral_llm, retriever=retriever)

    if update.message.text != '':
        user_input = update.message.text
        response = assistant.handle_user_input(user_input)

    else:
        return None

    await update.message.reply_text(response)


def main() -> None:
    """Start the bot."""
    bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
    application = Application.builder().token(bot_token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # echo the message on Telegram
    # application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # RAG reply should be
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, rag_reply))

    # until  Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
