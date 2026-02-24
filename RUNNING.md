# LiteLLM Running Locally

## Services Running

### 1. PostgreSQL Database
- **Port**: 5432
- **Container**: litellm_db
- **Credentials**: llmproxy / dbpassword9090
- **Database**: litellm

### 2. LiteLLM Proxy Server
- **URL**: http://localhost:4000
- **Master Key**: sk-1234
- **Swagger UI**: http://localhost:4000/
- **Status**: ✅ Running

## Quick Start

### Test the Server
```bash
# Health check
curl http://localhost:4000/health/readiness \
  -H "Authorization: Bearer sk-1234"

# List models
curl http://localhost:4000/models \
  -H "Authorization: Bearer sk-1234"
```

### Make API Calls

#### Using Python SDK
```python
from litellm import completion

# Direct SDK usage (no proxy)
response = completion(
    model="gpt-4o",  # or any supported model
    messages=[{"role": "user", "content": "Hello!"}]
)
print(response)
```

#### Using OpenAI SDK with Proxy
```python
import openai

client = openai.OpenAI(
    api_key="sk-1234",  # LiteLLM master key
    base_url="http://localhost:4000"
)

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello!"}]
)
print(response)
```

#### Using cURL
```bash
curl -X POST http://localhost:4000/v1/chat/completions \
  -H "Authorization: Bearer sk-1234" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4o",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

## Configuration

### Add API Keys
Edit `.env` file to add your provider API keys:
```bash
OPENAI_API_KEY="your-key-here"
ANTHROPIC_API_KEY="your-key-here"
COHERE_API_KEY="your-key-here"
```

### Configure Models
Edit `proxy_server_config.yaml` to define available models and routing.

## Development Commands

```bash
# Start proxy server
export PATH="/teamspace/studios/this_studio/.local/bin:$PATH"
poetry run python litellm/proxy/proxy_cli.py --port 4000

# Run tests
make test-unit

# Format code
make format

# Lint code
make lint
```

## Stopping Services

```bash
# Stop proxy server (if running in background)
pkill -f proxy_cli.py

# Stop database
docker compose down
```

## Accessing the UI Dashboard

The Swagger UI is available at: http://localhost:4000/

## Next Steps

1. Add your LLM provider API keys to `.env`
2. Configure models in `proxy_server_config.yaml`
3. Create virtual keys for different users/teams
4. Set up logging, caching, and guardrails as needed

## Troubleshooting

- **Database connection issues**: Ensure PostgreSQL container is running with `docker ps`
- **Port already in use**: Change port with `--port` flag
- **Missing dependencies**: Run `poetry install -E proxy`
