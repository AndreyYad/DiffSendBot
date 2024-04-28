from json import load

with open('config.json', encoding='utf-8') as file:
    config = load(file)

TOKEN = config.get('token')
CHAT_ID = config.get('chat_id')
RECIPIENTS = config.get('recipients')

BOT_ID = int(TOKEN[:TOKEN.find(':')])