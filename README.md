# Telegram media dump

## Run

- Obtain api key and has https://core.telegram.org/api/obtaining_api_id
- Fill .env file
```shell
APP_API_ID=1234567
APP_API_HASH=dedabeaf1234567
APP_SESSION_FILE=test
```

- run `python3 main.py 12345 ./`

## Usage
```
usage: main.py [-h] [--session SESSION] [--api-id ID] [--api-hash HASH]
               {init,list,backup} ...

Backup script for telegram

options:
  -h, --help            show this help message and exit
  --session SESSION, -s SESSION
                        user session file
  --api-id ID           telegram api id
  --api-hash HASH       telegram api hash

Commands:
  {init,list,backup}
    init                Init or check current session
    list                list user chats
    backup              backup messages from chats
```
