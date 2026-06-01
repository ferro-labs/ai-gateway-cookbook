# TypeScript Recipes

TypeScript / Node recipes that pair Ferro Labs AI Gateway with popular JS/TS LLM frameworks.

All recipes:

- Use [`@ferro-labs-ai/sdk`](https://www.npmjs.com/package/@ferro-labs-ai/sdk) as the SDK base.
- Will use `@ferro-labs-ai/sdk/langchain` once shipped.
- Run via `cp .env.example .env && make run` (Docker-based; `tsx` inside the image).

| Recipe | Frameworks | Status |
|---|---|---|
| `01-vercel-ai-sdk-fallback` | Vercel AI SDK | Planned |
| `02-langchainjs-streaming-agent` | LangChain.js | Planned — needs `@ferro-labs-ai/sdk/langchain` |
| `03-mastra-workflow` | Mastra | Planned |
| `04-nextjs-chat-with-budget-plugin` | Next.js | Planned |

See the root [`README.md`](../README.md) for the full cookbook overview and the [`_template/`](../_template/) directory for the recipe scaffold (note: the template ships with Python defaults — swap to `node:20-slim` + `npm ci` + `tsx` for TypeScript recipes).
