"""Utilities for summarizing lists of messages."""

import os
import logging
from typing import List

try:
    import openai
except ImportError:  # fallback if openai not installed
    openai = None

logger = logging.getLogger(__name__)


def summarize_texts(texts: List[str]) -> str:
    """Return a single summary from multiple message strings.

    Args:
        texts: Sequence of message texts to summarize.

    Returns:
        A concise string containing the summary.
    """
    if not texts:
        return ""
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key and openai:
        openai.api_key = api_key
        try:
            joined = "\n".join(texts)
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": f"Summarize the following messages:\n{joined}"}],
                max_tokens=150,
            )
            return response.choices[0].message["content"].strip()
        except Exception as exc:  # network or API error
            logger.error("OpenAI summarization failed: %s", exc)
    # fallback simple summary: return first 500 characters
    joined = "\n".join(texts)
    return (joined[:497] + "...") if len(joined) > 500 else joined
