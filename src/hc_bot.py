import uuid
import gradio as gr

from src.hc_agent_factory import HCAgentFactory
class HCBots:
    def __init__(self, factory: HCAgentFactory):
        self.thread_id = str(uuid.uuid4())
        self.config = {"configurable": {"thread_id": self.thread_id}}
        self.agent = factory.create_prod_agent()
    
    def chat_with_agent(self, user_input: str)-> str:
        response = self.agent.invoke(
            {
                "messages": [
                    {"role": "user","content": user_input}
                ]
            },
            config=self.config
        )
        return response["messages"][-1].content
    
    def respond(self, message, history):
        reply = self.chat_with_agent(message)
        history.append({"role":"user", "content": message})
        history.append({"role":"assistant", "content": reply})
        return "", history    
    
    def launch_app(self):    
        with gr.Blocks() as app:
            gr.Markdown("## Healthcare Assistant ##")
            chatbot = gr.Chatbot()
            text = gr.Textbox(label="Ask Something...")

            text.submit(self.respond, [text, chatbot], [text, chatbot])

        app.launch()