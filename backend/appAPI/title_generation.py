from backend.appAPI.base.sonnet_llm import llm_sonnet
from backend.appAPI.base.history_retriever import get_history

from langchain_mongodb import MongoDBChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage
from backend.appAPI.utils import get_secret
import json
import boto3

def title_generator(session_id, query):
    client = boto3.client('bedrock-runtime', region_name='us-west-2', aws_access_key_id=get_secret("AWS_ACCESS_KEY"), aws_secret_access_key = get_secret("AWS_SECRET_ACCESS_KEY"))
  
    system_prompt = """
Role: Title Generation Expert
Task: Create Engaging Titles from User Queries

Output Schema:
Use the format: [Genre | Summarized intent]

Example:
Guide | How to Implement LSTM Models for Predictive Analytics

Note: This optimized schema emphasizes clarity, conciseness, extremely short, and alignment with the user's purpose.
""" 
    messages = [
        {
            "role": "user",
            "content": query
        }
    ]
    body = json.dumps(
    {
        "anthropic_version": 'bedrock-2023-05-31',
        "max_tokens": 200,
        "messages": messages,
        "temperature": 0.0,
        "top_p": 0.7,
        "system": system_prompt
    }
)

    history = get_history(session_id)

    response = client.invoke_model(body=body, modelId="anthropic.claude-3-5-sonnet-20241022-v2:0")

    response_body = json.loads(response.get("body").read())
    result = response_body.get("content") 

    human_message = HumanMessage(content=query, name="User")
    ai_message = AIMessage(content=result)

    # Add human message
    history.add_user_message(human_message)

    # Add ai message
    history.add_ai_message(ai_message)
    return result[0]["text"]