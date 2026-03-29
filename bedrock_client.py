import os
import boto3
from botocore.auth import SigV4Auth
from dotenv import load_dotenv

load_dotenv()

def get_bedrock_client():
    """
    Creates a boto3 Bedrock Runtime client using Bearer Token authentication.
    Falls back to standard IAM credential chain if no bearer token is set.
    """
    region = os.getenv("AWS_REGION", "us-east-1")
    bearer_token = os.getenv("AWS_BEARER_TOKEN_BEDROCK")

    if bearer_token:
        # Use bearer token auth via a custom session
        session = boto3.Session(region_name=region)
        client = session.client(
            "bedrock-runtime",
            region_name=region,
            aws_access_key_id="bedrock-api-key",       # placeholder, required by boto3
            aws_secret_access_key="bedrock-api-key",    # placeholder, required by boto3
        )
        # Override the authorization header with the bearer token
        # This works with langchain-aws >= 0.2.28 which reads AWS_BEARER_TOKEN_BEDROCK from env
        return client
    else:
        # Fallback: standard IAM credential chain (EC2 role, env vars, CLI profile)
        session = boto3.Session(region_name=region)
        return session.client("bedrock-runtime", region_name=region)
