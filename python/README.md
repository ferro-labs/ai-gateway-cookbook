# Python Recipes

Python recipes that pair Ferro Labs AI Gateway with popular Python LLM frameworks.

All recipes:

- Use [`ferrolabsai`](https://pypi.org/project/ferrolabsai/) as the SDK base.
- Use the official integration package where it exists (e.g., [`langchain-ferrolabsai`](https://pypi.org/project/langchain-ferrolabsai/), [`llama-index-llms-ferrolabsai`](https://pypi.org/project/llama-index-llms-ferrolabsai/)).
- Run via `cp .env.example .env && make run`.

| Recipe | Frameworks | Status |
|---|---|---|
| [`02-langgraph-multi-provider-agent`](02-langgraph-multi-provider-agent/) | LangGraph + `langchain-ferrolabsai` | ✅ Ready (requires `langchain-ferrolabsai>=0.1.0`) |
| `01-langchain-fallback-chain` | LangChain | Planned |
| `03-rag-with-cost-routing` | LangChain + pgvector | Planned |
| `04-langsmith-tracing` | LangChain + LangSmith | Planned |
| `05-llamaindex-cheap-embeddings` | LlamaIndex | Planned |
| `06-crewai-team-multi-llm` | CrewAI | Planned |
| `07-dspy-optimizer-with-ferro` | DSPy | Planned |
| `08-evals-promptfoo-vs-ferro` | promptfoo | Planned |
| `09-guardrails-pii-redaction` | guardrails | Planned |

See the root [`README.md`](../README.md) for the full cookbook overview and the [`_template/`](../_template/) directory for the recipe scaffold.
