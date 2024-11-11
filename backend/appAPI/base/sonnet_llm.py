from langchain_aws import ChatBedrock
from backend.appAPI.utils import get_secret



def llm_sonnet():
    llm = ChatBedrock(
        aws_access_key_id=get_secret("AWS_ACCESS_KEY"),
        aws_secret_access_key=get_secret("AWS_SECRET_ACCESS_KEY"),
        model_id="anthropic.claude-3-5-sonnet-20241022-v2:0",
        model_kwargs=dict(temperature=0),
        region="us-west-2"
    )

    return llm
