from base.base_llms import llm_llama3b

from langchain_core.prompts import ChatPromptTemplate
from langchain.output_parsers.structured import StructuredOutputParser, ResponseSchema
from langchain_core.output_parsers import JsonOutputParser
import json

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
    )
    format_llm = corrector_prompt | llm_llama3b()

    result = format_llm.invoke(llm_input)
    return result

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
        output = JsonOutputParser(ans)
        return output
    except json.JSONDecodeError:
        corrected_text=json_corrector(ans)
        text_1 = corrected_text.replace("```json\n", "")
        text_2 = text_1.replace("```", "")
        output = json.loads(text_2)
        return output





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
        output = JsonOutputParser(ans)
        return output
    except json.JSONDecodeError:
        corrected_text=json_corrector(ans)
        text_1 = corrected_text.replace("```json\n", "")
        text_2 = text_1.replace("```", "")
        output = json.loads(text_2)
        return output