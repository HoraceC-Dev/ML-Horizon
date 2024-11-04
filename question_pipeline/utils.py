from QuestionPipeline import QuestionPipeline
from node_functions import learner_assistant_chain,question_extractor_chain
from database import MongoDB

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, END
from dotenv import load_dotenv
import os

def synchronization(state):
    load_dotenv()
    MONGODB_USER_NAME = os.getenv("MONGODB_USER_NAME")
    MONGODB_USER_PASSWORD= os.getenv("MONGODB_USER_PASSWORD")

    db = MongoDB(MONGODB_USER_NAME, MONGODB_USER_PASSWORD)
    org_questions = state["org_questions"]
    expanded_questions = state["list_of_questions"]

    total = org_questions + expanded_questions
    db.add_question(total)
    db.close_connection()
    if len(state["messages"]) > 20:
        state["messages"] = state["messages"][2:]
    return {"messages": state["messages"], "list_of_questions": [], "org_questions": []}

def graph_formation():

    question_data_extractor_graph = StateGraph(QuestionPipeline)
    question_data_extractor_graph.add_node("learning_assistant",learner_assistant_chain)
    question_data_extractor_graph.add_node("question_expander",question_extractor_chain)
    question_data_extractor_graph.add_node("database_synchronization", synchronization)

    question_data_extractor_graph.set_entry_point("learning_assistant")
    question_data_extractor_graph.add_edge("learning_assistant", "question_expander")
    question_data_extractor_graph.add_edge("question_expander", "database_synchronization")
    question_data_extractor_graph.add_edge("database_synchronization", END)


    memory = MemorySaver()

    question_data_extractor = question_data_extractor_graph.compile(
        checkpointer = memory,
        debug = True
    )

    return question_data_extractor