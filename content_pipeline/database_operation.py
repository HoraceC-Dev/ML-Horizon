import os
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from base.base_embedding import get_embedding_model


class ContetIngestionMongoDB():
    
    def _get_client(self):
        load_dotenv()

        MONGODB_CONNECTION_STRING_URL= os.getenv("MONGODB_CONNECTION_STRING_URL")

        client = MongoClient(MONGODB_CONNECTION_STRING_URL, server_api=ServerApi('1'))

        return client

    def update_database(self, list_of_org_questions, list_of_expanded_questions_answers):

        client = self._get_client()

        db = client["MLHorizon"]
        
        for question_doc in list_of_org_questions:
            # Search it doc to update
            query = {
                "_id": question_doc["doc"]["_id"]
            }
            # Define update operation
            update_operation ={
                '$set': {"content" : question_doc["ans"],
                            "websites" : question_doc["web"]}
            }

            db.MLKnowledgeBase.update_one(query, update_operation)

        embeddings = get_embedding_model()
        for question_doc in list_of_expanded_questions_answers:
            
            question = question_doc["question"]

            embedding = embeddings.embed_query(question)

            db.MLKnowledgeBase.insert_one({
                "text": question,
                "embedding": embedding,
                "content": question_doc["ans"],
                "websites": question_doc["web"]
            })

        client.close()

    def store_web_info(self,web_dict):
        client = self._get_client()

        db = client["MLHorizon"]
        collection = db.MLWebInfo
        collection.insert_one(web_dict)
        client.close()

    def question_retriever(self):

        client = self._get_client()

        collection = client["MLHorizon"].MLKnowledgeBase
        
        query = {
            "content": None
        }
        filtered_documents = list(collection.find(query))

        client.close()

        return filtered_documents


