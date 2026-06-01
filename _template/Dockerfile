# Recipe template Dockerfile (Python flavour).
# For TypeScript recipes, swap to `node:20-slim` + `npm ci` + `tsx`.
FROM python:3.12-slim

WORKDIR /app

# Install dependencies first for layer caching.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source.
COPY . .

# Default entrypoint runs the recipe. Override with `docker run ... <cmd>` if needed.
CMD ["python", "recipe.py"]
