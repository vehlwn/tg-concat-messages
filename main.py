import datetime
import logging
import sys
import telethon
import asyncio

import app_settings

config = app_settings.ApplicationSettings()

logger = logging.getLogger(__name__)
logging.basicConfig(format=config.logger_format())
logger.setLevel(logging.DEBUG)

CONCAT_TIMEOUT = datetime.timedelta(seconds=config.concat_timeout_s())
client = telethon.TelegramClient(
    "client", config.telegram_api_id(), config.telegram_api_hash()
)
_concat_mutex = asyncio.Lock()


async def _get_messages(chat_id, *, limit, offset_id):
    ret = []
    async for message in client.iter_messages(
        chat_id, limit=limit, offset_id=offset_id
    ):
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
        comma = ""
        if chat.username:
            ret += "@" + chat.username
            comma = " "
        if chat.first_name:
            ret += comma + chat.first_name
        if chat.last_name:
            ret += comma + chat.last_name
    elif isinstance(chat, telethon.tl.types.Chat) or isinstance(
        chat, telethon.tl.types.Channel
    ):
        ret = chat.title
    return ret


async def _process_link_preview(event: telethon.tl.custom.message.Message):
    if isinstance(event.media, telethon.tl.types.MessageMediaWebPage):
        if config.format_remove_link_preview():
            logger.info("Deleting link_preview")
            event = await event.edit(event.text, link_preview=False, file=None)
        else:
            logger.info("Ignoring link_preview")
    return event


@client.on(telethon.events.NewMessage(outgoing=True))
async def new_message_handler(event: telethon.tl.custom.message.Message):
    async with _concat_mutex:
        chat = await event.get_chat()
        title = _get_title(chat)
        logger.info(f"NEW MESSAGE in chat {title}: {event.text}")
        event = await _process_link_preview(event)
        last_messages = await _get_messages(
            event.chat_id, limit=1, offset_id=event.id
        )
        if len(last_messages) == 0:
            logger.info("Not enough last messages")
            return
        last_message = last_messages[0]
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


@client.on(telethon.events.MessageEdited(outgoing=True))
async def edit_message_handler(event: telethon.tl.custom.message.Message):
    chat = await event.get_chat()
    title = _get_title(chat)
    logger.info(f"EDIT MESSAGE in chat {title}: {event.text}")
    await _process_link_preview(event)


async def main():
    logger.info("Connecting")
    await client.connect()
    if not await client.is_user_authorized():
        logger.critical("You must call login.py before starting this client")
        sys.exit(1)
    logger.info("Authorized. Wait until disconnected")
    await client.disconnected


client.loop.run_until_complete(main())
