import logging
import telethon

import app_settings

config = app_settings.ApplicationSettings()

logger = logging.getLogger(__name__)
logging.basicConfig(format=config.logger_format())
logger.setLevel(logging.DEBUG)

client = telethon.TelegramClient(
    "client", config.telegram_api_id(), config.telegram_api_hash()
)


async def main():
    logger.info("Connecting")
    await client.connect()
    if await client.is_user_authorized():
        logger.info("Already logged in. Exitting")
    else:
        logger.info("Not authorized. Sending code request")
        await client.send_code_request(config.telegram_phone())
        await client.sign_in(config.telegram_phone(), input("Enter the code: "))
        logger.info("Logged in")


client.loop.run_until_complete(main())
