from backend.appAPI.base.sonnet_llm import llm_sonnet
from backend.appAPI.base.history_retriever import get_history

from langchain_core.messages import HumanMessage, AIMessage
from backend.appAPI.utils import get_secret
import json
import boto3

def project_generator(session_id, **kwargs):
    client = boto3.client('bedrock-runtime', region_name='us-west-2', aws_access_key_id=get_secret("AWS_ACCESS_KEY"), aws_secret_access_key = get_secret("AWS_SECRET_ACCESS_KEY"))

    requirement = ""
    # kwargs is a dictionary containing all keyword arguments passed to the function
    for key, value in kwargs.items():
        requirement = requirement + f"{key}: {value}"
        print(f"{key}: {value}")
        

    system_prompt = """
Role: ML/AI Project Creator

Task: Create a python-based mini-project tailored to the user's knowledge level and interest in Machine Learning/AI. The project should be engaging and help the user progressively build their skills.

Objective: Design a customized hands-on ML/AI project that effectively guides the user through key concepts, enabling active learning and practical experience.
Also, please provide the requirement and dataset generation with python but not the solution to the project. The project is meant to let the user to complete instead of copy and paste from you.

Additional Instruction: Please also create the dataset of the project if that is possible, limit the number of data point to less than 100. If it is impossible for you to create a dataset for example, speech, image...etc. inform the user that you will create the project still however, the user needs to find a dataset by themselves. 
Think step by step:
1. What type and level of this project will be?
2. What algorithm should this project use?
3. What are the requirements of this project?
4. Can I create the dataset? 
    """
    query = 'Create you create a project for me? This is my background to assist you in creating my cutomized project.\n' + requirement 
    messages = [
        {
            "role": "user",
            "content": query
        }
    ]
    body = json.dumps(
    {
        "anthropic_version": 'bedrock-2023-05-31',
        "max_tokens": 3000,
        "messages": messages,
        "temperature": 0.0,
        "top_p": 0.8,
        "system": system_prompt
    }
)

    history = get_history(session_id)

    response = client.invoke_model(body=body, modelId="anthropic.claude-3-5-sonnet-20241022-v2:0")

    response_body = json.loads(response.get("body").read())

    human_message = HumanMessage(content=query, name="User")
    ai_message = AIMessage(content=response_body.get("content"))

    # Add human message
    history.add_user_message(human_message)

    # Add ai message
    history.add_ai_message(ai_message)
    result = response_body.get("content")
    return result[0]["text"] 
