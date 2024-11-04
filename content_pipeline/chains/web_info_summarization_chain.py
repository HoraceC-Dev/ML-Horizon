from langchain_core.prompts import ChatPromptTemplate

from base.base_llms import llm_llama3b

def web_content_summarization_chain():
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", """
Role: Formatting Expert
             
Task: You will be given a long text formatted in an unqiue way. Your primary task is to reformat the text into detail, precise, and legible format.
The length of the output can be anywhere from 3 parahgraphs to 10 paragraphs depending on the context. Keep in mind that the technical explaination of some concepts are keys,
make sure to include all the technical aspect of the orginal content.
"""),
("human", "Please reformat the document in detailed paragraphs so it is more legible.\n Title: {title}\n\n URL Available:{url}\n\n Content:{description}")
        ]
    )
    format_text_chain = prompt | llm_llama3b()
    
    return format_text_chain
