import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Kiro Gateway
https://github.com/BerriAI/litellm/tree/main/kiro-gateway

:::tip

**We support all models exposed by your Kiro Gateway. Set `model=kiro_gateway/<gateway-model-name>` as a prefix when sending LiteLLM requests.**

:::

## Environment Variables
```python
# API key used by LiteLLM to authenticate to Kiro Gateway
os.environ['KIRO_GATEWAY_API_KEY']

# Optional override for gateway base URL
# Defaults to http://localhost:8000/v1
os.environ['KIRO_GATEWAY_API_BASE']
```

`KIRO_GATEWAY_API_KEY` should match the `PROXY_API_KEY` configured on your `kiro-gateway` server.

## Sample Usage
```python
from litellm import completion
import os

os.environ['KIRO_GATEWAY_API_KEY'] = "your-gateway-key"
os.environ['KIRO_GATEWAY_API_BASE'] = "http://localhost:8000/v1"

response = completion(
    model="kiro_gateway/us.anthropic.claude-sonnet-4-20250514-v1:0",
    messages=[
        {
            "role": "user",
            "content": "Write a one-line haiku about gateways."
        }
    ],
    max_tokens=128,
)

print(response)
```

## Sample Usage - Streaming
```python
from litellm import completion
import os

os.environ['KIRO_GATEWAY_API_KEY'] = "your-gateway-key"
os.environ['KIRO_GATEWAY_API_BASE'] = "http://localhost:8000/v1"

response = completion(
    model="kiro_gateway/us.anthropic.claude-sonnet-4-20250514-v1:0",
    messages=[
        {
            "role": "user",
            "content": "Count from 1 to 3."
        }
    ],
    stream=True,
)

for chunk in response:
    print(chunk)
```

## Usage with LiteLLM Proxy Server

Here's how to call a Kiro Gateway model with the LiteLLM Proxy Server.

1. Modify the config.yaml

  ```yaml
  model_list:
    - model_name: kiro-sonnet
      litellm_params:
        model: kiro_gateway/us.anthropic.claude-sonnet-4-20250514-v1:0
        api_key: os.environ/KIRO_GATEWAY_API_KEY
        api_base: os.environ/KIRO_GATEWAY_API_BASE
  ```

2. Start the proxy

  ```bash
  litellm --config /path/to/config.yaml
  ```

3. Send request to LiteLLM Proxy Server

  <Tabs>

  <TabItem value="openai" label="OpenAI Python v1.0.0+">

  ```python
  import openai

  client = openai.OpenAI(
      api_key="sk-1234",
      base_url="http://0.0.0.0:4000"
  )

  response = client.chat.completions.create(
      model="kiro-sonnet",
      messages=[
          {
              "role": "user",
              "content": "What model are you?"
          }
      ],
  )

  print(response)
  ```

  </TabItem>

  <TabItem value="curl" label="curl">

  ```shell
  curl --location 'http://0.0.0.0:4000/chat/completions' \
      --header 'Authorization: Bearer sk-1234' \
      --header 'Content-Type: application/json' \
      --data '{
      "model": "kiro-sonnet",
      "messages": [
          {
          "role": "user",
          "content": "What model are you?"
          }
      ]
  }'
  ```

  </TabItem>

  </Tabs>

## Notes

- Default Kiro Gateway base URL is `http://localhost:8000/v1`.
- Kiro Gateway exposes OpenAI-compatible (`/v1/chat/completions`, `/v1/models`) and Anthropic-compatible (`/v1/messages`) endpoints.
- LiteLLM routes this provider through its OpenAI-compatible JSON provider system.
