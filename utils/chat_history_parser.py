from llama_index.llms import ChatMessage, MessageRole
from mongodb.index import get_chat_history

def retrieve_chat_history(chatId):
    """
    Retrieve chat history from MongoDB
    """

    chat_history = get_chat_history(chatId)

    return convertMongoChat(chat_history)

def convertMongoChat(chat_history):
    """
    Convert chat history from MongoDB to the format required by the chat engine
    """

    chat = []

    for message in chat_history:
        chat.append(ChatMessage(
        role=getHistoryRole(message), 
        content=message['message'],
    ))

    return chat

def getHistoryRole(message):
    """
    Get the role of the message in the chat history
    """

    if message['role'] == 'user':
        return MessageRole.USER
    else:
        return MessageRole.ASSISTANT
