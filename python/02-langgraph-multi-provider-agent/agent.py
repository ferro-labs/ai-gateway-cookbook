"""LangGraph multi-provider agent — one graph, three providers, one Ferro gateway.

Pipeline:

    user request
        │
        ▼
    planner   →  gpt-4o            (OpenAI — strong reasoning)
        │
        ▼
    coder     →  claude-3-5-sonnet (Anthropic — code quality)
        │
        ▼
    summarizer → gemini-1.5-flash  (Google — cheap, fast)
        │
        ▼
      result

Every step prints its Ferro ``trace_id`` (propagated as the ``x-trace-id``
response header — frozen contract since ``ai-gateway v1.1.0``). Those IDs are
the join key for any v1.2 observability bridge plugin (LangSmith, Langfuse,
Phoenix, …).
"""

from __future__ import annotations

import os
from typing import TypedDict

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_ferrolabsai import FerroChatModel
from langgraph.graph import END, StateGraph


# ---------------------------------------------------------------------------
# State
# ---------------------------------------------------------------------------


class AgentState(TypedDict):
    """The state passed between graph nodes."""

    request: str
    plan: str
    code: str
    summary: str
    trace_ids: list[str]


# ---------------------------------------------------------------------------
# Per-node chat models — one FerroChatModel per provider, all pointing at the
# same gateway. The model name is the *only* thing that differs.
# ---------------------------------------------------------------------------


def _make_chat(model: str) -> FerroChatModel:
    return FerroChatModel(
        model=model,
        base_url=os.environ.get("FERRO_BASE_URL", "http://localhost:8080"),
        api_key=os.environ.get("FERRO_API_KEY"),
        temperature=0.2,
    )


PLANNER = _make_chat("gpt-4o")
CODER = _make_chat("claude-3-5-sonnet-20241022")
SUMMARIZER = _make_chat("gemini-1.5-flash")


# ---------------------------------------------------------------------------
# Nodes
# ---------------------------------------------------------------------------


def _trace_id(response) -> str:
    """Pull the Ferro trace_id from a LangChain AIMessage's response_metadata."""
    return response.response_metadata.get("trace_id", "<missing>")


def _provider(response) -> str:
    return response.response_metadata.get("provider", "<unknown>")


def plan(state: AgentState) -> AgentState:
    response = PLANNER.invoke(
        [
            SystemMessage(content="You are a senior engineer. Produce a numbered, 3-5 step plan."),
            HumanMessage(content=state["request"]),
        ]
    )
    trace_id = _trace_id(response)
    print(f"  [{'planner':<10} · {_provider(response):<10} · trace_id={trace_id}]")
    return {
        **state,
        "plan": response.content,
        "trace_ids": [*state["trace_ids"], trace_id],
    }


def code(state: AgentState) -> AgentState:
    response = CODER.invoke(
        [
            SystemMessage(
                content="You are a senior Python engineer. Implement the plan as a single "
                "self-contained Python snippet. No prose, just code."
            ),
            HumanMessage(content=f"Plan:\n{state['plan']}"),
        ]
    )
    trace_id = _trace_id(response)
    print(f"  [{'coder':<10} · {_provider(response):<10} · trace_id={trace_id}]")
    return {
        **state,
        "code": response.content,
        "trace_ids": [*state["trace_ids"], trace_id],
    }


def summarize(state: AgentState) -> AgentState:
    response = SUMMARIZER.invoke(
        [
            SystemMessage(content="Summarize in ONE short sentence what the code does."),
            HumanMessage(content=state["code"]),
        ]
    )
    trace_id = _trace_id(response)
    print(f"  [{'summarizer':<10} · {_provider(response):<10} · trace_id={trace_id}]")
    return {
        **state,
        "summary": response.content,
        "trace_ids": [*state["trace_ids"], trace_id],
    }


# ---------------------------------------------------------------------------
# Graph
# ---------------------------------------------------------------------------


def build_graph():
    # Node names intentionally differ from state keys — LangGraph disallows
    # collisions between the two namespaces.
    graph = StateGraph(AgentState)
    graph.add_node("planner", plan)
    graph.add_node("coder", code)
    graph.add_node("summarizer", summarize)
    graph.set_entry_point("planner")
    graph.add_edge("planner", "coder")
    graph.add_edge("coder", "summarizer")
    graph.add_edge("summarizer", END)
    return graph.compile()


# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------


def main() -> int:
    if not os.environ.get("FERRO_API_KEY"):
        print(
            "ERROR: FERRO_API_KEY is not set. Run `cp .env.example .env` and fill it in.",
        )
        return 1

    request = os.environ.get(
        "AGENT_REQUEST",
        "Build a CLI that fetches the current UTC time and prints it as ISO-8601.",
    )

    print(f"Request: {request}\n")
    print("Routing through Ferro gateway:")
    app = build_graph()
    final = app.invoke({"request": request, "plan": "", "code": "", "summary": "", "trace_ids": []})

    print("\n--- Plan (gpt-4o) ---")
    print(final["plan"])
    print("\n--- Code (claude-3-5-sonnet) ---")
    print(final["code"])
    print("\n--- Summary (gemini-1.5-flash) ---")
    print(final["summary"])
    print("\n--- Ferro trace IDs (join key for any observability bridge) ---")
    for step, tid in zip(["plan", "code", "summary"], final["trace_ids"], strict=True):
        print(f"  {step:<10} {tid}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
