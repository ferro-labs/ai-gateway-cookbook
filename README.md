<div align="center">
  <table border="0" cellspacing="0" cellpadding="0"><tr>
    <td rowspan="2"><img src="https://raw.githubusercontent.com/ferro-labs/ai-gateway/refs/heads/main/docs/logo.png" alt="Ferro Labs" width="64" /></td>
    <td align="center"><h1>Ferro Labs - AI Gateway</h1></td>
  </tr><tr>
    <td align="center"><strong>Cookbook</strong></td>
  </tr></table>
  <p>
    <a href="LICENSE"><img src="https://img.shields.io/badge/license-Apache%202.0-blue.svg" alt="License" /></a>
    <a href="https://github.com/ferro-labs/ai-gateway-cookbook"><img src="https://img.shields.io/badge/status-active-brightgreen.svg" alt="Status" /></a>
    <a href="#recipe-catalog"><img src="https://img.shields.io/badge/recipes-1%20live%20%2B%2012%20planned-blue.svg" alt="Recipe catalog" /></a>
    <a href="#quickstart"><img src="https://img.shields.io/badge/Python-3.10%2B-3776AB.svg" alt="Python 3.10+" /></a>
    <a href="#recipe-catalog"><img src="https://img.shields.io/badge/Node-18%2B-339933.svg" alt="Node 18+" /></a>
    <a href="#recipe-contract"><img src="https://img.shields.io/badge/Docker-ready-2496ED.svg" alt="Docker ready" /></a>
    <a href="https://discord.gg/yCAeYvJeDV"><img src="https://img.shields.io/badge/Discord-Join-5865F2.svg" alt="Discord" /></a>
  </p>
</div>

The official cookbook for [Ferro Labs AI Gateway](https://github.com/ferro-labs/ai-gateway): runnable, framework-focused recipes that show how to build agents and LLM apps across OpenAI, Anthropic, Gemini, and other providers through one gateway endpoint.

Use this repo when you want a working example, not just an API snippet. Each recipe is self-contained, Dockerized, and shaped around a real integration such as LangGraph, LangChain, LlamaIndex, CrewAI, Vercel AI SDK, Mastra, DSPy, evals, or guardrails.

Recipes are validated against **ai-gateway v1.4.1** (`ghcr.io/ferro-labs/ai-gateway:1.4.1`), `ferrolabsai` 0.2.1, `langchain-ferrolabsai` 0.1.0, and `@ferro-labs-ai/sdk` 0.2.0.

---

## What This Is For

| Need | Use this cookbook for |
|---|---|
| Evaluate Ferro quickly | Run a complete recipe with `cp .env.example .env && make run`. |
| Adopt a framework | See the exact LangChain, LangGraph, LlamaIndex, CrewAI, Vercel AI SDK, or Mastra wiring. |
| Prove multi-provider routing | Route different model calls through one `FERRO_BASE_URL` without provider SDKs in app code. |
| Correlate requests | Print Ferro `trace_id` values so gateway logs, OTel traces, and the `langsmith` / `langfuse` / `phoenix` observability plugins share a join key. |
| Build a new demo | Copy `_template/` and follow the same `README.md`, `Dockerfile`, `.env.example`, and `Makefile` contract. |

Looking for raw Go gateway examples instead? Use [`ai-gateway-examples`](https://github.com/ferro-labs/ai-gateway-examples). This cookbook is for framework and application recipes.

---

## Quickstart

Each recipe is self-bootstrapping: `docker compose up` starts the Ferro Labs AI
Gateway (its published image) **and** the recipe together, pre-wired. The only
thing you supply is a `MASTER_KEY` and the provider keys that recipe needs.

```bash
cd python/02-langgraph-multi-provider-agent
cp .env.example .env
# Fill in MASTER_KEY + provider keys (OPENAI/ANTHROPIC/GEMINI for this recipe).

make test   # mocked smoke test — no gateway, no provider calls, no keys
make run    # docker compose up: gateway + recipe, one command
```

Provider keys are injected into the **gateway** container only — recipe code
never sees them (it only knows `FERRO_BASE_URL` + `FERRO_API_KEY`).

Gateway options:

| Option | When to use | Setup |
|---|---|---|
| Bundled gateway (default) | OSS development and local demos | `make run` / `docker compose up` — the recipe pulls `ghcr.io/ferro-labs/ai-gateway:latest` (set `GATEWAY_VERSION` to pin a release). |
| Existing / remote gateway | Shared staging, FerroCloud, or team gateway | Set `FERRO_BASE_URL` to it and leave provider keys blank — it already holds them. |

---

## First Recipe

[`python/02-langgraph-multi-provider-agent`](python/02-langgraph-multi-provider-agent/) is the first public recipe and the recommended starting point.

It builds a three-node LangGraph agent:

| Step | Model | Provider role | What it proves |
|---|---|---|---|
| Planner | `gpt-5.2` | OpenAI reasoning | One graph can call an OpenAI model through Ferro. |
| Coder | `claude-sonnet-4-6` | Anthropic code quality | The next graph node can switch providers with only the model name changed. |
| Summarizer | `gemini-2.5-flash` | Google fast summary | Cheap/fast tasks can route to a different provider through the same endpoint. |

The app prints one Ferro `trace_id` per node. Those IDs are the join key for request logs, OpenTelemetry traces, and observability bridge plugins such as LangSmith, Langfuse, and Phoenix.

---

## Recipe Catalog

### Python

| Status | Recipe | Frameworks | Demonstrates |
|---|---|---|---|
| Live | [`02-langgraph-multi-provider-agent`](python/02-langgraph-multi-provider-agent/) | LangGraph + `langchain-ferrolabsai` | Planner=gpt-5.2, coder=claude, summarizer=gemini in one agent. |
| Planned | `01-langchain-fallback-chain` | LangChain | Provider fallback through Ferro. |
| Planned | `03-rag-with-cost-routing` | LangChain + pgvector | Cheap-then-smart routing for RAG. |
| Planned | `04-langsmith-tracing` | LangChain + LangSmith | Ferro `trace_id` to LangSmith run linkage. |
| Planned | `05-llamaindex-cheap-embeddings` | LlamaIndex | Cost-routed embeddings. |
| Planned | `06-crewai-team-multi-llm` | CrewAI | Per-agent model selection. |
| Planned | `07-dspy-optimizer-with-ferro` | DSPy | Optimizer workloads through Ferro. |
| Planned | `08-evals-promptfoo-vs-ferro` | promptfoo | Eval harness with provider switching. |
| Planned | `09-guardrails-pii-redaction` | guardrails | PII redaction through gateway plugins. |

### TypeScript

| Status | Recipe | Frameworks | Demonstrates |
|---|---|---|---|
| Planned | `01-vercel-ai-sdk-fallback` | Vercel AI SDK | Provider fallback from a TS app. |
| Planned | `02-langchainjs-streaming-agent` | LangChain.js | Streaming tool-calling agent. |
| Planned | `03-mastra-workflow` | Mastra | Workflow with multi-provider routing. |
| Planned | `04-nextjs-chat-with-budget-plugin` | Next.js | Chat app with the Ferro budget plugin. |

### Go

Go-native gateway examples live in [`ai-gateway-examples`](https://github.com/ferro-labs/ai-gateway-examples). This keeps the cookbook focused on framework and app-level recipes.

---

## Repository Layout

```text
.
├── _template/          # Copy this when adding a new recipe
├── python/             # Python framework recipes
│   └── 02-langgraph-multi-provider-agent/
├── typescript/         # TypeScript framework recipes
└── go/                 # Pointer to ai-gateway-examples
```

Each recipe ships with the same file shape:

| File | Purpose |
|---|---|
| `README.md` | What the recipe demonstrates, prerequisites, how to run, and what to look for. |
| `docker-compose.yml` | Starts the pinned gateway image + the recipe together (the one-command experience). |
| `Dockerfile` | Self-contained recipe runtime image. |
| `Makefile` | Standard `make run`, `make test`, `make down`, `make clean`, `make logs` targets. |
| `.env.example` | Every env var: gateway-facing (`FERRO_BASE_URL`, `MASTER_KEY`) and the provider keys the bundled gateway needs. |
| Source files | Small, focused implementation for the recipe. |
| Tests | Mocked smoke tests that run without a gateway or live provider calls. |

---

## Recipe Contract

Every recipe should satisfy these rules before it is published:

- `make test` runs without a gateway or provider calls and checks the important control flow.
- `cp .env.example .env && make run` gets a user to a real request quickly (one command, gateway + recipe).
- The recipe ships a `docker-compose.yml` that consumes the gateway's **published image** (defaults to `latest`; pin via `GATEWAY_VERSION`) — never vendored gateway source.
- Provider keys are injected into the **gateway** container only; recipe code reads just `FERRO_BASE_URL` + `FERRO_API_KEY`.
- Direct runtime dependencies are pinned for reproducibility.
- The recipe uses official Ferro SDK/framework adapters where they exist.
- The README links back to the matching page in [`ferrolabs-docs`](https://github.com/ferro-labs/ferrolabs-docs).
- Observability-oriented recipes surface `trace_id` from response metadata.

---

## Adding A Recipe

1. Copy `_template/` to `python/<NN>-<slug>/` or `typescript/<NN>-<slug>/`.
2. Update `README.md`, `.env.example`, `Dockerfile`, `Makefile`, dependencies, and source files.
3. Add a mocked smoke test and verify `make test`.
4. Run the recipe from a fresh `.env` and verify `make run`.
5. Add the recipe to the catalog above.
6. Link it from the matching `ferrolabs-docs/docs/frameworks/*.mdx` page.
7. Add a short screencast GIF when the recipe is ready for promotion.

See [`CONTRIBUTING.md`](CONTRIBUTING.md) and [`AGENT.md`](AGENT.md) for the full checklist and automation conventions.

---

## Ecosystem

| Repo | Purpose |
|---|---|
| [`ai-gateway`](https://github.com/ferro-labs/ai-gateway) | The OSS gateway: providers, routing, plugins, admin API, OTel. |
| [`ai-gateway-cookbook`](https://github.com/ferro-labs/ai-gateway-cookbook) | Runnable framework and app recipes. |
| [`ai-gateway-examples`](https://github.com/ferro-labs/ai-gateway-examples) | Go-native examples for embedding or calling the gateway. |
| [`ferrolabs-python-sdk`](https://github.com/ferro-labs/ferrolabs-python-sdk) | Python SDK and framework adapter packages. |
| [`ferrolabs-typescript-sdk`](https://github.com/ferro-labs/ferrolabs-typescript-sdk) | TypeScript SDK. |
| [`ferrolabs-docs`](https://github.com/ferro-labs/ferrolabs-docs) | Product docs, framework guides, and deployment guides. |

Community: [Discord](https://discord.gg/yCAeYvJeDV)
