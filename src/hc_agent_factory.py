from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware, PIIMiddleware
from langgraph.checkpoint.memory import InMemorySaver
from src.hc_tools import HCTools
from src.hc_guardrails import HCGuardrails


class HCAgentFactory:
    
    def __init__(self, hc_tools: HCTools, hc_guardrails: HCGuardrails, model: str="gpt-4o-mini"):
        """Initialize the agent factory with tool and guardrail dependencies."""
        self.model = model
        self.tools = hc_tools
        self.guardrails = hc_guardrails
    
    def create_prod_agent(self):
        
        prod_agent = create_agent(
            tools=[self.tools.schedule_appointment, self.tools.search_symptoms, self.tools.get_medication_info],
            model = self.model,
            middleware = [
                self.guardrails,
                PIIMiddleware("email",strategy="redact", apply_to_input=True),
                HumanInTheLoopMiddleware(
                    interrupt_on={
                        "schedule_appointment": True,
                        "search_symptoms": False,
                        "get_medication_info": False

                    }
                )
            ],
            checkpointer = InMemorySaver(),
            system_prompt = (
                "You are a helpful healthcare assistant. "
                "You can search for symptoms, medication information, and help book appointments. "
                "Always be empathetic and remind users to consult a doctor for diagnosis. "
                "STRICT CONSTRAINT: Keep all responses under 200 words. "
                "To do this, use bullet points for lists and provide direct, punchy answers. "
                "Avoid unnecessary introductions, pleasantries, or filler sentences. "
                "If a topic is too complex for 200 words, provide only the most critical information."
            )
        )
        return prod_agent        