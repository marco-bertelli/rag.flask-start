from index_manager import initialize_index, get_service_context
from flask import request, jsonify
from app import getFlaskApp, getLimiter

app = getFlaskApp()
limiter = getLimiter()

query_engine = initialize_index()

@app.route("/chats/<chatId>/answer", methods=["GET"])
@limiter.limit("10 per minute")
def query_index(chatId):
    answer = request.args.get('answer')

    result = query_engine.query(answer)

    return jsonify({
        "answer": result.response,
        "sources": result.get_formatted_sources()
    })
