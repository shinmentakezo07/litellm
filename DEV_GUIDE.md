# LiteLLM Development Guide

## 🎉 Setup Complete!

Your LiteLLM development environment is running from source code.

### Services Running

| Service | Status | URL/Port |
|---------|--------|----------|
| **Proxy Server** | ✅ Running | http://localhost:4000 |
| **PostgreSQL** | ✅ Running | localhost:5432 |
| **Swagger UI** | ✅ Available | http://localhost:4000/ |

**Master Key:** `sk-1234`

---

## 🚀 Quick Start

### 1. Add Your API Keys

Edit `.env` file:
```bash
OPENAI_API_KEY="sk-..."
ANTHROPIC_API_KEY="sk-ant-..."
GOOGLE_API_KEY="..."
GROQ_API_KEY="..."
```

### 2. Test the Setup

```bash
# Run test script
poetry run python test_litellm.py

# Check health
curl http://localhost:4000/health/readiness \
  -H "Authorization: Bearer sk-1234"

# List models
curl http://localhost:4000/v1/models \
  -H "Authorization: Bearer sk-1234"
```

### 3. Make Your First API Call

```bash
curl -X POST http://localhost:4000/v1/chat/completions \
  -H "Authorization: Bearer sk-1234" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4o",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

---

## 📚 Development Workflows

### Running Tests

```bash
# Run all unit tests
make test-unit

# Run specific test file
poetry run pytest tests/test_litellm/test_completion.py -v

# Run integration tests
make test-integration

# Run with coverage
poetry run pytest tests/ --cov=litellm --cov-report=html
```

### Code Quality

```bash
# Format code
make format

# Run all linters
make lint

# Run specific linters
make lint-ruff
make lint-mypy
```

### Working with the Proxy

```bash
# Start proxy with config
poetry run litellm --config proxy_server_config.yaml --port 4000

# Start with debug logging
poetry run litellm --config proxy_server_config.yaml --port 4000 --debug

# Start without database
poetry run litellm --model gpt-4o --port 4000
```

### Database Operations

```bash
# Generate Prisma client
poetry run prisma generate

# Create migration
poetry run prisma migrate dev --name your_migration_name

# Apply migrations
poetry run prisma migrate deploy

# Reset database
poetry run prisma migrate reset
```

---

## 💻 Using the Python SDK

### Direct Completion

```python
from litellm import completion

response = completion(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello!"}]
)
print(response.choices[0].message.content)
```

### Using the Proxy

```python
import openai

client = openai.OpenAI(
    api_key="sk-1234",
    base_url="http://localhost:4000"
)

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

### Router with Fallbacks

```python
from litellm import Router

router = Router(
    model_list=[
        {
            "model_name": "gpt-4",
            "litellm_params": {"model": "gpt-4o"}
        },
        {
            "model_name": "gpt-4",
            "litellm_params": {"model": "azure/gpt-4"}
        }
    ],
    fallbacks=[{"gpt-4": ["claude-sonnet-4"]}]
)

response = router.completion(
    model="gpt-4",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

See `examples_sdk.py` for more examples.

---

## 🔧 Configuration

### Proxy Config (`proxy_server_config.yaml`)

```yaml
model_list:
  - model_name: gpt-4
    litellm_params:
      model: openai/gpt-4o
      api_key: os.environ/OPENAI_API_KEY

litellm_settings:
  drop_params: true
  success_callback: ["prometheus"]
  num_retries: 3

general_settings:
  master_key: sk-1234
  database_url: "postgresql://..."
```

### Environment Variables (`.env`)

```bash
# Provider API Keys
OPENAI_API_KEY=""
ANTHROPIC_API_KEY=""
GOOGLE_API_KEY=""

# Database
DATABASE_URL="postgresql://llmproxy:dbpassword9090@localhost:5432/litellm"

# Proxy Settings
LITELLM_MASTER_KEY="sk-1234"
STORE_MODEL_IN_DB="True"
```

---

## 🌐 API Endpoints

### Core Endpoints

- `POST /v1/chat/completions` - Chat completions
- `POST /v1/completions` - Text completions
- `POST /v1/embeddings` - Generate embeddings
- `POST /v1/images/generations` - Generate images
- `GET /v1/models` - List models

### Management Endpoints

- `GET /health` - Health check
- `GET /health/readiness` - Readiness check
- `GET /model/info` - Model configuration
- `POST /key/generate` - Generate virtual keys
- `GET /spend/logs` - View spending logs

### Admin UI

Access the Swagger UI at: http://localhost:4000/

---

## 📖 Common Tasks

### Add a New Model

Edit `proxy_server_config.yaml`:

```yaml
model_list:
  - model_name: my-custom-model
    litellm_params:
      model: openai/gpt-4o
      api_key: os.environ/OPENAI_API_KEY
      rpm: 100  # Rate limit
      timeout: 60
```

Restart the proxy to apply changes.

### Create Virtual Keys

```bash
curl -X POST http://localhost:4000/key/generate \
  -H "Authorization: Bearer sk-1234" \
  -H "Content-Type: application/json" \
  -d '{
    "models": ["gpt-4o", "claude-sonnet-4"],
    "max_budget": 100,
    "duration": "30d"
  }'
```

### Enable Caching

Edit `proxy_server_config.yaml`:

```yaml
litellm_settings:
  cache: true
  cache_params:
    type: redis
    host: localhost
    port: 6379
```

### Add Logging/Observability

```yaml
litellm_settings:
  success_callback: ["langfuse", "prometheus"]
  langfuse_public_key: os.environ/LANGFUSE_PUBLIC_KEY
  langfuse_secret: os.environ/LANGFUSE_SECRET
```

---

## 🐛 Troubleshooting

### Proxy won't start

```bash
# Check if port is in use
netstat -tlnp | grep 4000

# Check database connection
docker ps | grep litellm_db

# View logs
tail -f /tmp/claude-1000/-teamspace-studios-this-studio-shinway/tasks/*.output
```

### Database errors

```bash
# Reset database
docker compose down -v
docker compose up -d db
poetry run prisma migrate deploy
```

### Import errors

```bash
# Reinstall dependencies
poetry install -E proxy
poetry run prisma generate
```

---

## 📁 Project Structure

```
litellm/
├── litellm/              # Core library
│   ├── main.py          # Main completion() function
│   ├── llms/            # Provider implementations
│   ├── proxy/           # Proxy server
│   │   ├── proxy_server.py
│   │   ├── auth/
│   │   └── management_endpoints/
│   ├── router.py        # Load balancing
│   └── types/           # Type definitions
├── tests/               # Test suite
├── proxy_server_config.yaml  # Proxy configuration
├── schema.prisma        # Database schema
└── pyproject.toml       # Dependencies
```

---

## 🎯 Next Steps

1. **Add your API keys** to `.env`
2. **Test with real providers** using `examples_sdk.py`
3. **Explore the codebase** in `litellm/`
4. **Run tests** with `make test-unit`
5. **Read the docs** at https://docs.litellm.ai

---

## 🛑 Stopping Services

```bash
# Stop proxy (if running in background)
pkill -f litellm

# Stop database
docker compose down

# Stop all
docker compose down && pkill -f litellm
```

---

## 📞 Getting Help

- **Documentation**: https://docs.litellm.ai
- **Discord**: https://discord.gg/wuPM9dRgDw
- **GitHub Issues**: https://github.com/BerriAI/litellm/issues
- **CLAUDE.md**: Project-specific guidance for Claude Code

---

**Status**: ✅ All systems operational
**Models loaded**: 289
**Version**: 1.81.14
