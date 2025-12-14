from llama_index.core import (
    VectorStoreIndex,
    StorageContext,
    SimpleDirectoryReader,
    Settings
)
from llama_index.embeddings.sagemaker_endpoint import SageMakerEmbedding
from llama_index.llms.sagemaker_endpoint import SageMakerLLM
from llama_index.core import load_index_from_storage

from utils.vector_database import build_pinecone_vector_store, build_mongo_index
from mongodb.index import getExistingLlamaIndexes

from handlers.llm_handler import MistralIOHandler, messages_to_prompt_mistral
from handlers.embeddings_handler import BGEHandler

import os

content_handler = BGEHandler()
ministral_handler = MistralIOHandler()

ENDPOINT_NAME = os.environ.get("SAGEMAKER_ENDPOINT_NAME")
EMBED_ENDPOINT_NAME = os.environ.get("SAGEMAKER_EMBED_ENDPOINT_NAME")
REGION_NAME = os.environ.get("AWS_REGION_NAME", "eu-west-1")

llm = SageMakerLLM(
    endpoint_name=ENDPOINT_NAME,
    content_handler=ministral_handler,
    aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    aws_region_name=REGION_NAME,
    messages_to_prompt=messages_to_prompt_mistral
)

embed_model = SageMakerEmbedding(
    endpoint_name=EMBED_ENDPOINT_NAME,
    content_handler=content_handler,
    region_name=REGION_NAME,
)

Settings.llm = llm
Settings.embed_model = embed_model

index_store = build_mongo_index()
vector_store = build_pinecone_vector_store()

storage_context = StorageContext.from_defaults(
    index_store=index_store,
    vector_store=vector_store
)

mongoIndex = None

def initialize_index():
    existing_indexes = getExistingLlamaIndexes()

    global mongoIndex

    if len(existing_indexes) > 0:
        print("Loading existing index...")

        mongoIndex = load_index_from_storage(
            storage_context=storage_context,
            index_id='mongo-index',
        )

        return createQueryEngine(mongoIndex)
    else:
        print("Building index...")

        mongoIndex = buildVectorIndex()

        return createQueryEngine(mongoIndex)


def createQueryEngine(index):
    return index.as_retriever(top_k=10)

def update_index(doc):
    mongoIndex.insert(doc)


def delete_document_from_index(doc_id):
    mongoIndex.delete_ref_doc(doc_id)


def buildVectorIndex():
    reader = SimpleDirectoryReader(
        input_files=["./data/rules.pdf"]
    )
    
    documents = reader.load_data()

    index = VectorStoreIndex.from_documents(
        documents,
        storage_context=storage_context
    )

    index.set_index_id("mongo-index")

    return index