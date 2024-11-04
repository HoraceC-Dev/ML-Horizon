from typing import List, TypedDict
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

from base.base_llms import llm_sonnet


class AnswerCreator(TypedDict):
    list_of_questions: List[str]
    question_answer_pair: dict

def question_from_content():
    class Schema(BaseModel):
        org_question_answer: str = Field(description= "This variable stores the response to the original question using the information from the given text.")
        additional_quiestion_answer_pairs: dict[str,str] = Field(description="This variable stores the additional questions answer pairs where the question will be the key and the corresponding answer will be the value in the dictionary. Depending on the information given, formulate 2-8 question-answer pairs")

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", """
Role: Question Explorer
             
Task: You will be given a text and a question. Not only you need to formulate an answer for that question but to discover
potential questions that can also be answered from the same text. For example, you have an original question: What is Machine Learning? 
Formulate a response using the information from the text, but also identify any potential questions like: Is Machine Learning a subset of AI? that can also 
be answered from the given text. 
"""),
("human", "This is the information I have for you: {text}"),
("human", "Use the provided information above to answer this question: {question}. Also try to identify potential questions that the given text has the answer to then formulate a response for those questions as well. Extra requirements: Don't use phrases like'Based on the text', 'Accordin to the text', formulate the response in a way where it sounds like you are using your own knowledge.")
        ]
    )

    chain = prompt | llm_sonnet().with_structured_output(Schema)
    
    return chain

