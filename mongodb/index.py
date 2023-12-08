from pymongo import MongoClient

import os

db = MongoClient(host=os.getenv("MONGODB_URI")).get_database()

def getExistingLlamaIndexes():
    """
    Get the existing Llama Indexes
    """

    indexes = []

    cursor = db['index_store/data'].find({})

    for item in cursor:
        indexes.append(item)

    return indexes