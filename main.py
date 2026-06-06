from src.hc_agent_factory import HCAgentFactory
from src.hc_bot import HCBots
from src.hc_guardrails import HCGuardrails
from src.hc_tools import HCTools


def main():
  
  tools = HCTools()
  guardrails = HCGuardrails()
  factory = HCAgentFactory(hc_tools=tools, hc_guardrails=guardrails)
  
  bot = HCBots(factory=factory)
  bot.launch_app()


if __name__ == "__main__":
    main()
