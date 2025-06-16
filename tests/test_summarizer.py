import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from summarizer import summarize_texts


def test_summarize_basic():
    texts = ["This is a long message about Python.", "Another message with info."]
    summary = summarize_texts(texts)
    assert isinstance(summary, str)
    assert summary


def test_openai_parameters(monkeypatch):
    class Resp:
        choices = [type("obj", (), {"message": {"content": "ok"}})()]

    called = {}

    def fake_create(**kwargs):
        called.update(kwargs)
        return Resp()

    if hasattr(summarize_texts, "__module__"):
        import summarizer

    monkeypatch.setenv("OPENAI_API_KEY", "x")
    monkeypatch.setattr(summarizer.openai.ChatCompletion, "create", staticmethod(fake_create))
    monkeypatch.setattr(summarizer, "DEFAULT_MODEL", "test-model")
    monkeypatch.setattr(summarizer, "DEFAULT_TEMPERATURE", 0.5)
    monkeypatch.setattr(summarizer, "MAX_OUTPUT_TOKENS", 200)
    monkeypatch.setattr(summarizer, "MAX_INPUT_TOKENS", 1)

    summary = summarizer.summarize_texts(["hello"] * 20)
    assert summary == "ok"
    assert called["model"] == "test-model"
    assert called["temperature"] == 0.5
    assert called["max_tokens"] == 200
    assert len(called["messages"][1]["content"]) <= 4
