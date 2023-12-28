from bson.objectid import ObjectId
from pymongo import MongoClient

from utils.mongo_parsers import MongoJSONEncoder

import datetime
import json
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


def get_user_chat(userId):
    return db.chats.find_one({"userId": ObjectId(userId)})


def create_chat(userId, role):
    db.chats.insert_one({
        "userId": ObjectId(userId),
        "role": role,
        "createdAt": datetime.datetime.now()
    })

    return db.chats.find_one({"userId": ObjectId(userId)})


def parse_mongo_item_to_json(item):
    return json.loads(json.dumps(item, cls=MongoJSONEncoder))


def retrieve_user_chat_history(chatId):
    """
    Retrieve chat history from MongoDB
    """
    messages = []

    cursor = db.chatmessages.find(
        {"chatId": ObjectId(chatId)}).sort('createdAt', 1)

    for item in cursor:
        messages.append(parse_mongo_item_to_json(item))

    return messages


def insert_message_in_chat(chatId, message, role):

    return db.chatmessages.insert_one({
        "chatId": ObjectId(chatId),
        "message": message,
        "role": role,
        "createdAt": datetime.datetime.now()
    })


def get_chat(chatId):
    return db.chats.find_one({"_id": ObjectId(chatId)})


def update_message_feedback(messageId, feedback):
    """
    Update a message feedback in MongoDB
    """

    db.chatmessages.update_one({"_id": ObjectId(messageId)}, {
                               "$set": {"feedback": feedback}})

    return db.chatmessages.find_one({"_id": ObjectId(messageId)})


def get_chat_history(chatId):
    messages = db.chatmessages.find(
        {"chatId": ObjectId(chatId)}).sort('createdAt', -1).limit(4)

    return list(messages)

def getUserById(id):
    """
    Get an existing user by id
    """

    return db['users'].find_one({'_id': ObjectId(id)})
