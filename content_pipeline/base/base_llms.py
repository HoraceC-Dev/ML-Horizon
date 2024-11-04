import os
from dotenv import load_dotenv
from langchain_ollama.llms import OllamaLLM
from langchain_aws import ChatBedrock

def llm_sonnet():
    load_dotenv()
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_ACCESS_KEY= os.getenv("AWS_ACCESS_KEY")
    llm = ChatBedrock(
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        model_id="anthropic.claude-3-5-sonnet-20241022-v2:0",
        model_kwargs=dict(temperature=0),
        region="us-west-2"
    )

    return llm

def llm_llama3b():
    return OllamaLLM(model="llama3.2:latest", temperature=0.0, top_k=20, top_p= 0.6)