import argparse
import os.path
from datetime import datetime
from telethon import TelegramClient, types, functions


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


async def backup(client: TelegramClient, chats: list[int], output: str):
    # Do simple backup
    print('Backuping chats', chats, ' to ', output)

    # chatid_datatime.ext

    for chat in chats:
        async for m in client.iter_messages(chat):
            if (m.media):
                if isinstance(m.media, types.MessageMediaPhoto):
                    filename = str(chat) + '_' + m.date.strftime("%Y-%d-%mT%H:%M:%S") + '.jpg'
                    fullPath = os.path.join(output, filename)
                    if not os.path.isfile(fullPath):
                        await client.download_media(m, fullPath)
                        print(filename)

    pass
