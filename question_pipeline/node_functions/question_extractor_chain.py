from base.base_llms import llm_llama3b
from node_functions.formatting_chains import question_explorer_format_doc

from langchain_core.prompts import ChatPromptTemplate

def question_extractor_chain():
    question_explorer_prompt = ChatPromptTemplate.from_template(
"""
Role: Search Engine Question Optimizer Robot

Scenario:
User has a question that he/she wants to know from the internet not from you.

Task: Base on user question, try to dive deeper to the intent, the technical aspects of the query, and optimize user's question for search engine.
You are not responsible in answering user's question. You need to generate 10 search query based on the user's question
that allows user to obtain the best informtaion from the internet through the search engine, NOT FROM YOU. 
The generated questions should not enquire user to input information, instead, they should be ready for search engine. 
Optimize all the questions for search engine that enables user to obtain high quality information. 

This is the user's question: {question}

Instructions:
Think step by step to generate 10 search engine queries at the best of your ability.
Assume user will copy and paste directly without any changes, so there shouldn't be [] variable that allows user to change.

Output Format: No greeting, no bold text, no Italic text, just plain text in string, no number index
"""
    )


    question_explorer_chain = question_explorer_prompt |  llm_llama3b() | question_explorer_format_doc
    return question_explorer_chain

def question_extractor_node_function(state):
    temp_list = []

    if "list_of_questions" in state:
        temp_list = state["list_of_questions"]
    else:
        temp_list = []

    for question in state["org_questions"]:
        result = question_extractor_chain().invoke(question)
        temp_list.extend(result["list_of_queries"])

    return {"list_of_questions": temp_list}