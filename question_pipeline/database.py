from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pprint import pprint
import os
from dotenv import load_dotenv
from base.base_embedding import get_embedding_model
from langchain_mongodb import MongoDBAtlasVectorSearch
from uuid import uuid4
from langchain_core.documents import Document

class MongoDB():
    def __init__(self, user_name, password):
        self.user_name = user_name
        self.password = password
        
        uri = f"mongodb+srv://{self.user_name}:{self.password}@mldatabase.36zie.mongodb.net/?retryWrites=true&w=majority&appName=MLDatabase"

        client = MongoClient(uri, server_api=ServerApi('1'))

        try:
            client.admin.command('ping')
            self.client = client
        except Exception as e:
            self.client = e 
            print(e)

    def _get_collection(self):
        mongo_client = self.client
        client = mongo_client['MLHorizon']
        collection = client.MLKnowledgeBase
        return collection

    def _get_vectorstore(self):
        embeddings = get_embedding_model()
        vector_store = MongoDBAtlasVectorSearch(
            collection=self._get_collection("MLKnowledgeBase"),
            embedding=embeddings,
            index_name="vector_index",
            relevance_score_fn="cosine",
        )
        return vector_store

    def _vector_search_aggregation(self, query):
        embeddings = get_embedding_model()
        embedding = embeddings.embed_query(query)
        pipeline = [
        {
            '$vectorSearch': {
            'index': 'vector_index', 
            'path': 'embedding', 
            'queryVector': embedding,
            'numCandidates': 3, 
            'limit': 3
            }
        }, {
            '$project': {
            '_id': 0, 
            'text': 1, 
            'score': {
                '$meta': 'vectorSearchScore'
            }
            }
        }
        ]
        collection = self._get_collection("MLKnowledgeBase")
        result = collection.aggregate(pipeline)
        for doc in result:
            if doc["score"] >= 0.90:
                return False
        return True

    def add_question(self, questions):
        vector_store = self._get_vectorstore()
        documents = []
        for question in questions:
            if self._vector_search_aggregation(query=question):
                document = Document(
                    page_content=question,
                    metadata={
                        "content": None,
                        'websites': None
                    }
                )
                documents.append(document)
        uuids = [str(uuid4()) for _ in range(len(documents))]
        vector_store.add_documents(documents=documents, ids=uuids)

    def close_connection(self):
        if self.client:
            self.client.close()
            print("MongoDB connection closed.")
        else:
            print("No MongoDB connection to close.")

