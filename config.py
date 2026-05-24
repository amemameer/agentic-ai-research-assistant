##Configuration file for the Agentic AI Research Assistant.


import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini").strip()

MAX_PAPERS = 5
OUTPUT_FOLDER = "outputs"
OUTPUT_FILE = f"final_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"