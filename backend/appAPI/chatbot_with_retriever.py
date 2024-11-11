from backend.appAPI.base.sonnet_llm import llm_sonnet
from backend.appAPI.base.base_embedding import get_embedding_model
from backend.appAPI.mongodb_text_retriever import MongoDBKeywordRetriever

from langchain_mongodb import MongoDBAtlasVectorSearch
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from langchain_core.prompts import ChatPromptTemplate
from langchain.retrievers.contextual_compression import ContextualCompressionRetriever
from langchain_cohere import CohereRerank
from langchain_community.llms import Cohere
from langchain.retrievers import EnsembleRetriever
from langchain_core.runnables import RunnablePassthrough, RunnableMap
from langchain_core.output_parsers import StrOutputParser
from langchain_mongodb import MongoDBChatMessageHistory
from langchain_core.messages import HumanMessage
from backend.appAPI.utils import get_secret
import os

def chatbot_knowledge_retriever(session_id, query):
    print(session_id)
    MONGODB_CONNECTION_STRING_URL= get_secret("mongodb_connection_url")
    client = MongoClient(MONGODB_CONNECTION_STRING_URL, server_api=ServerApi('1'))

    embeddings = get_embedding_model()

    vector_store = MongoDBAtlasVectorSearch(
        collection=client["MLHorizon"].MLKnowledgeBase,
        embedding=embeddings,
        index_name="vector_index",
        relevance_score_fn="cosine",
    )
    semantic_retriever = vector_store.as_retriever(include_metadata=True, metadata_key ='Category',search_kwargs={"k": 85})
    keyword_retriever = MongoDBKeywordRetriever(collection=client["MLHorizon"].MLKnowledgeBase, top_k=2)

    compressor = CohereRerank(model="rerank-english-v3.0",cohere_api_key= get_secret("CO_API_KEY") , top_n=2)
    compression_retriever= ContextualCompressionRetriever(
        base_compressor=compressor, base_retriever=semantic_retriever
    )


    retriever = EnsembleRetriever(     
            retrievers=[compression_retriever, keyword_retriever], weights=[0.5, 0.5]
    )
    
    def format_docs(all_documents):
        content = ""
        try:
            for index, doc in enumerate(all_documents):
                if doc.metadata["content"] != None:
                    content = content + f"This is the {index+1} source\n" + str(doc.metadata["content"]) + "\nThese are the websites from this source: " + str(doc.metadata["websites"])
        except:
            pass
        
        return content

    system_prompt = """
    Role: Expert ML & AI Chatbot

    Task: You are incredible in the fields of AI and Machine Leraning whic allows you to answer any relevant questions, including machine learning applications, different algorithms, technical coding problems, and all the theories. 
    As a result, you are not suppose to provide any assistance to user when the user is not asking questions that are relevant AI/ML. 
    To assist you in providing the best response to user, the following are some aid information:

    {context}

    Using the provided informmation incorperating with your own knowledge, please provide a clear and precise response to user.
    Note: If no information is provided or the information is not helpful, you can solely apply your intellegence to generate a response, however, if you use any information from the aid text, ensure the source of infromation is attached at the end of the message(e.g. Source: url1, url2). 

    Output Guideline: Enssure your response is short, precise, and informative. 
    """

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("placeholder", "{messages}"),
            ("human", "{question}")
        ]
    )

    chain = RunnableMap({
    "context": RunnablePassthrough().pick("question") | retriever | format_docs,
    "question": RunnablePassthrough().pick("question"),
    "messages": RunnablePassthrough().pick("messages"),
    }) | prompt | llm_sonnet() | StrOutputParser()

    history = MongoDBChatMessageHistory(
        session_id=session_id,
        connection_string=MONGODB_CONNECTION_STRING_URL,
        database_name="MLHorizon",
        collection_name="MessageStore",
    )

    # Retrieve messages
    messages = history.messages

    config = {"configurable": {"session_id": session_id}}

    ai_message = chain.invoke({"question": query, "messages":messages}, config=config)
    human_message = HumanMessage(content=query, name="User")
    history.add_user_message(human_message)
    history.add_ai_message(ai_message)

    return ai_message
 