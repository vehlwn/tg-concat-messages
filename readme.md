# tg-concat-messages

Telethon-based Telegram client to concatenate consecutive sent text messages.

## Build

```bash
$ cp config-example.ini config.ini
# Get api_id and api_hash from https://core.telegram.org/api/obtaining_api_id
# and change [telegram] section accordingly.
$ python3 login.py
2021-05-30 17:47:04,691 - __main__ [INFO] Connecting
2021-05-30 17:47:06,659 - __main__ [INFO] Not authorized. Sending code request
Enter the code: 123456
2021-05-30 17:47:25,893 - __main__ [INFO] Logged in
# login.py needed for client.session which will be copied into container.
$ docker-compose build && docker-compose up
app_1  | 2021-05-30 13:49:35,905 - __main__ [INFO] Connecting
app_1  | 2021-05-30 13:49:36,965 - __main__ [INFO] Authorized. Wait until disconnected
app_1  | 2021-05-30 13:49:45,264 - __main__ [INFO] EVENT in chat @vehlwn vehlwn
app_1  | 2021-05-30 13:49:45,468 - __main__ [INFO] no
app_1  | 2021-05-30 13:49:45,468 - __main__ [INFO] event.date (2021-05-30 13:49:45+00:00) - last_date (2021-05-30 12:28:11+00:00) > 0:01:00
app_1  | 2021-05-30 13:49:52,020 - __main__ [INFO] EVENT in chat @vehlwn vehlwn
app_1  | 2021-05-30 13:49:52,225 - __main__ [INFO] Concating
app_1  | 2021-05-30 13:49:52,225 - __main__ [INFO] last_message.text='7', event.text='8'
app_1  | 2021-05-30 13:49:59,186 - __main__ [INFO] EVENT in chat @vehlwn vehlwn
app_1  | 2021-05-30 13:49:59,337 - __main__ [INFO] Concating
app_1  | 2021-05-30 13:49:59,337 - __main__ [INFO] last_message.text='7\n8', event.text='9'

# Alternative without docker:
$ pip3 install -r requirements.txt --user
$ python3 main.py
```
