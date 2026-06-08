from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langgraph.graph.message import add_messages


class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]


def medical_disclaimer(state: AgentState):
    """Ensure all responses include appropriate medical disclaimers.
    Block non-medical or harmful request in a healthcare products
    """

    disclaimer = "\n\n *This is general health information, not medical advice. Please consult doctors*"
    messages = state.get("messages", [])
    if not messages:
        return state

    last_message = messages[-1]
    if not isinstance(last_message, AIMessage):
        return None

    if "medical advice" not in last_message.content.lower():
        last_message.content += disclaimer

    return {"messages": messages}


def blocked_topics_node(state: AgentState):
    BLOCKED_TOPICS = ["drug synthesis", "self-harm", "suicide method", "weapon", "hack"]

    messages = state.get("messages", [])
    if not messages:
        return state
    last_message = messages[-1]
    content = last_message.content.lower()

    if isinstance(last_message, HumanMessage):
        for keyword in BLOCKED_TOPICS:
            if keyword in content:
                return {
                    "messages": [
                        AIMessage(
                            content="I am a healthcare assistant and can only help with medical questions. Please call 112 or local emergency number."
                        )
                    ]
                }

    return state
