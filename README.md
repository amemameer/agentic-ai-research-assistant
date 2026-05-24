Agentic AI Research Assistant

Overview

Agentic AI Research Assistant is a production-ready raw Python application designed to demonstrate the core agentic AI design patterns taught in the DeepLearning.AI Agentic AI course by Professor Andrew Ng.

The application performs automated research workflows by combining planning, tool usage, reflection, and multi-agent collaboration into one intelligent system.

The user enters a research topic, and the system automatically:

* creates a research plan,
* searches for relevant research papers,
* extracts important keywords,
* generates a mini research report,
* performs reflection/error analysis,
* and saves the final report.

⸻

Agentic AI Design Patterns Implemented

1. Reflection

The Reviewer Agent checks the generated report for:

* completeness,
* report quality,
* missing sections,
* source presence,
* and possible weaknesses.

This demonstrates self-review and reflection behavior.

⸻

2. Tool Use

The application uses external tools including:

* arXiv research paper search,
* keyword extraction,
* file saving utilities.

The Researcher Agent dynamically uses these tools during execution.

⸻

3. Planning

The Planner Agent creates a step-by-step workflow before the task begins.

Instead of immediately generating output, the system first:

1. understands the task,
2. plans the workflow,
3. then executes each step.

⸻

4. Multi-Agent Systems

The project uses multiple specialized agents:

* Planner Agent
* Researcher Agent
* Writer Agent
* Reviewer Agent
* Coordinator Agent

Each agent performs a dedicated responsibility while collaborating together as a complete agentic workflow.

⸻

Technologies Used

* Python
* OpenAI API (optional)
* arXiv API
* dotenv
* standard Python libraries

⸻

Features

* Raw Python implementation
* Multi-agent workflow
* Reflection and error analysis
* Research paper retrieval
* Keyword extraction
* Automatic report generation
* Automatic report saving
* Modular architecture
* Optional OpenAI integration
* Cost-aware fallback mode

⸻

Project Structure

agentic_ai_research_assistant/
│
├── main.py
├── agents.py
├── tools.py
├── config.py
├── requirements.txt
├── .env.example
└── outputs/

⸻

Installation

Install dependencies:

pip install -r requirements.txt

⸻

Run the Application

python main.py

⸻

Example Research Topics

* Agentic AI in healthcare
* Generative AI in education
* AI ethics
* Multi-agent systems
* Prompt engineering
* Reinforcement learning

⸻

Output

Generated reports are automatically saved inside the outputs folder.

Example:

outputs/final_report_20260524_232132.txt

⸻

Assignment Requirement Mapping

Course Requirement	Project Implementation
Reflection	Reviewer Agent
Tool Use	arXiv search + keyword extraction
Planning	Planner Agent workflow
Multi-Agent Systems	Multiple collaborating agents
Raw Python	No LangChain/CrewAI/AutoGen
Production-ready direction	Modular architecture + error handling

⸻

Notes

This project was intentionally developed using raw Python without agentic AI frameworks in order to better demonstrate the underlying workflow and system architecture concepts taught in the course.
