from mongodb.index import (
    get_user_chat,
    create_chat,
    parse_mongo_item_to_json,
    retrieve_user_chat_history,
    insert_message_in_chat,
    update_message_feedback,
)

from middlewares.auth_middleware import user_token_required
from utils.chat_history_parser import retrieve_chat_history
from llama_index.chat_engine import ContextChatEngine
from llama_index.memory import ChatMemoryBuffer
from index_manager import initialize_index, get_service_context
from bson.objectid import ObjectId
from flask import request, jsonify, Response
from app import getFlaskApp, getLimiter

app = getFlaskApp()
limiter = getLimiter()

query_engine = initialize_index()
service_context = get_service_context()


@app.route("/chats/me", methods=["GET"])
@limiter.limit("5 per minute")
@user_token_required
def get_my_chat(current_user):
    chat = get_user_chat(current_user["_id"])

    if chat is None:
        chat = create_chat(current_user["_id"], current_user["role"])

    return jsonify(parse_mongo_item_to_json(chat)), 200


@app.route("/chats/me/history", methods=["GET"])
@limiter.limit("15 per minute")
@user_token_required
def get_my_chat_history(current_user):
    chat = get_user_chat(current_user["_id"])
    chat_history = retrieve_user_chat_history(str(chat['_id']))

    return jsonify(chat_history), 200


@app.route("/chats/guest", methods=["GET"])
@limiter.limit("5 per minute")
def get_guest_chat():
    chat = create_chat(ObjectId(), "guest")

    return jsonify({'_id': str(chat['_id'])}), 200


@app.route("/chats/message/<messageId>/feedback", methods=["PUT"])
def set_message_feedback(messageId):

    body = request.get_json()

    if 'feedback' not in body:
        return "Invalid body set feedback field with value good | bad", 400

    feedback = body["feedback"]

    if feedback is None:
        return "Invalid feedback (use good or bad)", 400

    if feedback not in ['good', 'bad']:
        return "Invalid feedback (use good or bad)", 400

    updated_message = update_message_feedback(messageId, feedback)

    del updated_message["_id"]
    del updated_message["chatId"]

    return updated_message, 200


@app.route("/chats/<chatId>/answer", methods=["GET"])
@limiter.limit("10 per minute")
def query_index(chatId):
    answer = request.args.get('answer')

    if answer is None:
        return "No text found, please include a ?answer=example parameter in the URL", 400

    history = retrieve_chat_history(chatId)

    memory = ChatMemoryBuffer.from_defaults(
        chat_history=history
    )

    # re-add history when fix perplexity API problem with llama_index guys
    chat_engine = ContextChatEngine.from_defaults(
        retriever=query_engine,
        service_context=service_context,
        system_prompt=(
            """\
            You are a chatbot. You MUST NOT provide any information unless it is in the Context or previous messages or general conversation. If the user ask something you don't know, say that you cannot answer. \
            you MUST keep the answers short and simple. \
            """
        ),
        verbose=True
    )

    response = chat_engine.stream_chat(message=answer)

    return Response(send_and_save_response(response, chatId, answer), mimetype='application/json')


def send_and_save_response(response, chatId, query_text):
    for token in response.response_gen:
        yield token

    user_message = insert_message_in_chat(chatId, query_text, 'user')
    bot_response = insert_message_in_chat(chatId, str(response), 'assistant')

    json_bosy = {
        "user_message": str(user_message.inserted_id),
        "bot_response": str(bot_response.inserted_id)
    }

    yield f" {json_bosy}"
