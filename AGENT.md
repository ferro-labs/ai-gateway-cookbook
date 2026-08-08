# AGENT.md — AI Coding Agent Guide for ai-gateway-cookbook

This document gives AI coding agents the conventions for adding and maintaining recipes in the [Ferro Labs AI Gateway](https://github.com/ferro-labs/ai-gateway) cookbook.

---

## Project Overview

This repo holds **runnable, copy-pasteable recipes** showing how to use Ferro Labs AI Gateway with popular LLM frameworks (LangChain, LangGraph, LlamaIndex, CrewAI, Vercel AI SDK, Mastra, DSPy, …) and use cases (RAG, evals, guardrails, multi-provider routing).

- **Audience:** developers evaluating or already using Ferro who want a working starting point.
- **Promise:** every recipe runs in two minutes via `cp .env.example .env && make run`.
- **Scope:** Python + TypeScript. Go recipes link out to [`ai-gateway-examples`](https://github.com/ferro-labs/ai-gateway-examples).

---

## Repository Structure

```
ai-gateway-cookbook/
├── README.md                # Index of all recipes
├── AGENT.md                 # This file
├── CONTRIBUTING.md          # Human-facing contribution guide
├── LICENSE                  # Apache-2.0
├── _template/               # Recipe scaffold — copy this when adding a recipe
│   ├── README.md
│   ├── Dockerfile
│   ├── Makefile
│   ├── .env.example
│   └── recipe.py            # or recipe.ts — placeholder source
├── python/
│   └── <NN>-<slug>/         # Each recipe is a self-contained directory
└── typescript/
    └── <NN>-<slug>/
```

---

## Recipe Conventions

Every recipe directory MUST contain:

| File              | Required | Notes                                                        |
| ----------------- | -------- | ------------------------------------------------------------ |
| `README.md`       | ✅       | Use the `_template/README.md` skeleton                       |
| `docker-compose.yml` | ✅    | Gateway (pinned published image) + recipe service. Copy from `_template/` |
| `Dockerfile`      | ✅       | Self-contained recipe image. Multi-stage when it shortens runtime |
| `Makefile`        | ✅       | Must expose `run`, `test`, `down`, `clean`, `logs` targets   |
| `.env.example`    | ✅       | Every env var, with comments. Gateway-facing + provider keys |
| Source files      | ✅       | Small, focused, heavily commented                            |
| `requirements.txt` *(Python)* / `package.json` *(TS)* | ✅ | Pinned versions      |

### Naming

- Directory: `<NN>-<slug>` where `NN` is a two-digit ordinal **within the language folder** (e.g., `python/02-langgraph-multi-provider-agent`).
- `<slug>` is kebab-case, describes the recipe in 3–5 words.
- Numbering is not reserved globally — Python `02` and TypeScript `02` are independent.

### `make run` contract

`make run` MUST:

1. `docker compose up --build` — start the bundled gateway (pinned published
   image) and the recipe together, loading `.env` from the recipe directory.
2. Wait for the gateway to be healthy before the recipe calls it
   (`depends_on: condition: service_healthy`).
3. Run the recipe to completion and exit with the recipe's exit code
   (`--abort-on-container-exit --exit-code-from recipe`), or run until the user
   kills it for long-running demos.

The user has only done `cp .env.example .env` and filled values — nothing else.
The gateway is **consumed as its published image**, never vendored as source.
The image tag defaults to `latest` and is overridable via `GATEWAY_VERSION`
(set it to pin a specific release for reproducibility).

### `make test` contract

`make test` MUST run without live provider calls. Use mocked framework/model clients
to verify the recipe control flow, metadata surfacing, and output shape. It may
reuse the recipe Docker image so dependency versions match `make run`.

### Env vars

- Under compose, the recipe reaches the gateway at `http://gateway:8080` (the
  service name). `FERRO_API_KEY` equals the gateway's `MASTER_KEY`.
- Provider API keys (`OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, etc.) are read from
  `.env` and injected into the **gateway** container only — the recipe container
  never receives them, and recipe **code** never reads them. Never hardcode keys.
- If the user points `FERRO_BASE_URL` at an existing gateway instead of the
  bundled one, the provider keys are left blank (that gateway already holds them).
- New env vars MUST appear in `.env.example` with a one-line comment describing them.

### `trace_id` surfacing

Recipes that demonstrate observability MUST surface the Ferro `trace_id` (returned in the `X-Request-ID` response header). For LangChain-style recipes, this means inspecting `response_metadata["trace_id"]`. This is the join key for any downstream observability bridge (LangSmith, Langfuse, Phoenix).

---

## Adding a New Recipe (step-by-step)

1. **Pick a number.** Use the next free `NN` in the target language folder.
2. **Copy the template.**
   ```bash
   cp -r _template python/<NN>-<slug>
   ```
3. **Edit `README.md`** — fill in: title, what it demonstrates, prerequisites, how to run, what to look for, docs link, related recipes.
4. **Edit `.env.example`** — declare every env var the recipe reads.
5. **Edit `Dockerfile`** — use the language's official slim base image. Pin dependencies.
6. **Edit `Makefile`** — usually only the image tag changes from the template.
7. **Write the recipe source.** Smallest possible code that shows the Ferro feature. Comment liberally.
8. **Verify tests and the end-to-end run** from a fresh clone:
   ```bash
   git clean -fdx <recipe-dir>
   make test
   cp .env.example .env && # fill values
   make run
   ```
9. **Update the root `README.md`** — add a row to the recipes table for the new recipe.
10. **Link from `ferrolabs-docs`** — open a PR in `ferrolabs-docs` adding a link from the relevant `docs/frameworks/*.mdx` page.

---

## Code Style

### Python recipes

- Python 3.10+ syntax. Type hints on every public function.
- `ruff format` + `ruff check` clean. Line length 100.
- Pin dependencies in `requirements.txt`.
- Use exact versions for direct runtime dependencies.
- Use the official integration package where it exists (`langchain-ferrolabsai`, `llama-index-llms-ferrolabsai`) — do not re-implement adapters inside a recipe.

### TypeScript recipes

- Node 18+ / TypeScript 5+.
- ESM by default. Use `tsx` for `make run`.
- Pin dependencies in `package.json`. Prefer exact versions for recipe reproducibility.
- Use `@ferro-labs-ai/sdk` (and `@ferro-labs-ai/sdk/langchain` when shipped).

### Documentation style

- READMEs are scannable. Lead with what the recipe does and how to run it. Explanation comes after.
- Code blocks specify language for syntax highlighting.
- Outbound links use absolute URLs.

---

## Common Pitfalls

- **Do not commit `.env`.** Only `.env.example` is checked in. `.gitignore` already blocks `.env`.
- **Do not hardcode API keys**, even fake ones, in source files or fixtures.
- **Do not assume the gateway is running on `localhost`.** Always read `FERRO_BASE_URL`.
- **Do not pull in heavy framework dependencies** in a recipe that only needs one feature — keep the dependency graph minimal.
- **Do not number recipes globally.** Each language folder has its own `NN` sequence.
- **Do not embed LangSmith / Langfuse / observability vendor SDKs in a recipe.** Observability is the gateway's job via its observability plugins (`langsmith`, `langfuse`, `phoenix`); recipes surface `trace_id` and stop there.

---

## Related Repositories

- [`ai-gateway`](https://github.com/ferro-labs/ai-gateway) — the gateway (Go core, OTel-native, v1.4.x)
- [`ai-gateway-examples`](https://github.com/ferro-labs/ai-gateway-examples) — raw Go examples
- [`ferrolabs-python-sdk`](https://github.com/ferro-labs/ferrolabs-python-sdk) — Python SDK + `integrations/` framework adapters
- [`ferrolabs-typescript-sdk`](https://github.com/ferro-labs/ferrolabs-typescript-sdk) — TypeScript SDK
- [`ferrolabs-docs`](https://github.com/ferro-labs/ferrolabs-docs) — documentation site, including `frameworks/` pages each recipe should link from
