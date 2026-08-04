from dotenv import load_dotenv
from langchain.agents import create_agent
from tools import tool_get_picture

agent = create_agent(
    model = "openai:gpt-5.4-nano",
    tools = [
        tool_get_picture, 
        {"type": "web_search"},
        
    ]
)

input = {
    "messages": [
        {
            "role": "user",
            "content": "What is yesterday's picture of the day? and tell me like if there any news related to it?",
        }
    ]
}

stream = agent.stream_events(input, version="v3")
for message in stream.messages:
    for delta in message.text:
        print(delta, end="", flush=True)

