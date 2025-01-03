from langchain_community.agent_toolkits import GmailToolkit 
from langchain_community.tools.tavily_search import TavilySearchResults
from dotenv import load_dotenv
load_dotenv()
from langchain_openai import ChatOpenAI
from langchain import hub
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_community.tools.gmail.utils import (
    build_resource_service,
    get_gmail_credentials,
)
from langchain.memory import ConversationBufferMemory
from utils.email_auth import authenticate_gmail


toolkit = GmailToolkit()

credentials = get_gmail_credentials(
    token_file="token.json",
    scopes=["https://mail.google.com/"],
    client_secrets_file="credentials.json",
)
api_resource = build_resource_service(credentials=credentials)
toolkit = GmailToolkit(api_resource=api_resource)

tools = toolkit.get_tools()
llm = ChatOpenAI(temperature=0, streaming=True)
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)


instructions = """You are an Email assistant. You have access to the GmailToolkit and you can access my emails, scan them, send and draft emails, or summarize the content of emails I have. You only follow my instructions and don't complete any actions unless I tell you to do so. You have memory of the conversation history as we go on, and can look back at our previous chats to use as context for future queries."""
base_prompt = hub.pull("langchain-ai/openai-functions-template")
prompt = base_prompt.partial(instructions=instructions)

agent = create_openai_functions_agent(llm, toolkit.get_tools(), prompt)

agent_executor = AgentExecutor(
    agent=agent,
    tools=toolkit.get_tools(),
    verbose=True,
    memory=memory,
)

def main():
    # Authenticate and get the Gmail API service, run the agent
    try:
        authenticate_gmail()
        print("Welcome to the Gmail Assistant CLI!")
        print("Type 'exit' to end the conversation.")
        while True:
            # Get input from the user
            user_input = input("You: ")
            if user_input.lower() == 'exit':
                print("Goodbye!")
                break
            # Run the agent with the user's input
            response = agent_executor.invoke({"input": user_input})
            if isinstance(response, dict) and "output" in response:
                print(f"Assistant: {response['output']}")
            else:
                print(f"Assistant: {response}")
            # print(f"Assistant: {response}")
    except Exception as e:
        print("There was an error in the Gmail authentication process. More info: ", e)

if __name__ == '__main__':
    main()
