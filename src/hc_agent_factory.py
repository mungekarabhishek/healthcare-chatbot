from langchain_core.messages import SystemMessage
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph.state import END, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition
from src.hc_guardrails import AgentState, blocked_topics_node, medical_disclaimer
from src.hc_tools import get_medication_info, schedule_appointment, search_symptoms
from langchain_openai import ChatOpenAI


class HCAgentFactory:
    def __init__(self, model: str = "gpt-4o-mini"):
        """Initialize the agent factory with tool and guardrail dependencies."""
        self.tools_list = [get_medication_info, schedule_appointment, search_symptoms]
        self.model = ChatOpenAI(model=model).bind_tools(self.tools_list)

    def create_prod_agent(self):

        builder = StateGraph(AgentState)

        builder.add_node("safety_filter", blocked_topics_node)
        builder.add_node("agent", self.call_node)
        builder.add_node("tools", ToolNode(self.tools_list))
        builder.add_node("disclaimer", medical_disclaimer)

        builder.set_entry_point("safety_filter")
        builder.add_edge("safety_filter", "agent")
        builder.add_conditional_edges(
            "agent", tools_condition, {"tools": "tools", "__end__": "disclaimer"}
        )
        builder.add_edge("tools", "agent")
        builder.add_edge("disclaimer", END)

        return builder.compile(checkpointer=InMemorySaver(), interrupt_before=["agent"])

    def call_node(self, state: AgentState):

        system_prompt = SystemMessage(
            content=(
                "You are a strict healthcare assistant. You do not guess information. "
                "If a user asks about symptoms, you MUST use the `search_symptoms` tool. "
                "If they ask about medication, you MUST use `get_medication_info`. "
                "If they want to book something, use `schedule_appointment`. "
                "Always look up data using your tools before answering medical questions."
                "Always keep response maximum 200 words only"
            )
        )
        messages = [system_prompt] + list(state["messages"])
        response = self.model.invoke(messages)
        return {"messages": [response]}
