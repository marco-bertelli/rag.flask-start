from llama_index.storage.index_store import MongoIndexStore
from llama_index.vector_stores import PineconeVectorStore

from pinecone import Pinecone
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

pinecone_key = os.getenv("PINECONE_API_KEY")
pinecone_env = os.getenv("PINECONE_ENV")

mongoUri = os.getenv("MONGODB_URI")
mongoDbName = os.getenv("MONGODB_DATABASE")

def build_pinecone_vector_store():
    pc = Pinecone(api_key=pinecone_key, environment=pinecone_env)

    pinecone_index = pc.Index("medium")

    return PineconeVectorStore(pinecone_index=pinecone_index, add_sparse_vector=True,)

def build_mongo_index():
    return MongoIndexStore.from_uri(uri=mongoUri, db_name=mongoDbName)