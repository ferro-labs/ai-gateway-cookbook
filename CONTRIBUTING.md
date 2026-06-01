# Contributing to ai-gateway-cookbook

Thanks for adding a recipe — that's the single highest-leverage way to grow Ferro adoption.

## Before you start

- Skim [`AGENT.md`](AGENT.md) — it has the full conventions (file layout, `make run` contract, env-var rules, `trace_id` surfacing).
- Check the [recipe catalog in the README](README.md#recipe-catalog) to make sure your recipe doesn't already exist or have a planned slot.
- If you're proposing a brand-new pattern (not on the planned list), open an issue first so we can confirm the slot and number before you build it.

## The five-minute checklist

1. **Copy the template.**
   ```bash
   cp -r _template python/<NN>-<your-slug>
   ```
2. **Fill in the README** (title, what it shows, how to run, docs link).
3. **Edit `.env.example`** so a fresh clone can fill it and go.
4. **Pin your dependencies** (`requirements.txt` or `package.json`).
5. **Add or update a mocked smoke test** so `make test` runs without live provider calls.
6. **Run from a fresh clone** to verify the two-minute promise holds:
   ```bash
   git clean -fdx <recipe-dir>
   make test
   cp .env.example .env  # fill in values
   make run
   ```

## What makes a great recipe

- **One feature, smallest code.** Recipes are demonstrations, not products.
- **Two minutes to first response.** If `make run` doesn't print useful output within two minutes of cloning, rework it.
- **Real provider routing.** Recipes prove Ferro's value — multi-provider, fallback, cost routing, tracing. Don't ship a recipe that could run against raw OpenAI unchanged.
- **`trace_id` everywhere.** Surface the Ferro trace ID anywhere the framework exposes response metadata. This is the join key for the v1.2 observability bridges.
- **No provider secrets in recipe `.env`.** Provider API keys belong in the gateway runtime or gateway config. Recipes only need gateway-facing settings such as `FERRO_BASE_URL` and `FERRO_API_KEY`.
- **A screencast GIF** at the top of the README (60 seconds max) closes the loop visually.

## PR process

- Branch from `main`, PR back to `main`.
- One recipe per PR.
- Update the root `README.md` recipes table in the same PR.
- Open a companion PR in [`ferrolabs-docs`](https://github.com/ferro-labs/ferrolabs-docs) linking the recipe from the matching `docs/frameworks/*.mdx` page.

## Code of conduct

By participating you agree to follow the [Ferro Labs Code of Conduct](https://github.com/ferro-labs/.github/blob/main/CODE_OF_CONDUCT.md).
