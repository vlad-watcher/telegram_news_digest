"""Utilities for summarizing lists of messages."""

import os
import logging
from typing import List

try:
    import openai
except ImportError:  # fallback if openai not installed
    openai = None

logger = logging.getLogger(__name__)

# Configuration defaults controllable via environment variables
DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")
DEFAULT_TEMPERATURE = float(os.getenv("SUMMARY_TEMPERATURE", "0.2"))
MAX_OUTPUT_TOKENS = int(os.getenv("SUMMARY_MAX_OUTPUT_TOKENS", "1000"))
MAX_INPUT_TOKENS = int(os.getenv("SUMMARY_MAX_INPUT_TOKENS", "5000"))

# The default system prompt used for the summarization request
SYSTEM_PROMPT = (
    "You are an expert news summarizer. Preserve all important facts, names, "
    "and logical flow. Summarize concisely into 600–800 tokens with no "
    "hallucination or invented content."
)


def summarize_texts(texts: List[str]) -> str:
    """Return a single summary from multiple message strings.

    Environment variables can adjust the behavior:
        - ``OPENAI_MODEL``: model name (default ``gpt-4o``)
        - ``SUMMARY_TEMPERATURE``: sampling temperature (default ``0.2``)
        - ``SUMMARY_MAX_OUTPUT_TOKENS``: max summary tokens (default ``1000``)
        - ``SUMMARY_MAX_INPUT_TOKENS``: max input tokens considered (default ``5000``)

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
            char_limit = MAX_INPUT_TOKENS * 4  # rough token-to-char conversion
            if len(joined) > char_limit:
                joined = joined[:char_limit]
            response = openai.ChatCompletion.create(
                model=DEFAULT_MODEL,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": joined},
                ],
                temperature=DEFAULT_TEMPERATURE,
                max_tokens=MAX_OUTPUT_TOKENS,
            )
            return response.choices[0].message["content"].strip()
        except Exception as exc:  # network or API error
            logger.error("OpenAI summarization failed: %s", exc)

    # fallback simple summary: return first 500 characters
    joined = "\n".join(texts)
    return (joined[:497] + "...") if len(joined) > 500 else joined
