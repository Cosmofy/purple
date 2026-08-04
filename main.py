from uuid import uuid4

from langchain.agents import create_agent
from langchain_core.messages import AIMessageChunk
from tools import tool_get_picture
from a2a.helpers.proto_helpers import new_task_from_user_message, new_text_part
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.server.tasks import TaskUpdater
from bedrock_agentcore.runtime import serve_a2a

agent = create_agent(
    model = "openai:gpt-5.4-nano",
    tools = [
        tool_get_picture, 
        {"type": "web_search"},
    ]
)  

class CosmofyAgentExecutor(AgentExecutor):
    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        if context.message is None:
            raise ValueError("A2A request must include a message.")

        task = context.current_task or new_task_from_user_message(context.message)
        if context.current_task is None:
            await event_queue.enqueue_event(task)

        updater = TaskUpdater(event_queue, task.id, task.context_id)
        agent_input = {
            "messages": [
                {
                    "role": "user",
                    "content": context.get_user_input(),
                }
            ]
        }
        artifact_id = str(uuid4())
        pending_text = None
        artifact_started = False

        async for message_chunk, metadata in agent.astream(
            agent_input,
            stream_mode="messages",
        ):
            if not isinstance(message_chunk, AIMessageChunk):
                continue
            if metadata.get("langgraph_node") != "model":
                continue

            text = message_chunk.text
            if not text:
                continue

            if pending_text is not None:
                await updater.add_artifact(
                    [new_text_part(pending_text)],
                    artifact_id=artifact_id,
                    append=artifact_started,
                    last_chunk=False,
                )
                artifact_started = True
            pending_text = text

        if pending_text is not None:
            await updater.add_artifact(
                [new_text_part(pending_text)],
                artifact_id=artifact_id,
                append=artifact_started,
                last_chunk=True,
            )
        await updater.complete()

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        if context.current_task is not None:
            updater = TaskUpdater(
                event_queue,
                context.current_task.id,
                context.current_task.context_id,
            )
            await updater.cancel()
  
if __name__ == "__main__":
    serve_a2a(CosmofyAgentExecutor())
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
