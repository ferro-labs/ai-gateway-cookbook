# 02 · LangGraph Multi-Provider Agent

A LangGraph agent where **each step routes to a different best-in-class provider** through one Ferro Labs AI Gateway endpoint — zero rewrites to the LangGraph code, one URL, one auth token.

```diagram
  user request
       │
       ▼
   ╭──────────╮      ╭──────────╮      ╭───────────────╮
   │ planner  │─────▶│  coder   │─────▶│  summarizer   │─────▶ result
   │  gpt-4o  │      │  claude  │      │ gemini-flash  │
   ╰──────────╯      ╰──────────╯      ╰───────────────╯
        OpenAI         Anthropic           Google
        ▲                                        ▲
        ╰────────── one FERRO_BASE_URL ──────────╯
```

## What it demonstrates

- **Multi-provider routing inside a single LangGraph state machine.** `FerroChatModel(model="gpt-4o")`, `FerroChatModel(model="claude-3-5-sonnet-20241022")`, and `FerroChatModel(model="gemini-1.5-flash")` all talk to the *same* gateway — only the model name changes.
- **`trace_id` surfacing.** Every step prints the Ferro `trace_id` it received (propagated via the `x-trace-id` response header, frozen contract since `ai-gateway v1.1.0`). These IDs are the join key for any v1.2 observability bridge plugin (LangSmith, Langfuse, Phoenix, Datadog, …).
- **Provider specialization.** The planner gets the strongest reasoning model; the coder gets the highest-quality code model; the summarizer gets the cheapest fast model. The agent author writes none of the routing, retry, or auth logic — it lives in the gateway.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- A running Ferro Labs AI Gateway at `FERRO_BASE_URL` (defaults to `http://localhost:8080`) with provider credentials configured for OpenAI, Anthropic, and Gemini.
- A Ferro API key (`FERRO_API_KEY`).

## How to run

```bash
cp .env.example .env
# Edit .env: set FERRO_API_KEY (and FERRO_BASE_URL if not localhost).
# Provider keys stay on the gateway side, not in this recipe .env file.

make run
```

Run the mocked smoke test without live provider calls:

```bash
make test
```

Expected output (abridged):

```
Request: Build a CLI that fetches the current UTC time and prints it as ISO-8601.

Routing through Ferro gateway:
  [planner    · openai     · trace_id=abc-123-...]
  [coder      · anthropic  · trace_id=def-456-...]
  [summarizer · google     · trace_id=ghi-789-...]

--- Plan (gpt-4o) ---
1. Parse argparse for optional --tz flag.
...

--- Code (claude-3-5-sonnet) ---
import argparse
from datetime import datetime, timezone
...

--- Summary (gemini-1.5-flash) ---
A CLI that prints the current UTC time in ISO-8601 format.

--- Ferro trace IDs (join key for any observability bridge) ---
  plan       abc-123-...
  code       def-456-...
  summary    ghi-789-...
```

## What to look for

- **Three different providers** in the bracketed step lines — `openai`, `anthropic`, `google` — produced by the gateway's routing.
- **Three different `trace_id` values**, one per provider call. If you have any observability bridge plugin installed on the gateway (e.g., `langsmith-bridge`), those three IDs will appear in your LangSmith / Langfuse / Phoenix UI as three separate runs — without the recipe importing any of those SDKs.
- **No provider SDKs imported.** This recipe imports only `langchain_ferrolabsai` and `langgraph`. The gateway handles every provider-specific concern.

## How it works

[`agent.py`](agent.py) builds a three-node `StateGraph` (planner → coder → summarizer). Each node instantiates a separate `FerroChatModel` pointed at the same gateway URL, differing only in the `model` argument. After each step the node pulls `response.response_metadata["trace_id"]` and appends it to the agent state for later printing.

`langchain-ferrolabsai` 0.1.0+ (released alongside this recipe) handles the metadata surfacing automatically — you do not need to read response headers manually.

## Docs

- Framework page: [docs.ferrolabs.ai/frameworks/langgraph](https://docs.ferrolabs.ai/frameworks/langgraph) *(publishing with the frameworks docs sprint)*
- LangChain integration: [pypi.org/project/langchain-ferrolabsai](https://pypi.org/project/langchain-ferrolabsai/)
- Gateway routing: [docs.ferrolabs.ai/guides/routing-policies](https://docs.ferrolabs.ai/guides/routing-policies)

## Related recipes

- `01-langchain-fallback-chain` *(planned)* — same idea, but with provider fallback inside a single node.
- `04-langsmith-tracing` *(planned)* — pair this recipe with the `langsmith-bridge` plugin so the three `trace_id`s above show up as LangSmith runs.
