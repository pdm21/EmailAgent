from langchain_community.agent_toolkits import GmailToolkit 
toolkit = GmailToolkit()

from langchain_community.tools.gmail.utils import (
    build_resource_service,
    get_gmail_credentials,
)

credentials = get_gmail_credentials(
    token_file="token.json",
    scopes=["https://mail.google.com/"],
    client_secrets_file="credentials.json",
)
api_resource = build_resource_service(credentials=credentials)
toolkit = GmailToolkit(api_resource=api_resource)

tools = toolkit.get_tools()

from dotenv import load_dotenv
import os
dotenv_path = os.getenv("../.env")
load_dotenv(dotenv_path)