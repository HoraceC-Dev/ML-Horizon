from utils import graph_formation

from langchain_core.runnables import RunnableConfig
from langchain_core.messages import HumanMessage

def main():

    graph = graph_formation

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
        
        events = graph.stream({"messages": [HumanMessage(content=question, name="User")]}, config, stream_mode="values")
        for event in events:
            print(event)