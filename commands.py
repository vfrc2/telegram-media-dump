import argparse
import os.path
import sys
from datetime import datetime
from telethon import TelegramClient, types, functions
from pathvalidate import sanitize_filename


async def init(client: TelegramClient):
    # Just check what client is running
    me = await client.get_me()
    print('Username: ', me.username)


async def listChats(client: TelegramClient):
    print('Availiable chats are: ')

    async for d in client.iter_dialogs(10):
        print(d.entity.stringify(), d.title)
    # List all availiable chats
    pass


async def backup(client: TelegramClient, chats: list[int], output: str, **options):
    # Do simple backup
    print(f"Backuping chats {[str(c) for c in chats]} to {output}")

    for chat in chats:
        try:
            entity = await client.get_entity(chat)
            print(f"Backup chat '{entity.title}'")
            async for m in client.iter_messages(entity):
                if m.file and m.file.mime_type in options['mime_types']:
                    chat_title = sanitize_filename(m.chat.title).replace(' ', '_')
                    values = {
                        'chat': chat,
                        'ctitle': chat_title,
                        'cstitle': chat_title[:15],
                        'date': m.date.strftime("%Y-%d-%mT%H:%M:%S"),
                        'ext': m.file.ext
                    }
                    filename = options['filename_tpl'].format(**values)
                    fullPath = os.path.join(output, filename)
                    if not os.path.isfile(fullPath):
                        await client.download_media(m, fullPath)
                        print(fullPath)
        except Exception as err:
            print(f"Error while backup chat '{chat}': {type(err)} - {err}", file=sys.stderr)

            
