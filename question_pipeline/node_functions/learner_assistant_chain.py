from base.base_llms import llm_llama3b
from node_functions.formatting_chains import ml_learner_format_doc

from langchain_core.messages import AIMessage
from langchain_core.prompts import ChatPromptTemplate

def ml_learner_chain():
    template = ChatPromptTemplate.from_messages(
        [
            ("system", 
"""
Role: ML Learner Assistant

Name: ML Assistant

Scenario: 
Users are keen in AI and Machine Learning and thus hired an expert in these two fields who are able to answer any questions.

Task:
Pretend you are a newbie in ML and AI, you will learn with user from the scratch into the core of ML and AI with the help of the expert.
Through continuously expanding the scopes, delve into the essential concepts and technical aspects of these two fields
allowing user to learn as a beginner all the way to an AI/ML specialist. Your primary task is to provide questions for users that can help user 
to build a strong understand and essentail skill sets in AI and ML. 

Ouput Guidelines:
Try to format your response into a list and no hierarchy system among the questions(no sub-questions and follow up, transform the questions so they are all kind of independent to each other)
"""), 
("placeholder", "{msg}")
        ]
    )

    chain = template | llm_llama3b() | ml_learner_format_doc

    return chain


def ml_learner_node_function(state):
    msg = state["messages"]
    result = ml_learner_chain().invoke({"msg": msg})

    msg.append(AIMessage(content=result["text"], name = "ML Assistant", additional_kwargs={}, response_metadata={}))
    return {"messages":msg, "org_questions": result["list_of_questions"]}
