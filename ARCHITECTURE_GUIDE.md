# LiteLLM Codebase Architecture Guide

## 📁 Project Structure

```
litellm/
├── litellm/                          # Core library
│   ├── main.py                       # Main entry point - completion() function
│   ├── router.py                     # Load balancing & routing logic
│   ├── _logging.py                   # Logging infrastructure
│   │
│   ├── llms/                         # Provider implementations (115+ providers)
│   │   ├── base_llm/                 # Base classes for all providers
│   │   ├── openai/                   # OpenAI implementation
│   │   ├── anthropic/                # Anthropic/Claude implementation
│   │   ├── azure/                    # Azure OpenAI implementation
│   │   ├── bedrock/                  # AWS Bedrock implementation
│   │   ├── vertex_ai/                # Google Vertex AI
│   │   └── ...                       # 110+ other providers
│   │
│   ├── proxy/                        # Proxy server (AI Gateway)
│   │   ├── proxy_server.py           # FastAPI application
│   │   ├── proxy_cli.py              # CLI entry point
│   │   ├── auth/                     # Authentication & authorization
│   │   ├── management_endpoints/     # Admin APIs
│   │   ├── pass_through_endpoints/   # Provider-specific forwarding
│   │   └── guardrails/               # Safety & content filtering
│   │
│   ├── types/                        # Type definitions (Pydantic models)
│   │   ├── completion.py             # Completion types
│   │   ├── router.py                 # Router types
│   │   └── utils.py                  # Utility types
│   │
│   ├── caching/                      # Cache implementations
│   │   ├── caching.py                # Base caching logic
│   │   ├── redis_cache.py            # Redis backend
│   │   ├── s3_cache.py               # S3 backend
│   │   └── in_memory_cache.py        # In-memory backend
│   │
│   ├── integrations/                 # Third-party integrations
│   │   ├── langfuse.py               # Langfuse observability
│   │   ├── prometheus.py             # Prometheus metrics
│   │   ├── datadog.py                # Datadog monitoring
│   │   └── ...                       # 20+ other integrations
│   │
│   ├── router_utils/                 # Router utilities
│   │   ├── cooldown_callbacks.py     # Cooldown logic
│   │   ├── health_check.py           # Health checking
│   │   └── router_callbacks.py       # Router callbacks
│   │
│   └── utils.py                      # Core utilities
│
├── tests/                            # Test suite
│   ├── test_litellm/                 # Unit tests
│   ├── llm_translation/              # Provider integration tests
│   ├── proxy_unit_tests/             # Proxy tests
│   └── load_tests/                   # Performance tests
│
├── schema.prisma                     # Database schema (Prisma ORM)
├── proxy_server_config.yaml          # Proxy configuration
├── pyproject.toml                    # Dependencies & project config
└── Makefile                          # Development commands
```

---

## 🔧 Key Components

### 1. Core Completion Flow (`litellm/main.py`)

The main `completion()` function is the entry point for all LLM calls:

```python
from litellm import completion

response = completion(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello"}]
)
```

**Flow:**
1. Parse model name → determine provider
2. Get provider-specific config from `llms/{provider}/`
3. Transform request to provider format
4. Make HTTP request via `HTTPHandler`
5. Transform response to OpenAI format
6. Log via callbacks (Langfuse, Prometheus, etc.)
7. Return standardized response

### 2. Provider Implementation (`litellm/llms/`)

Each provider has its own directory with:
- `chat/completion.py` - Chat completion logic
- `embedding/embedding.py` - Embedding logic
- `common_utils.py` - Provider-specific utilities
- `transformation.py` - Request/response transformation

**Example: Adding a new provider**

```python
# litellm/llms/my_provider/chat/completion.py

from litellm.llms.base_llm.chat.transformation import BaseLLMException

class MyProviderConfig(BaseLLMException):
    def transform_request(self, messages, optional_params):
        # Transform OpenAI format → Provider format
        return provider_request

    def transform_response(self, response):
        # Transform Provider format → OpenAI format
        return openai_response
```

### 3. Router (`litellm/router.py`)

Handles load balancing, fallbacks, and retries:

```python
from litellm import Router

router = Router(
    model_list=[
        {"model_name": "gpt-4", "litellm_params": {"model": "gpt-4o"}},
        {"model_name": "gpt-4", "litellm_params": {"model": "azure/gpt-4"}},
    ],
    fallbacks=[{"gpt-4": ["claude-sonnet-4"]}],
    routing_strategy="simple-shuffle"
)
```

**Features:**
- Load balancing across deployments
- Automatic fallbacks on failure
- Rate limit handling
- Health checks
- Cost tracking

### 4. Proxy Server (`litellm/proxy/`)

FastAPI application that provides:
- OpenAI-compatible API endpoints
- Virtual key management
- Multi-tenant support
- Budget tracking
- Admin dashboard

**Key files:**
- `proxy_server.py` - Main FastAPI app
- `auth/user_api_key_auth.py` - Authentication
- `management_endpoints/key_management_endpoints.py` - Key CRUD
- `management_endpoints/team_endpoints.py` - Team management

### 5. Caching (`litellm/caching/`)

Multiple cache backends:
- Redis (production)
- S3 (long-term storage)
- In-memory (development)
- DynamoDB (AWS)

**Usage:**
```python
from litellm import completion

completion(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello"}],
    caching=True  # Enable caching
)
```

### 6. Integrations (`litellm/integrations/`)

Observability and logging:
- **Langfuse** - LLM observability
- **Prometheus** - Metrics
- **Datadog** - APM
- **Sentry** - Error tracking
- **Weights & Biases** - Experiment tracking

---

## 🛠️ Development Workflows

### Adding a New Provider

1. **Create provider directory:**
```bash
mkdir -p litellm/llms/my_provider/chat
touch litellm/llms/my_provider/__init__.py
touch litellm/llms/my_provider/chat/completion.py
```

2. **Implement transformation:**
```python
# litellm/llms/my_provider/chat/completion.py

from litellm.llms.base_llm.chat.transformation import BaseLLMException

class MyProviderConfig(BaseLLMException):
    def __init__(self):
        super().__init__()

    def transform_request(self, messages, optional_params):
        # Convert OpenAI format to provider format
        return {
            "prompt": messages[-1]["content"],
            "max_tokens": optional_params.get("max_tokens", 100)
        }

    def transform_response(self, response):
        # Convert provider format to OpenAI format
        return {
            "choices": [{
                "message": {
                    "role": "assistant",
                    "content": response["text"]
                }
            }]
        }
```

3. **Register provider:**
```python
# litellm/llms/__init__.py

from .my_provider.chat.completion import MyProviderConfig

PROVIDER_MAP = {
    "my_provider": MyProviderConfig,
    # ... other providers
}
```

4. **Add tests:**
```python
# tests/llm_translation/test_my_provider.py

def test_my_provider_completion():
    response = completion(
        model="my_provider/my-model",
        messages=[{"role": "user", "content": "Hello"}]
    )
    assert response.choices[0].message.content
```

### Modifying Existing Functionality

**Example: Add custom logging**

```python
# litellm/integrations/my_logger.py

from litellm.integrations.custom_logger import CustomLogger

class MyLogger(CustomLogger):
    def log_success_event(self, kwargs, response_obj, start_time, end_time):
        print(f"Success! Model: {kwargs['model']}")
        print(f"Duration: {end_time - start_time}s")

    def log_failure_event(self, kwargs, response_obj, start_time, end_time):
        print(f"Failed! Error: {response_obj}")

# Register logger
litellm.callbacks = [MyLogger()]
```

### Running Tests

```bash
# Run all unit tests
make test-unit

# Run specific test file
poetry run pytest tests/test_litellm/test_completion.py -v

# Run with specific provider
poetry run pytest tests/llm_translation/test_openai.py -v

# Run with coverage
poetry run pytest tests/ --cov=litellm --cov-report=html

# Run integration tests
make test-integration
```

### Debugging

```bash
# Enable debug logging
export LITELLM_LOG=DEBUG

# Run with verbose output
poetry run python -m litellm --debug

# Use Python debugger
poetry run python -m pdb your_script.py
```

---

## 📊 Database Schema

The proxy uses Prisma ORM with PostgreSQL:

```prisma
// schema.prisma

model LiteLLM_VerificationToken {
  token           String   @id
  key_name        String?
  key_alias       String?
  spend           Float    @default(0.0)
  max_budget      Float?
  expires         DateTime?
  models          String[]
  aliases         Json?
  config          Json?
  user_id         String?
  team_id         String?
  created_at      DateTime @default(now())
  updated_at      DateTime @default(now()) @updatedAt
}

model LiteLLM_SpendLogs {
  request_id      String   @id
  api_key         String
  model           String
  spend           Float
  total_tokens    Int
  prompt_tokens   Int
  completion_tokens Int
  startTime       DateTime
  endTime         DateTime
  created_at      DateTime @default(now())
}
```

**Working with database:**

```bash
# Generate Prisma client
poetry run prisma generate

# Create migration
poetry run prisma migrate dev --name add_new_field

# Apply migrations
poetry run prisma migrate deploy

# View database
poetry run prisma studio
```

---

## 🎯 Common Development Tasks

### 1. Add Support for New Model Parameter

```python
# litellm/utils.py

def get_optional_params(
    model: str,
    temperature: Optional[float] = None,
    my_new_param: Optional[str] = None,  # Add here
    **kwargs
):
    optional_params = {}
    if temperature is not None:
        optional_params["temperature"] = temperature
    if my_new_param is not None:
        optional_params["my_new_param"] = my_new_param
    return optional_params
```

### 2. Add Custom Callback

```python
# my_callback.py

from litellm.integrations.custom_logger import CustomLogger

class MyCallback(CustomLogger):
    def log_pre_api_call(self, model, messages, kwargs):
        print(f"Calling {model}")

    def log_post_api_call(self, kwargs, response_obj, start_time, end_time):
        print(f"Response received in {end_time - start_time}s")

# Use it
import litellm
litellm.callbacks = [MyCallback()]
```

### 3. Add Custom Router Strategy

```python
# litellm/router_strategy/my_strategy.py

def my_routing_strategy(model_list, messages, **kwargs):
    # Custom logic to select deployment
    return selected_deployment

# Register in router.py
ROUTING_STRATEGIES = {
    "my-strategy": my_routing_strategy,
    # ... other strategies
}
```

---

## 🔍 Code Navigation Tips

### Finding Provider Implementation

```bash
# Find where OpenAI completion is implemented
grep -r "def openai_completion" litellm/

# Find all provider configs
find litellm/llms -name "common_utils.py"

# Find where model is parsed
grep -r "get_llm_provider" litellm/
```

### Understanding Request Flow

1. `litellm/main.py:completion()` - Entry point
2. `litellm/utils.py:get_llm_provider()` - Determine provider
3. `litellm/llms/{provider}/chat/completion.py` - Provider logic
4. `litellm/_logging.py` - Logging callbacks
5. Return standardized response

### Key Files to Know

- `litellm/main.py` - Main completion function
- `litellm/utils.py` - Core utilities
- `litellm/router.py` - Router logic
- `litellm/proxy/proxy_server.py` - Proxy server
- `litellm/types/completion.py` - Type definitions
- `litellm/exceptions.py` - Exception classes

---

## 📚 Additional Resources

- **Official Docs**: https://docs.litellm.ai
- **Contributing Guide**: CONTRIBUTING.md
- **Architecture Doc**: ARCHITECTURE.md
- **API Reference**: https://docs.litellm.ai/docs/api-reference
- **Provider Docs**: https://docs.litellm.ai/docs/providers

---

## 🚀 Next Steps for Development

1. **Explore a provider implementation**: Read `litellm/llms/openai/chat/completion.py`
2. **Understand the router**: Read `litellm/router.py`
3. **Check proxy endpoints**: Read `litellm/proxy/proxy_server.py`
4. **Run tests**: `make test-unit`
5. **Make a change**: Add a custom callback or modify a provider
6. **Submit PR**: Follow CONTRIBUTING.md guidelines

The codebase is well-structured and modular - each provider is isolated, making it easy to add new ones or modify existing functionality.
