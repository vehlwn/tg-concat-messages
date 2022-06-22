import logging
import telethon

import config_parser_factory

config = config_parser_factory.create_parser()
config.read("config.ini")

logger = logging.getLogger(__name__)
logging.basicConfig(format=config["logger"]["format"])
logger.setLevel(logging.DEBUG)

API_ID = config["telegram"]["api_id"]
API_HASH = config["telegram"]["api_hash"]
PHONE = config["telegram"]["phone"]

client = telethon.TelegramClient("client", API_ID, API_HASH)


async def main():
    logger.info("Connecting")
    await client.connect()
    if await client.is_user_authorized():
        logger.info("Already logged in. Exitting")
    else:
        logger.info("Not authorized. Sending code request")
        await client.send_code_request(PHONE)
        await client.sign_in(PHONE, input("Enter the code: "))
        logger.info("Logged in")


client.loop.run_until_complete(main())
