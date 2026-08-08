# <Recipe Title>

> Replace this block with a one-sentence pitch: what this recipe demonstrates and why a reader should care.

<!-- Optional: drop a 60s screencast GIF here once recorded -->

## What it demonstrates

- Bullet 1 — the headline Ferro feature this recipe shows.
- Bullet 2 — secondary feature or framework integration.
- Bullet 3 — what the reader will be able to do after running this.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) (Compose v2).
- Provider API keys for: `<list providers — e.g., OpenAI, Anthropic, Gemini>`.

No separate gateway setup: `docker compose up` starts the Ferro gateway
(published image) **and** this recipe, pre-wired.

## How to run

```bash
cp .env.example .env
# Fill in MASTER_KEY and the provider keys this recipe needs.
make run     # docker compose up: starts gateway + recipe together
```

Run the mocked smoke test (no gateway, no provider calls, no keys):

```bash
make test
```

Already have a gateway running? Point `FERRO_BASE_URL` at it and leave the
provider keys blank — that gateway already holds them.

Expected output: `<one or two lines describing what success looks like>`.

## What to look for

- `trace_id` printed alongside each response — that's the Ferro request ID, propagated as the `X-Request-ID` header.
- `<feature-specific signal>` — e.g., "Notice the planner step routed to gpt-5.2, the coder step routed to claude-sonnet-4-6".

## How it works

Brief walkthrough of the code. Reference the source file(s). Keep this section under ~30 lines.

## Docs

- Framework page: `<link to ferrolabs-docs/docs/frameworks/<framework>.mdx>`
- Ferro feature: `<link to the relevant guide in ferrolabs-docs>`

## Related recipes

- `<link to a logically-next recipe>`
- `<link to an alternative-framework version of the same recipe>`
