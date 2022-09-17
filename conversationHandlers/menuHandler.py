from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from .variables import *

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Send message on `/start`."""
    keyboard = [
        [InlineKeyboardButton("Channel Settings", callback_data=str(CHANNEL_SETTINGS))],
        [InlineKeyboardButton("Bot Functions", callback_data=str(BOT_FUNCTIONS))],
        [InlineKeyboardButton("Exit", callback_data=str(EXIT))],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    text = "Welcome to our bot"

    # If we're starting over we don't need to send a new message
    if context.user_data.get(START_OVER):
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(text=text, reply_markup=reply_markup)
    else:
        await update.message.reply_text(text=text + " (new)", reply_markup=reply_markup)

    context.user_data[START_OVER] = True

    return LAYER1_ROUTES


async def start_new_one(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    '''Send start message on a new reply'''
    context.user_data[START_OVER] = False
    await start(update, context)

    return LAYER1_ROUTES


async def end(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Returns `ConversationHandler.END`, which tells the
    ConversationHandler that the conversation is over.
    """
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="See you next time!")
    context.user_data[START_OVER] = False
    return END


async def btn_channelSettings_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    
    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("Publish", callback_data=str(PUBLISH))],
        [InlineKeyboardButton("Stop", callback_data=str(STOP_CHANNEL))],
        [InlineKeyboardButton("Show", callback_data=str(SHOW_LIST))],
        [InlineKeyboardButton("Back", callback_data=str(BACK))],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text="Choose Publish to start sending messages to channels\nChoose Stop to stop sending messages\nChoose Show to show current running channel", 
        reply_markup=reply_markup
    )

    return LAYER2_ROUTES


async def btn_botFunctions_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton("Check Rate", callback_data=str(CHECK_RATE))],
        [InlineKeyboardButton("Set Profit", callback_data=str(SET_PROFIT))],
        [InlineKeyboardButton("Back", callback_data=str(BACK))],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text="Choose Check Rate to get the detailed current rate\nChoose Set Profit to set the profit percentage", 
        reply_markup=reply_markup
    )

    return LAYER2_ROUTES


async def btn_publish_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    pass


async def btn_stop_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    pass


async def btn_showList_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    pass


async def btn_checkRate_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    pass


async def btn_setProfit_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    pass


menu_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        LAYER1_ROUTES: [
            CallbackQueryHandler(btn_channelSettings_handler, pattern="^" + str(CHANNEL_SETTINGS) + "$"),
            CallbackQueryHandler(btn_botFunctions_handler, pattern="^" + str(BOT_FUNCTIONS) + "$"),
        ],
        LAYER2_ROUTES: [
            CallbackQueryHandler(btn_publish_handler, pattern="^" + str(PUBLISH) + "$"),
            CallbackQueryHandler(btn_stop_handler, pattern="^" + str(STOP_CHANNEL) + "$"),
            CallbackQueryHandler(btn_showList_handler, pattern="^" + str(SHOW_LIST) + "$"),
            CallbackQueryHandler(btn_checkRate_handler, pattern="^" + str(CHECK_RATE) + "$"),
            CallbackQueryHandler(btn_setProfit_handler, pattern="^" + str(SET_PROFIT) + "$"),
        ],
    },
    fallbacks=[
        CallbackQueryHandler(start, pattern="^" + str(BACK) + "$"),
        CallbackQueryHandler(end, pattern="^" + str(EXIT) + "$"),
        CommandHandler("start", start_new_one),
    ],
)