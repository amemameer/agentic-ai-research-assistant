"""
Tool functions used by the agentic workflow.

These tools are intentionally written in raw Python.
No agent frameworks are used.
"""

from __future__ import annotations

import os
import re
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import Dict, List

from config import MAX_PAPERS, OUTPUT_FOLDER, OUTPUT_FILE


def clean_text(text: str) -> str:
    """Remove extra spaces and line breaks."""
    return re.sub(r"\s+", " ", text or "").strip()


def search_arxiv(topic: str, max_results: int = MAX_PAPERS) -> List[Dict[str, str]]:
    """
    Search arXiv for papers related to the topic.

    This function is used as a Tool Use pattern.
    The agent calls this tool when it needs outside research data.
    """

    encoded_topic = urllib.parse.quote(topic)

    url = (
        "http://export.arxiv.org/api/query?"
        f"search_query=all:{encoded_topic}"
        f"&start=0&max_results={max_results}"
        "&sortBy=relevance&sortOrder=descending"
    )

    try:
        with urllib.request.urlopen(url, timeout=20) as response:
            xml_data = response.read().decode("utf-8")
    except Exception as error:
        raise RuntimeError(f"arXiv search failed. Please check your internet connection. Details: {error}")

    root = ET.fromstring(xml_data)
    namespace = {"atom": "http://www.w3.org/2005/Atom"}

    papers: List[Dict[str, str]] = []

    for entry in root.findall("atom:entry", namespace):
        title = clean_text(entry.findtext("atom:title", default="", namespaces=namespace))
        summary = clean_text(entry.findtext("atom:summary", default="", namespaces=namespace))
        published = clean_text(entry.findtext("atom:published", default="", namespaces=namespace))
        link = clean_text(entry.findtext("atom:id", default="", namespaces=namespace))

        authors = []
        for author in entry.findall("atom:author", namespace):
            author_name = author.findtext("atom:name", default="", namespaces=namespace)
            if author_name:
                authors.append(clean_text(author_name))

        papers.append(
            {
                "title": title,
                "authors": ", ".join(authors),
                "published": published[:10],
                "summary": summary,
                "link": link,
            }
        )

    return papers


def extract_keywords(text: str, limit: int = 10) -> List[str]:
    """
    Extract simple keywords using frequency counting.

    This is another tool used by the Researcher Agent.
    """

    stopwords = {
        "the", "and", "for", "with", "that", "this", "from", "are", "was", "were",
        "has", "have", "into", "using", "used", "such", "their", "these", "those",
        "can", "may", "will", "our", "its", "about", "also", "than", "then",
        "model", "models", "data", "paper", "study", "based", "learning",
        "approach", "method", "methods", "results", "show", "shown"
    }

    words = re.findall(r"[a-zA-Z]{4,}", text.lower())
    counts: Dict[str, int] = {}

    for word in words:
        if word not in stopwords:
            counts[word] = counts.get(word, 0) + 1

    ranked_words = sorted(counts.items(), key=lambda item: item[1], reverse=True)
    return [word for word, _ in ranked_words[:limit]]


def save_report(content: str) -> str:
    """Save the final generated report."""
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    file_path = os.path.join(OUTPUT_FOLDER, OUTPUT_FILE)

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)

    return file_path


def get_current_time() -> str:
    """Return current date and time."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")