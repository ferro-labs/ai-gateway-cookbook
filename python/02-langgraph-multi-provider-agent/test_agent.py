from __future__ import annotations

import unittest
from dataclasses import dataclass
from typing import Any

import agent


@dataclass
class FakeResponse:
    content: str
    provider: str
    trace_id: str

    @property
    def response_metadata(self) -> dict[str, str]:
        return {"provider": self.provider, "trace_id": self.trace_id}


class FakeChat:
    def __init__(self, content: str, provider: str, trace_id: str) -> None:
        self._response = FakeResponse(content=content, provider=provider, trace_id=trace_id)
        self.calls: list[list[Any]] = []

    def invoke(self, messages: list[Any]) -> FakeResponse:
        self.calls.append(messages)
        return self._response


class LangGraphRecipeTest(unittest.TestCase):
    def test_graph_uses_three_models_and_preserves_trace_ids(self) -> None:
        planner = FakeChat("1. Write a small CLI", "openai", "trace-plan")
        coder = FakeChat('print("hello")', "anthropic", "trace-code")
        summarizer = FakeChat("A tiny CLI prints hello.", "google", "trace-summary")

        old_planner, old_coder, old_summarizer = agent.PLANNER, agent.CODER, agent.SUMMARIZER
        try:
            agent.PLANNER = planner
            agent.CODER = coder
            agent.SUMMARIZER = summarizer

            result = agent.build_graph().invoke(
                {
                    "request": "Build a hello CLI.",
                    "plan": "",
                    "code": "",
                    "summary": "",
                    "trace_ids": [],
                }
            )
        finally:
            agent.PLANNER = old_planner
            agent.CODER = old_coder
            agent.SUMMARIZER = old_summarizer

        self.assertEqual(result["plan"], "1. Write a small CLI")
        self.assertEqual(result["code"], 'print("hello")')
        self.assertEqual(result["summary"], "A tiny CLI prints hello.")
        self.assertEqual(result["trace_ids"], ["trace-plan", "trace-code", "trace-summary"])
        self.assertEqual(len(planner.calls), 1)
        self.assertEqual(len(coder.calls), 1)
        self.assertEqual(len(summarizer.calls), 1)


if __name__ == "__main__":
    unittest.main()
