
    
from typing import Any
from langchain.agents.middleware import AgentMiddleware, AgentState, hook_config
from langchain_core.messages import AIMessage
from langgraph.runtime import Runtime


class HCGuardrails(AgentMiddleware):

    """Ensure all responses include appropriate medical disclaimers.
       Block non-medical or harmful request in a healthcare products    
    """

    disclaimer = "\n\n *This is general health information, not medical advice. Please consult doctors*"

    @hook_config(can_jump_to=['end'])
    def after_agent(self, state: AgentState, runtime: Runtime)-> dict[str, Any] | None:
        if not state["messages"]:
            return None       

        last_message = state["messages"][-1]
        if not isinstance(last_message, AIMessage):
            return None

        if "medical advice" not in last_message.content.lower():
            last_message.content += self.disclaimer

        return None


    BLOCKED_TOPICS = ["drug synthesis", "self-harm", "suicide method", "weapon", "hack"]

    @hook_config(can_jump_to=['end'])
    def before_agent(self, state: AgentState, runtime: Runtime)-> dict[str, Any] | None:

        if not state["messages"]:
            return None    

        first_message= state["messages"][0]
        if first_message.type != "human":
            return None

        content = first_message.content.lower()

        for keyword in self.BLOCKED_TOPICS:
            if keyword in content:
                return{
                    "messages": [{
                        "role": "assistant",
                        "content": (
                            "I am a healthcare assistant and can only help with"
                            "medical questions, appointments, and health information."
                            "Please call 112 or local emergency number."
                        )
                    }]
                }    


        return None    