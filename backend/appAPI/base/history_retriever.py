from langchain_mongodb import MongoDBChatMessageHistory
from backend.appAPI.utils  import get_secret


def get_history(session_id):
    MONGODB_CONNECTION_STRING_URL= get_secret("mongodb_connection_url")

    history = MongoDBChatMessageHistory(
            session_id=session_id,
            connection_string=MONGODB_CONNECTION_STRING_URL,
            database_name="MLHorizon",
            collection_name="MessageStore",
        )
    
    return history
