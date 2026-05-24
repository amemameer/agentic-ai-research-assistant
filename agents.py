"""
Agent definitions for the Agentic AI Research Assistant.

This project uses a simple multi-agent architecture:

1. PlannerAgent
2. ResearcherAgent
3. WriterAgent
4. ReviewerAgent
5. CoordinatorAgent

No agent framework is used.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional

from config import OPENAI_API_KEY, OPENAI_MODEL
from tools import extract_keywords, get_current_time, save_report, search_arxiv


@dataclass
class AgentResponse:
    """Standard response format used between agents."""
    agent_name: str
    content: str


class LLMClient:
    """
    Optional OpenAI client.

    The app still works without an API key.
    If no API key is available, the Writer Agent uses local fallback writing.
    """

    def __init__(self) -> None:
        self.available = bool(OPENAI_API_KEY)
        self.client = None

        if self.available:
            try:
                from openai import OpenAI
                self.client = OpenAI(api_key=OPENAI_API_KEY)
            except Exception:
                self.available = False
                self.client = None

    def generate(self, prompt: str) -> Optional[str]:
        """Generate content using OpenAI if available."""
        if not self.available or self.client is None:
            return None

        try:
            response = self.client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a careful academic research assistant. "
                            "Write clearly, avoid unsupported claims, and organize the report professionally."
                        ),
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.3,
            )

            return response.choices[0].message.content

        except Exception:
            return None


class PlannerAgent:
    """
    Planning Agent.

    This agent breaks the user's research request into clear steps.
    This demonstrates the Planning design pattern.
    """

    name = "Planner Agent"

    def create_plan(self, topic: str) -> AgentResponse:
        plan = f"""
Research Topic: {topic}

Step-by-step plan:
1. Understand the topic and identify the research goal.
2. Search for relevant research papers using arXiv.
3. Extract paper titles, authors, dates, summaries, and links.
4. Extract important keywords from the collected summaries.
5. Generate a structured mini research report.
6. Review the report using reflection.
7. Save the final report in the output folder.
""".strip()

        return AgentResponse(agent_name=self.name, content=plan)


class ResearcherAgent:
    """
    Research Agent.

    This agent uses tools to collect research data.
    This demonstrates the Tool Use design pattern.
    """

    name = "Researcher Agent"

    def research(self, topic: str) -> Dict[str, object]:
        papers = search_arxiv(topic)

        combined_summaries = " ".join(paper["summary"] for paper in papers)
        keywords = extract_keywords(combined_summaries)

        return {
            "topic": topic,
            "papers": papers,
            "keywords": keywords,
        }


class WriterAgent:
    """
    Writer Agent.

    This agent writes the first version of the research report.
    """

    name = "Writer Agent"

    def __init__(self, llm_client: LLMClient) -> None:
        self.llm_client = llm_client

    def write_report(self, research_data: Dict[str, object]) -> AgentResponse:
        topic = str(research_data["topic"])
        papers = research_data["papers"]
        keywords = research_data["keywords"]

        prompt = self._build_prompt(topic, papers, keywords)
        llm_report = self.llm_client.generate(prompt)

        if llm_report:
            return AgentResponse(agent_name=self.name, content=llm_report)

        fallback_report = self._write_fallback_report(topic, papers, keywords)
        return AgentResponse(agent_name=self.name, content=fallback_report)

    def _build_prompt(
        self,
        topic: str,
        papers: List[Dict[str, str]],
        keywords: List[str],
    ) -> str:
        paper_details = "\n\n".join(
            f"Title: {paper['title']}\n"
            f"Authors: {paper['authors']}\n"
            f"Published: {paper['published']}\n"
            f"Summary: {paper['summary']}\n"
            f"Link: {paper['link']}"
            for paper in papers
        )

        return f"""
Write a formal mini research report on this topic:

{topic}

Important keywords:
{", ".join(keywords)}

Use these papers as the evidence base:
{paper_details}

Report format:
1. Title
2. Introduction
3. Key Findings
4. Recent Research Papers
5. Practical Applications
6. Limitations
7. Conclusion

Keep the writing clear, professional, and source-supported.
""".strip()

    def _write_fallback_report(
        self,
        topic: str,
        papers: List[Dict[str, str]],
        keywords: List[str],
    ) -> str:
        lines = [
            "Agentic AI Research Report",
            f"Topic: {topic}",
            f"Generated on: {get_current_time()}",
            "",
            "1. Introduction",
            (
                f"This report provides a short research overview of the topic: {topic}. "
                "The application uses an agentic workflow that includes planning, tool use, "
                "multi-agent collaboration, and reflection."
            ),
            "",
            "2. Key Findings",
            "The most important keywords found in the retrieved research summaries are:",
            ", ".join(keywords) if keywords else "No keywords were extracted.",
            "",
            "3. Recent Research Papers",
        ]

        if papers:
            for index, paper in enumerate(papers, start=1):
                lines.extend(
                    [
                        f"{index}. {paper['title']}",
                        f"   Authors: {paper['authors']}",
                        f"   Published: {paper['published']}",
                        f"   Link: {paper['link']}",
                        f"   Summary: {paper['summary']}",
                        "",
                    ]
                )
        else:
            lines.append("No papers were found for this topic.")

        lines.extend(
            [
                "4. Practical Applications",
                (
                    "This type of agentic application can support research discovery, "
                    "academic writing, literature review, and decision support."
                ),
                "",
                "5. Limitations",
                (
                    "The report depends on arXiv search results only. It may miss important "
                    "papers from IEEE, ACM, Springer, ScienceDirect, or other databases."
                ),
                "",
                "6. Conclusion",
                (
                    "The system successfully demonstrates an agentic workflow by planning the task, "
                    "using tools, dividing work between agents, reflecting on the result, and saving "
                    "the final output."
                ),
            ]
        )

        return "\n".join(lines)


class ReviewerAgent:
    """
    Reviewer Agent.

    This agent reviews the generated report.
    This demonstrates the Reflection design pattern.
    """

    name = "Reviewer Agent"

    def review(self, report: str) -> AgentResponse:
        feedback = []

        word_count = len(report.split())

        if word_count < 250:
            feedback.append("The report is short. Add more explanation if this is for formal submission.")
        else:
            feedback.append("The report has an acceptable length for a mini research report.")

        required_sections = [
            "Introduction",
            "Key Findings",
            "Recent Research Papers",
            "Practical Applications",
            "Limitations",
            "Conclusion",
        ]

        missing_sections = [
            section for section in required_sections
            if section.lower() not in report.lower()
        ]

        if missing_sections:
            feedback.append("Missing sections: " + ", ".join(missing_sections))
        else:
            feedback.append("All required sections are present.")

        if "http" in report:
            feedback.append("The report includes research links/sources.")
        else:
            feedback.append("The report should include research links or citations.")

        if "limitation" in report.lower() or "limitations" in report.lower():
            feedback.append("Limitations are discussed.")
        else:
            feedback.append("Limitations should be added.")

        reflection_report = "Reflection / Error Analysis:\n" + "\n".join(
            f"- {item}" for item in feedback
        )

        return AgentResponse(agent_name=self.name, content=reflection_report)


class CoordinatorAgent:
    """
    Coordinator Agent.

    This agent manages the complete workflow between all agents.
    """

    name = "Coordinator Agent"

    def __init__(self):
        self.llm_client = LLMClient()

        self.planner = PlannerAgent()
        self.researcher = ResearcherAgent()
        self.writer = WriterAgent(self.llm_client)
        self.reviewer = ReviewerAgent()

    def run(self, topic: str):

        # Planning step
        plan_response = self.planner.create_plan(topic)

        # Research step
        research_data = self.researcher.research(topic)

        # Writing step
        draft_response = self.writer.write_report(research_data)

        # Reflection step
        review_response = self.reviewer.review(draft_response.content)

        final_output = f"""
==================================================
AGENTIC AI RESEARCH ASSISTANT
==================================================

{plan_response.content}

==================================================
FINAL RESEARCH REPORT
==================================================

{draft_response.content}

==================================================
REFLECTION / ERROR ANALYSIS
==================================================

{review_response.content}

==================================================
AGENTIC DESIGN PATTERNS USED
==================================================

1. Reflection
- Reviewer Agent checks report quality.

2. Tool Use
- Researcher Agent uses arXiv search and keyword extraction tools.

3. Planning
- Planner Agent creates a workflow before execution.

4. Multi-Agent Systems
- Multiple specialized agents work together.

==================================================
LATENCY AND COST OPTIMIZATION
==================================================

- Limited paper retrieval reduces latency.
- OpenAI API is optional.
- Lightweight keyword extraction is used.
- Modular design improves maintainability.
"""

        saved_path = save_report(final_output)

        return f"{final_output}\n\nSaved report path: {saved_path}"