# Go Recipes

Go-native examples (embedding the gateway, custom plugins, hooks, MCP) live in a separate repo to keep this cookbook focused on framework-side integrations.

👉 **[`ferro-labs/ai-gateway-examples`](https://github.com/ferro-labs/ai-gateway-examples)**

Examples there cover:

- `basic` — single chat-completion request
- `streaming` — real-time token output
- `embeddings` — embedding requests through the gateway
- `fallback` — automatic provider fallback
- `loadbalance` — weighted load-balancing
- `conditional-routing` — route on request metadata
- `caching` — response caching
- `config-file` — drive the gateway from `config.yaml`
- `embedded` — mount the gateway inside your own `net/http` server
- `custom-plugin` — write and register a plugin
- `with-circuit-breaker`, `with-guardrails`, `with-hooks`, `with-mcp`

If you have a Go recipe that's framework-specific (e.g., LangChainGo, Genkit Go) and doesn't fit the existing examples repo, open an issue here first so we can decide whether it lives in the cookbook or the examples repo.
