import argparse
import sys
from environs import Env
from telethon import TelegramClient, events, sync

import commands

env = Env()
env.read_env()  # read .env file, if it exists

p = argparse.ArgumentParser(description='Backup script for telegram')
sp = p.add_subparsers(title='Commands')

p.add_argument('--session', '-s', metavar='SESSION', help="user session file",
               default="anon", required=not env.str('APP_SESSION_FILE'))
p.add_argument('--api-id', metavar='ID', help="telegram api id", default="anon", required=not env.str('APP_API_ID'))
p.add_argument('--api-hash', metavar='HASH', help="telegram api hash",
               default="anon", required=not env.str('APP_API_HASH'))


async def doInitCmd(client, args):
    await commands.initCmd(client)

spInit = sp.add_parser('init', help="Init or check current session")
spInit.set_defaults(func=doInitCmd)


async def doListCmd(client, args):
    await commands.listChats(client)

spList = sp.add_parser('list', help="list user chats")
spList.set_defaults(func=doListCmd)


async def doBackupCmd(client, args):
    await commands.backup(client, [int(i) for i in args.ids], args.output, 
                          filename_tpl=args.template,
                          mime_types=args.mime
                          )

spBackup = sp.add_parser('backup', help="backup messages from chats")
spBackup.add_argument('ids', metavar='CHAT_ID', nargs='*')
spBackup.add_argument('output', metavar='OUTPUT')
spBackup.add_argument('--template', '-t', metavar='TPL', nargs=1, default="{chat}_{cstitle}/{chat}_{date}{ext}")
spBackup.add_argument('--mime', '-m', metavar='MIME', nargs='*', default=[
                                                                    'image/jpeg',
                                                                    'video/mp4'
                                                                    ]
                      )
spBackup.set_defaults(func=doBackupCmd)

    # filename_tpl = "{chat}_{cstitle}/{chat}_{date}{ext}"

    # mimeTypeWhiteList = [
    #     'image/jpeg',
    #     'video/mp4'
    # ]

p.set_defaults(
    session=env.str('APP_SESSION_FILE'),
    api_id=env.int('APP_API_ID'),
    api_hash=env.str('APP_API_HASH')
)

args = p.parse_args()

client = TelegramClient(args.session, args.api_id, args.api_hash)

async def main():
    await args.func(client, args)
    print('Exit')

with client:
    client.loop.run_until_complete(main())
