from flask_limiter.util import get_remote_address

from flask_limiter import Limiter
from flask_cors import CORS
from flask import Flask

import os

app = Flask(__name__)

app.config["MONGO_URI"] = os.getenv("MONGODB_URI")
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config['CORS_HEADERS'] = 'Content-Type'

cors = CORS(app)

limiter = Limiter(
    get_remote_address,
    app=app,
    storage_uri=os.getenv("MONGODB_URI")
)


def getFlaskApp():
    return app


def getLimiter():
    return limiter
