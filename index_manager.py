from llama_index.core import (
    VectorStoreIndex,
    StorageContext,
    SimpleDirectoryReader,
    Settings
)
from llama_index.core import load_index_from_storage

from utils.vector_database import build_pinecone_vector_store, build_mongo_index
from mongodb.index import getExistingLlamaIndexes

from llama_index.llms.perplexity import Perplexity
import os

llm = Perplexity(
    api_key=os.getenv("PERPLEXITY_API_KEY"), 
    model="mixtral-8x7b-instruct", 
    temperature=0.2
)

Settings.llm = llm
Settings.embed_model = "local:BAAI/bge-small-en-v1.5" 

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