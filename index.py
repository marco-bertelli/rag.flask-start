from conf import load_env

load_env()

print('Loading Flask app...')

from apis import _chats
from apis import _sources

from app import getFlaskApp

app = getFlaskApp()