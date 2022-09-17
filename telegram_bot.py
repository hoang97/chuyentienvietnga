import logging
from telegram.ext import Application
from conversationHandlers.menuHandler import menu_handler

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

def main() -> None:
    """Run the bot."""
    application = Application.builder().token("5538324444:AAF3O9TbuWophnrxNRfg93xvVNsd7PuBIus").build()

    application.add_handler(menu_handler)
    application.run_polling()

if __name__ == "__main__":
    main()