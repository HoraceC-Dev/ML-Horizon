from typing import List, TypedDict, Annotated
from langgraph.graph.message import AnyMessage, add_messages

class QuestionPipeline(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    org_questions: List[str]
    list_of_questions: List[str]

