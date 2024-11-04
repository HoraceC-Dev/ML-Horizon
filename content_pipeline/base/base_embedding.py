from dotenv import load_dotenv
import os
import boto3
from langchain_aws import BedrockEmbeddings

def get_bedrock_client():
    load_dotenv()

    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")

    session = boto3.Session(
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name='us-west-2'
    )

    bedrock_client = session.client(service_name='bedrock-runtime')

    return bedrock_client


def get_embedding_model(model_id="amazon.titan-embed-text-v2:0"):
    bedrock_client = get_bedrock_client()

    embeddings = BedrockEmbeddings(
        client=bedrock_client,
        region_name="us-west-2",
        model_id=model_id,
    )

    return embeddings

