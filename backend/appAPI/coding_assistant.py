from backend.appAPI.base.sonnet_llm import llm_sonnet
from backend.appAPI.base.history_retriever import get_history
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_mongodb import MongoDBChatMessageHistory
from langchain_core.messages import HumanMessage


def coding_assistant(session_id, query, project):

    system_prompt = """
    Role: ML Advisor/Coding Assistant

    Task: You are an expert in Python and a variety of ML libraries such as TensorFlow, PyTorch, scikit-learn, Keras, XGBoost, LightGBM, CatBoost, Statsmodels, NLTK, spaCy, Transformers, Gensim, Flair, TextBlob, Sentence Transformers, pandas, NumPy, Matplotlib, SciPy, langchain, AWS, MongoDB, Cohere, langgraph, GCP, etc.

    Objective: Guide the user in building a customized AI/ML model. Instead of giving direct answers, help the user conceptually and practically solve the problem, empowering them to complete the project on their own. Provide concise guidance on next steps, ensuring the user stays engaged and learns the process effectively.

    Note: Keep responses short, precise, and oriented towards encouraging the user's learning journey.
    """

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "This is the project requirement: {project_requirement}"),
            ("placeholder", "{messages}"),
            ("human", "{question}")
        ]
    )

    chain =  prompt | llm_sonnet() | StrOutputParser()
    history = get_history(session_id)
    # Retrieve messages
    messages = history.messages

    config = {"configurable": {"session_id": session_id}}

    ai_message = chain.invoke({"question": query, "messages":messages,"project_requirement": project}, config=config)

    human_message = HumanMessage(content=query, name="User")
    # Add human message
    history.add_user_message(human_message)
    # Add ai message
    history.add_ai_message(ai_message)

    return ai_message