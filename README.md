# Healthcare Chatbot 🏥

An AI-powered healthcare assistant chatbot built with LangChain, LangGraph, and Gradio. This chatbot provides medical information, schedules appointments, and searches symptoms while maintaining strict safety guardrails and medical disclaimers.

## Features ✨

- **🔍 Symptom Search**: Search for information about medical symptoms
- **💊 Medication Information**: Get details about medications
- **📅 Appointment Scheduling**: Book appointments with doctors
- **🛡️ Safety Guardrails**: Blocks harmful topics (drug synthesis, self-harm, weapons, etc.)
- **⚠️ Medical Disclaimers**: Automatically adds disclaimers to all responses
- **💬 Interactive UI**: User-friendly Gradio interface
- **🧠 LangGraph Workflow**: Structured agent workflow with state management

## Architecture 🏗️

The chatbot uses a multi-node LangGraph workflow:

```
User Input → Safety Filter → Agent → Tools/Disclaimer → Response
```

### Components

1. **Safety Filter**: Blocks harmful or inappropriate topics
2. **Agent Node**: LLM-powered decision making with tool binding
3. **Tool Node**: Executes healthcare-related tools
4. **Disclaimer Node**: Adds medical disclaimers to responses

## Prerequisites 📋

- Python 3.12 or higher
- OpenAI API key
- UV package manager (recommended) or pip

## Installation 🚀

### 1. Clone the Repository

```bash
git clone <repository-url>
cd healthcare-chatbot
```

### 2. Set Up Environment

**Using UV (Recommended):**
```bash
uv sync
```

### 3. Configure API Key

Copy the example environment file:
```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:
```
OPENAI_API_KEY=your-actual-api-key-here
```

Get your API key from: https://platform.openai.com/api-keys

## Usage 🎯

### Run the Chatbot

```bash
python main.py
```

The Gradio interface will launch in your browser (typically at `http://127.0.0.1:7860`).

### Example Interactions

**Symptom Search:**
```
User: I have a headache and fever
Bot: Symptoms: headache and fever. Please consult the doctor for more information.
     *This is general health information, not medical advice. Please consult doctors*
```

**Medication Info:**
```
User: Tell me about aspirin
Bot: Here are your medicines: aspirin. Please follow doctor's prescription
     *This is general health information, not medical advice. Please consult doctors*
```

**Appointment Booking:**
```
User: Book an appointment with Dr. Smith on Monday
Bot: Appointment booked for [patient_name] with Dr.Smith on Monday
     *This is general health information, not medical advice. Please consult doctors*
```

## Project Structure 📁

```
healthcare-chatbot/
├── src/
│   ├── __init__.py
│   ├── hc_agent_factory.py    # Agent creation and workflow
│   ├── hc_bot.py               # Gradio UI and chat logic
│   ├── hc_guardrails.py        # Safety filters and disclaimers
│   └── hc_tools.py             # Healthcare tools (LangChain)
├── main.py                     # Application entry point
├── app.ipynb                   # Jupyter notebook for testing
├── pyproject.toml              # Project dependencies
├── .env.example                # Environment variables template
├── .gitignore                  # Git ignore rules
└── README.md                   # This file
```

## Key Components 🔑

### Tools (`src/hc_tools.py`)

Three main tools powered by LangChain:
- `schedule_appointment`: Books medical appointments
- `search_symptoms`: Searches symptom information
- `get_medication_info`: Retrieves medication details

### Agent Factory (`src/hc_agent_factory.py`)

Creates the LangGraph agent with:
- Tool binding to GPT-4o-mini
- State management with InMemorySaver
- Conditional routing based on tool calls
- System prompt for strict healthcare assistance

### Guardrails (`src/hc_guardrails.py`)

Safety mechanisms:
- **Blocked Topics**: Filters harmful content (drug synthesis, self-harm, weapons, etc.)
- **Medical Disclaimers**: Adds disclaimers to all AI responses
- **Emergency Routing**: Redirects dangerous queries to emergency services

### Bot Interface (`src/hc_bot.py`)

Gradio-based chat interface with:
- Conversation history management
- Thread-based state tracking
- Real-time response streaming

## Configuration ⚙️

### Model Selection

Change the LLM model in `main.py`:
```python
factory = HCAgentFactory(model="gpt-4o-mini")  # or "gpt-4", "gpt-3.5-turbo"
```

### Blocked Topics

Modify blocked topics in `src/hc_guardrails.py`:
```python
BLOCKED_TOPICS = ["drug synthesis", "self-harm", "suicide method", "weapon", "hack"]
```

## Dependencies 📦

- `langchain>=1.3.4` - LLM framework
- `langchain-openai>=1.2.2` - OpenAI integration
- `langgraph>=0.2.0` - Graph-based agent workflows
- `gradio>=6.16.0` - Web UI framework
- `python-dotenv>=0.9.9` - Environment variable management

## Safety & Disclaimers ⚠️

This chatbot:
- ✅ Provides general health information only
- ✅ Includes medical disclaimers on all responses
- ✅ Blocks harmful or dangerous topics
- ✅ Redirects emergencies to professional services
- ❌ Does NOT provide medical diagnosis
- ❌ Does NOT replace professional medical advice
- ❌ Should NOT be used for emergencies

**Always consult qualified healthcare professionals for medical advice.**

## Development 🛠️

### Running Tests

```bash
# Using pytest (if tests are added)
pytest tests/
```

### Jupyter Notebook

Explore the chatbot interactively:
```bash
jupyter notebook app.ipynb
```

## Troubleshooting 🔧

### Common Issues

**API Key Error:**
```
Error: OpenAI API key not found
Solution: Ensure .env file exists with valid OPENAI_API_KEY
```

**Import Errors:**
```
Error: Module not found
Solution: Run `uv sync`
```

**Port Already in Use:**
```
Error: Address already in use
Solution: Change port in bot.launch() or kill existing process
```

## Contributing 🤝

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request


## Acknowledgments 🙏

- Built with [LangChain](https://langchain.com/)
- Powered by [OpenAI](https://openai.com/)
- UI by [Gradio](https://gradio.app/)
- Workflow by [LangGraph](https://langchain-ai.github.io/langgraph/)

---

**⚠️ IMPORTANT MEDICAL DISCLAIMER ⚠️**

This chatbot is for informational purposes only and does not constitute medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition. Never disregard professional medical advice or delay in seeking it because of something you have read from this chatbot. If you think you may have a medical emergency, call your doctor or emergency services immediately.