from mongodb.index import (
    get_document_to_add_in_index,
    get_document_to_delete_from_index,
    insert_source,
    delete_source,
)
from middlewares.auth_middleware import admin_token_required
from utils.validators import validateSourceType, validateBodyFields
from index_manager import update_index, delete_document_from_index
from flask import jsonify, request
from app import getFlaskApp

app = getFlaskApp()

@app.route("/index/source/<sourceType>", methods=["POST"])
@admin_token_required
def add_to_index(sourceType):
    body = request.get_json()

    if not validateSourceType(sourceType):
        return "Invalid type (use qa, csv or pdf)", 400

    if not validateBodyFields(body, sourceType):
        return "Invalid body fields", 400

    source = insert_source(sourceType, body)

    source_documents = get_document_to_add_in_index(source.inserted_id)

    for document in source_documents:
        update_index(document)

    return jsonify({}), 200


@app.route("/index/source/<sourceId>", methods=["DELETE"])
@admin_token_required
def delete_from_index(sourceId):
    documents_to_delete = get_document_to_delete_from_index(sourceId)

    for document_id in documents_to_delete:
        delete_document_from_index(document_id)

    delete_source(sourceId)

    return jsonify({}), 204