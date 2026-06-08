from dotenv import load_dotenv
from src.hc_agent_factory import HCAgentFactory
from src.hc_bot import HCBots

load_dotenv()


def main():

    factory = HCAgentFactory()

    bot = HCBots(factory=factory)
    bot.launch_app()


if __name__ == "__main__":
    main()
