from datetime import datetime, date

from bson import ObjectId
from json import JSONEncoder


class MongoJSONEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, (datetime, date)):
            return o.isoformat(timespec='milliseconds')
        if isinstance(o, ObjectId):
            return str(o)
        else:
            return super().default(o)