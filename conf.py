import os

from dotenv import load_dotenv

def load_env():
    for env_file in ('.env', '.flaskenv'):
        env = os.path.join(os.getcwd(), env_file)

        if os.path.exists(env):
            load_dotenv(env)