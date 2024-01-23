from conf import load_env

load_env()

print('Loading Flask app...')

from apis import chats
from apis import sources

from app import getFlaskApp

app = getFlaskApp()