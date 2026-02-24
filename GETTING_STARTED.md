# 🚀 Getting Started with LiteLLM - Your First API Call

Now that LiteLLM is running, let's make your first API call!

## Quick Start (5 minutes)

### Step 1: Add Your API Key

Choose one provider to start with:

```bash
# Edit .env file
nano .env

# Add ONE of these (whichever you have):
OPENAI_API_KEY="sk-..."
# OR
ANTHROPIC_API_KEY="sk-ant-..."
# OR
GOOGLE_API_KEY="..."
```

### Step 2: Restart the Proxy

```bash
# Stop current proxy
pkill -f litellm

# Start with config
poetry run litellm --config proxy_server_config.yaml --port 4000
```

### Step 3: Make Your First Call

**Option A: Using cURL**

```bash
curl -X POST http://localhost:4000/v1/chat/completions \
  -H "Authorization: Bearer sk-1234" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4o",
    "messages": [
      {"role": "user", "content": "Say hello!"}
    ]
  }'
```

**Option B: Using Python**

```python
import openai

client = openai.OpenAI(
    api_key="sk-1234",
    base_url="http://localhost:4000"
)

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Say hello!"}]
)

print(response.choices[0].message.content)
```

**Option C: Using LiteLLM SDK**

```python
from litellm import completion

response = completion(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Say hello!"}]
)

print(response.choices[0].message.content)
```

---

## Common Use Cases

### 1. Chat Application

```python
import openai

client = openai.OpenAI(
    api_key="sk-1234",
    base_url="http://localhost:4000"
)

def chat(message: str, history: list = None):
    if history is None:
        history = []

    history.append({"role": "user", "content": message})

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=history
    )

    assistant_message = response.choices[0].message.content
    history.append({"role": "assistant", "content": assistant_message})

    return assistant_message, history

# Usage
response, history = chat("What is Python?")
print(response)

response, history = chat("Give me an example", history)
print(response)
```

### 2. Streaming Chat

```python
def stream_chat(message: str):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": message}],
        stream=True
    )

    for chunk in response:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)
    print()

stream_chat("Write a short poem about coding")
```

### 3. Multiple Providers with Fallback

```python
from litellm import Router

router = Router(
    model_list=[
        {
            "model_name": "my-model",
            "litellm_params": {
                "model": "gpt-4o",
                "api_key": "sk-..."
            }
        },
        {
            "model_name": "my-model",
            "litellm_params": {
                "model": "anthropic/claude-sonnet-4",
                "api_key": "sk-ant-..."
            }
        }
    ],
    fallbacks=[{"my-model": ["my-model"]}]
)

response = router.completion(
    model="my-model",
    messages=[{"role": "user", "content": "Hello"}]
)
```

### 4. Function Calling

```python
tools = [
    {
        "type": "function",
        "function": {
            "name": "search_database",
            "description": "Search the product database",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "limit": {"type": "integer"}
                },
                "required": ["query"]
            }
        }
    }
]

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Find laptops under $1000"}],
    tools=tools
)

if response.choices[0].message.tool_calls:
    # Model wants to call a function
    tool_call = response.choices[0].message.tool_calls[0]
    print(f"Function: {tool_call.function.name}")
    print(f"Arguments: {tool_call.function.arguments}")
```

---

## Testing Different Models

```python
models = [
    "gpt-4o",
    "gpt-3.5-turbo",
    "anthropic/claude-sonnet-4",
    "gemini/gemini-1.5-flash"
]

for model in models:
    try:
        response = completion(
            model=model,
            messages=[{"role": "user", "content": "Say hi!"}],
            max_tokens=20
        )
        print(f"✅ {model}: {response.choices[0].message.content}")
    except Exception as e:
        print(f"❌ {model}: {str(e)[:50]}")
```

---

## Monitoring & Debugging

### View Logs

```bash
# Check proxy logs
tail -f /tmp/claude-1000/-teamspace-studios-this-studio-shinway/tasks/*.output

# Or if running in foreground, logs appear in terminal
```

### Check Metrics

```bash
# Prometheus metrics
curl http://localhost:4000/metrics

# Health check
curl http://localhost:4000/health/readiness \
  -H "Authorization: Bearer sk-1234"
```

### View Spend

```bash
# Get spend logs
curl http://localhost:4000/spend/logs \
  -H "Authorization: Bearer sk-1234"
```

---

## Troubleshooting

### "Authentication Error"
- Check your API key in .env
- Restart the proxy after adding keys
- Verify key format (OpenAI: sk-..., Anthropic: sk-ant-...)

### "Model not found"
- Check available models: `curl http://localhost:4000/v1/models -H "Authorization: Bearer sk-1234"`
- Verify model name matches config in proxy_server_config.yaml

### "Rate limit exceeded"
- Add multiple API keys for load balancing
- Configure rate limits in proxy_server_config.yaml
- Use Router with multiple deployments

### Proxy won't start
- Check if port 4000 is in use: `netstat -tlnp | grep 4000`
- Verify database is running: `docker ps | grep litellm_db`
- Check logs for errors

---

## Next Steps

### 1. Production Setup
- [ ] Add all your API keys
- [ ] Configure rate limits
- [ ] Set up Redis for caching
- [ ] Enable Prometheus monitoring
- [ ] Configure logging (Langfuse, Datadog, etc.)

### 2. Security
- [ ] Change master key from sk-1234
- [ ] Create virtual keys for different users/teams
- [ ] Set budget limits per key
- [ ] Enable request logging

### 3. Optimization
- [ ] Enable caching for repeated queries
- [ ] Set up load balancing across providers
- [ ] Configure fallback strategies
- [ ] Optimize timeout settings

### 4. Development
- [ ] Read ARCHITECTURE_GUIDE.md
- [ ] Explore provider implementations in litellm/llms/
- [ ] Run tests: `make test-unit`
- [ ] Add custom callbacks or integrations

---

## Useful Commands Reference

```bash
# Start proxy
poetry run litellm --config proxy_server_config.yaml --port 4000

# Run tests
make test-unit

# Format code
make format

# Check code quality
make lint

# View database
poetry run prisma studio

# Generate Prisma client
poetry run prisma generate

# Test setup
poetry run python test_litellm.py

# Run demos
poetry run python demo_proxy.py
poetry run python interactive_demo.py
poetry run python advanced_workflows.py
```

---

## Resources

- **Local Docs**: DEV_GUIDE.md, ARCHITECTURE_GUIDE.md, RUNNING.md
- **Official Docs**: https://docs.litellm.ai
- **API Reference**: https://docs.litellm.ai/docs/api-reference
- **Providers**: https://docs.litellm.ai/docs/providers
- **GitHub**: https://github.com/BerriAI/litellm
- **Discord**: https://discord.gg/wuPM9dRgDw

---

## Quick Test Script

Save this as `quick_test.py`:

```python
#!/usr/bin/env python3
import openai
import sys

client = openai.OpenAI(
    api_key="sk-1234",
    base_url="http://localhost:4000"
)

try:
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": "Say 'LiteLLM is working!'"}],
        max_tokens=20
    )
    print("✅ Success!")
    print(f"Response: {response.choices[0].message.content}")
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)
```

Run it:
```bash
poetry run python quick_test.py
```

---

**You're all set! 🎉**

Start by adding your API key and running `quick_test.py` to verify everything works.
