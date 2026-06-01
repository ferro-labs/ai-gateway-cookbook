# <Recipe Title>

> Replace this block with a one-sentence pitch: what this recipe demonstrates and why a reader should care.

<!-- Optional: drop a 60s screencast GIF here once recorded -->

## What it demonstrates

- Bullet 1 — the headline Ferro feature this recipe shows.
- Bullet 2 — secondary feature or framework integration.
- Bullet 3 — what the reader will be able to do after running this.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- A running Ferro Labs AI Gateway (`http://localhost:8080` by default — set `FERRO_BASE_URL` to point elsewhere).
- Provider API keys for: `<list providers — e.g., OpenAI, Anthropic, Gemini>`.

## How to run

```bash
cp .env.example .env
# Edit .env and fill in FERRO_API_KEY + FERRO_BASE_URL if not localhost.
# Provider keys stay on the gateway side.
make test
make run
```

Expected output: `<one or two lines describing what success looks like>`.

## What to look for

- `trace_id` printed alongside each response — that's the Ferro request ID, propagated as the `x-trace-id` header (frozen contract since `ai-gateway v1.1.0`).
- `<feature-specific signal>` — e.g., "Notice the planner step routed to gpt-4o, the coder step routed to claude-3-5-sonnet".

## How it works

Brief walkthrough of the code. Reference the source file(s). Keep this section under ~30 lines.

## Docs

- Framework page: `<link to ferrolabs-docs/docs/frameworks/<framework>.mdx>`
- Ferro feature: `<link to the relevant guide in ferrolabs-docs>`

## Related recipes

- `<link to a logically-next recipe>`
- `<link to an alternative-framework version of the same recipe>`
