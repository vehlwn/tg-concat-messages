import datetime
import logging
import sys
import telethon

import config_parser_factory

config = config_parser_factory.create_parser()
config.read("config.ini")

logger = logging.getLogger(__name__)
logging.basicConfig(format=config["logger"]["format"])
logger.setLevel(logging.DEBUG)

API_ID = config["telegram"]["api_id"]
API_HASH = config["telegram"]["api_hash"]
EXPLAIN_CONCAT = config.getboolean("concat", "explain")
CONCAT_TIMEOUT = datetime.timedelta(seconds=int(config["concat"]["timeout_s"]))
client = telethon.TelegramClient("client", API_ID, API_HASH)


async def _get_messages(chat_id, limit):
    ret = []
    async for message in client.iter_messages(chat_id, limit=limit):
        ret.append(message)
    return ret


def _should_concat(event) -> bool:
    return (
        event.media is None
        and event.fwd_from is None
        and event.via_bot_id is None
        and event.reply_to_msg_id is None
        and event.reply_markup is None
    )


def _get_title(chat) -> str:
    ret = ""
    if isinstance(chat, telethon.tl.types.User):
        if chat.username:
            ret += "@" + chat.username + " "
        if chat.first_name:
            ret += chat.first_name + " "
        if chat.last_name:
            ret += chat.last_name
    elif isinstance(chat, telethon.tl.types.Chat) or isinstance(
        chat, telethon.tl.types.Channel
    ):
        ret = chat.title
    return ret


@client.on(telethon.events.NewMessage(outgoing=True))
async def handler(event):
    chat = await event.get_chat()
    title = _get_title(chat)
    logger.info(f"EVENT in chat {title}")
    last_messages = await _get_messages(event.chat_id, 2)
    if len(last_messages) < 2:
        logger.info("Not enough last messages")
        return
    last_message = last_messages[1]
    last_date = last_message.edit_date or last_message.date
    me = await client.get_me()
    if (
        last_message.sender_id == me.id
        and _should_concat(event)
        and _should_concat(last_message)
        and event.date - last_date <= CONCAT_TIMEOUT
    ):
        logger.info("Concating")
        logger.info(f"{last_message.text=}, {event.text=}")
        await last_message.edit(f"{last_message.text}\n{event.text}")
        await event.delete(revoke=True)
    else:
        logger.info("no")
        if EXPLAIN_CONCAT:
            if last_message.sender_id != me.id:
                logger.info(f"{last_message.sender_id=} != {me.id=}")
            elif event.media:
                logger.info(f"{event.media=}")
            elif event.fwd_from:
                logger.info(f"{event.fwd_from=}")
            elif event.via_bot_id:
                logger.info(f"{event.via_bot_id=}")
            elif event.reply_to_msg_id:
                logger.info(f"{event.reply_to_msg_id=}")
            elif event.reply_markup:
                logger.info(f"{event.reply_markup=}")
            elif last_message.media:
                logger.info(f"{last_message.media=}")
            elif last_message.fwd_from:
                logger.info(f"{last_message.fwd_from=}")
            elif last_message.via_bot_id:
                logger.info(f"{last_message.via_bot_id=}")
            elif last_message.reply_to_msg_id:
                logger.info(f"{last_message.reply_to_msg_id=}")
            elif last_message.reply_markup:
                logger.info(f"{last_message.reply_markup=}")
            elif event.date - last_date > CONCAT_TIMEOUT:
                logger.info(
                    f"event.date ({event.date}) - last_date ({last_date})"
                    f" > {CONCAT_TIMEOUT}"
                )


async def main():
    logger.info("Connecting")
    await client.connect()
    if not await client.is_user_authorized():
        logger.critical("You must call login.py before starting this client")
        sys.exit(1)
    logger.info("Authorized. Wait until disconnected")
    await client.disconnected


client.loop.run_until_complete(main())
