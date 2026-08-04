from langchain.agents import create_agent
from tools import tool_get_picture
from bedrock_agentcore.runtime import BedrockAgentCoreApp

app = BedrockAgentCoreApp()

agent = create_agent(
    model = "openai:gpt-5.4-nano",
    tools = [
        tool_get_picture, 
        {"type": "web_search"},
    ]
)  

@app.entrypoint
def invoke_agent(payload, context):
    if not isinstance(payload.get("prompt"), str) or not payload.get("prompt").strip():
        raise ValueError("payload must include a non-empty prompt.")
    result = agent.invoke({
            "messages": [
                {
                    "role": "user",
                    "content": payload.get("prompt")
                }
            ]
    })
    return { "result": result["messages"][-1].text}
  
if __name__ == "__main__":
    app.run()
# input = {
#     "messages": [
#         {
#             "role": "user",
#             "content": "What is yesterday's picture of the day? and tell me like if there any news related to it?",
#         }
#     ]
# }
# stream = agent.stream_events(input, version="v3")
# for message in stream.messages:
#     for delta in message.text:
#         print(delta, end="", flush=True)

