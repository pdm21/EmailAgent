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

from langchain_community.tools.tavily_search import TavilySearchResults
# from dotenv import load_dotenv
# import os
# dotenv_path = ".env"
# load_dotenv(dotenv_path)
from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
llm = ChatOpenAI(temperature=0, streaming=True)

from langchain import hub
from langchain.agents import AgentExecutor, create_openai_functions_agent

instructions = """You are an assistant."""
base_prompt = hub.pull("langchain-ai/openai-functions-template")
prompt = base_prompt.partial(instructions=instructions)

agent = create_openai_functions_agent(llm, toolkit.get_tools(), prompt)

agent_executor = AgentExecutor(
    agent=agent,
    tools=toolkit.get_tools(),
    verbose=True,
)

agent_executor.invoke(
    {
        "input": "Create a test mail with text 'An AI Agent created and sent this email, hey Sydney' and send it to the email 'sklepper@hamilton.edu'."
    }
)