"""
Recipe template — replace with your actual recipe.

Conventions:
  - Read configuration from env (never hardcode).
  - Print the Ferro `trace_id` from response metadata when available.
  - Keep the recipe under ~80 lines of focused code; comments are encouraged.
"""

from __future__ import annotations

import os
import sys

from ferrolabsai import FerroClient


def main() -> int:
    base_url = os.environ.get("FERRO_BASE_URL", "http://localhost:8080")
    api_key = os.environ.get("FERRO_API_KEY")
    if not api_key:
        print(
            "ERROR: FERRO_API_KEY is not set. Copy .env.example to .env and fill it in.",
            file=sys.stderr,
        )
        return 1

    client = FerroClient(api_key=api_key, base_url=base_url)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "Say hello from the Ferro cookbook."}],
    )

    print(response.choices[0].message.content)
    # `trace_id` is propagated by the gateway via the `x-trace-id` response header
    # (frozen contract since ai-gateway v1.1.0). Surface it so users can correlate
    # this call across logs, OTel traces, and any observability bridge plugin.
    print(f"trace_id={getattr(response, 'trace_id', None)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
