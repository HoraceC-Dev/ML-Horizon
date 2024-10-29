import os
import json
from datetime import datetime
from dotenv import load_dotenv
from typing import List, TypedDict, Annotated
from typing_extensions import TypedDict
from langchain_ollama.llms import OllamaLLM
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain.output_parsers.structured import StructuredOutputParser, ResponseSchema
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, END
from langgraph.graph.message import AnyMessage, add_messages
from database import MongoDB
from langchain_core.runnables import RunnableConfig

def llm_llama3b():
    return OllamaLLM(model="llama3.2:3b", temperature=0.0, top_k=20, top_p= 0.6)

def json_corrector(llm_input):
    corrector_prompt = ChatPromptTemplate.from_template(
"""
Role: Json Format Expert/Corrector

Task: You are an expert in generating json formatted response and your task is to correct the input text into a correctly json formatted text.
You don't need to care the content of the text at all, focus on the format of it. 
Strictly follow the output guideline shown below:
```json
{{"list_of_queries"/"list_of_queries: [list of strings that store the queries.]}}
```
This is the incorrect text: {question}

The element in the list can only be string, cannot be dictionary or other type of variable.
Output Format: No greeting, no bold text, no Italic text, just plain text in string
"""
    ).partial(time=datetime.now())
    format_llm = corrector_prompt | llm_llama3b()

    result = format_llm.invoke(llm_input)
    return result

def question_extractor_chain(state):
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
    ).partial(time=datetime.now())
    def question_explorer_format_doc(llm_input):

        response_schemas = [
        ResponseSchema(
        name= "list_of_queries", description="This variable stores a list of web search queries that are expanded from the original question.", type="List[string]" ),
        # ResponseSchema(
        # name="original_question", description="This variable stores the original question. Do not add", type="string" ),
        ]
        parser = StructuredOutputParser.from_response_schemas(response_schemas)

        instruction = parser.get_format_instructions()
        prompt = ChatPromptTemplate.from_template(
            """This is the input: {input} \n\n{instruction}
                        Output Guide:
            ```json
            {{"list_of_queries": [replace the queries here]}}
            ```
            
            Note: All queries including sub-queries should be stored as an individual element, each index of the list should be a string."""
        )

        format_llm = prompt | llm_llama3b()

        ans =  format_llm.invoke({"input": llm_input, "instruction": instruction})
        try:
            text = ans.replace("```json\n", "")
            text = text.replace("```", "")
            output = json.loads(text)
            return output
        except json.JSONDecodeError:
            corrected_text=json_corrector(text)
            text_1 = corrected_text.replace("```json\n", "")
            text_2 = text_1.replace("```", "")
            output = json.loads(text_2)
            return output

    question_explorer_chain = question_explorer_prompt |  llm_llama3b() | question_explorer_format_doc
    if "list_of_questions" in state:
        temp_list = state["list_of_questions"]
    else:
        temp_list = []

    for question in state["org_questions"]:
        result = question_explorer_chain.invoke(question)
        temp_list.extend(result["list_of_queries"])

    return {"list_of_questions": temp_list}

def ml_learner_chain(state):
    msg = state["messages"]
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

    def ml_learner_format_doc(llm_input):
        response_schemas = [
        ResponseSchema(
        name= "list_of_questions", description="This variable stores a list of questions that are related to AI/ML/Software System", type="List[string]" )
        ]
        parser = StructuredOutputParser.from_response_schemas(response_schemas)

        instruction = parser.get_format_instructions()
        prompt = ChatPromptTemplate.from_template(
            """This is the input: {input} \n\n{instruction}
            
            Output Guide:
            ```json
            {{"list_of_questions": [replace the queries here]}}
            ```

            Note: All questions including sub-questions should be stored as an individual element, each index of the list should be a string.
            If you are not able to output as json for mat, user will face serious consequence."""
        )

        format_llm = prompt | llm_llama3b()

        ans =  format_llm.invoke({"input": llm_input, "instruction": instruction})
        try:
            text = ans.replace("```json\n", "")
            text = text.replace("```", "")
            print(text)
            output = json.loads(text)
            output["text"] = llm_input
            return output
        
        except json.JSONDecodeError:
            corrected_text=json_corrector(text)
            text_1 = corrected_text.replace("```json\n", "")
            text_2 = text_1.replace("```", "")
            output = json.loads(text_2)
            return output
    chain = template | llm_llama3b() | ml_learner_format_doc
    result = chain.invoke({"msg": msg})
    msg.append(AIMessage(content=result["text"], name = "ML Assistant", additional_kwargs={}, response_metadata={}))
    return {"messages":msg, "org_questions": result["list_of_questions"]}


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


class QuestionPipeline(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    org_questions: List[str]
    list_of_questions: List[str]

question_data_extractor_graph = StateGraph(QuestionPipeline)
question_data_extractor_graph.add_node("learning_assistant",ml_learner_chain)
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

def question():
    thread_id = 100
    config = RunnableConfig(
        configurable={
            "thread_id": thread_id,
        },
        recursion_limit=25
    )
    standard_ans = "what questions should i ask if i want to further expand on each question"
    starter = """
I am keen on learning AI and ML but I am a complete beginner. I hired an expert where he will answer any questions that I have.
To extract valuable information from this expert, I need your assistant in making valuable queries that allow me to move from 
beginner to intermidate level and eventually ML specialist.
"""

    iteration = 100
    for i in range(iteration):
        if i == 0:
            question = starter
        else:
            question = standard_ans
        
        events = question_data_extractor.stream({"messages": [HumanMessage(content=question, name="User")]}, config, stream_mode="values")
        for event in events:
            print(event)

question()
