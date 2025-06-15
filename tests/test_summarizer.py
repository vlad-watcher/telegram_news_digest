import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from summarizer import summarize_texts


def test_summarize_basic():
    texts = ["This is a long message about Python.", "Another message with info."]
    summary = summarize_texts(texts)
    assert isinstance(summary, str)
    assert summary
