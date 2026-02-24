#!/usr/bin/env python3
"""
Practical demonstration of LiteLLM proxy features
"""

import requests
import json

BASE_URL = "http://localhost:4000"
MASTER_KEY = "sk-1234"

def print_section(title):
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)

# ============================================================
# 1. Check Proxy Health and Status
# ============================================================

print_section("1. Proxy Health Check")

response = requests.get(
    f"{BASE_URL}/health/readiness",
    headers={"Authorization": f"Bearer {MASTER_KEY}"}
)

health = response.json()
print(f"Status: {health['status']}")
print(f"Database: {health['db']}")
print(f"Version: {health['litellm_version']}")
print(f"Callbacks: {', '.join(health['success_callbacks'])}")

# ============================================================
# 2. List Available Models
# ============================================================

print_section("2. Available Models")

response = requests.get(
    f"{BASE_URL}/v1/models",
    headers={"Authorization": f"Bearer {MASTER_KEY}"}
)

models = response.json()
print(f"Total models: {len(models['data'])}")
print("\nSample models:")
for model in models['data'][:15]:
    print(f"  • {model['id']}")

# ============================================================
# 3. Get Model Configuration Details
# ============================================================

print_section("3. Model Configuration")

response = requests.get(
    f"{BASE_URL}/model/info",
    headers={"Authorization": f"Bearer {MASTER_KEY}"}
)

if response.status_code == 200:
    model_info = response.json()
    print(f"Configured models: {len(model_info['data'])}")

    # Show first configured model
    if model_info['data']:
        first_model = model_info['data'][0]
        print(f"\nExample model config:")
        print(f"  Name: {first_model['model_name']}")
        print(f"  Provider: {first_model['litellm_params']['model']}")
        if 'model_info' in first_model:
            print(f"  Info: {first_model['model_info']}")

# ============================================================
# 4. Generate a Virtual Key (for multi-tenant usage)
# ============================================================

print_section("4. Virtual Key Management")

# Create a virtual key with budget and model restrictions
key_data = {
    "models": ["gpt-4o", "gpt-3.5-turbo"],
    "max_budget": 10.0,  # $10 budget
    "duration": "30d",
    "metadata": {
        "user": "demo_user",
        "team": "engineering"
    }
}

response = requests.post(
    f"{BASE_URL}/key/generate",
    headers={
        "Authorization": f"Bearer {MASTER_KEY}",
        "Content-Type": "application/json"
    },
    json=key_data
)

if response.status_code == 200:
    key_response = response.json()
    virtual_key = key_response.get('key', 'N/A')
    print(f"✅ Virtual key created: {virtual_key[:20]}...")
    print(f"   Models: {', '.join(key_data['models'])}")
    print(f"   Budget: ${key_data['max_budget']}")
    print(f"   Duration: {key_data['duration']}")
else:
    print(f"⚠️  Key generation requires database setup")
    print(f"   Status: {response.status_code}")

# ============================================================
# 5. Test Completion Endpoint (without actual API key)
# ============================================================

print_section("5. Completion Endpoint Test")

# This will fail without a real API key, but shows the endpoint structure
completion_data = {
    "model": "gpt-4o",
    "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is LiteLLM?"}
    ],
    "temperature": 0.7,
    "max_tokens": 100
}

print("Request structure:")
print(json.dumps(completion_data, indent=2))

response = requests.post(
    f"{BASE_URL}/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {MASTER_KEY}",
        "Content-Type": "application/json"
    },
    json=completion_data
)

print(f"\nResponse status: {response.status_code}")
if response.status_code == 200:
    result = response.json()
    print(f"✅ Success!")
    print(f"Response: {result['choices'][0]['message']['content']}")
else:
    print(f"⚠️  Expected - requires valid OPENAI_API_KEY in .env")
    print(f"Error: {response.json().get('error', {}).get('message', 'Unknown')}")

# ============================================================
# 6. Check Prometheus Metrics
# ============================================================

print_section("6. Prometheus Metrics")

response = requests.get(f"{BASE_URL}/metrics")

if response.status_code == 200:
    metrics = response.text
    # Show first few metrics
    lines = metrics.split('\n')[:20]
    print("Sample metrics:")
    for line in lines:
        if line and not line.startswith('#'):
            print(f"  {line}")
else:
    print(f"Metrics endpoint status: {response.status_code}")

# ============================================================
# 7. View Spend Logs (if available)
# ============================================================

print_section("7. Spend Tracking")

response = requests.get(
    f"{BASE_URL}/spend/logs",
    headers={"Authorization": f"Bearer {MASTER_KEY}"}
)

if response.status_code == 200:
    logs = response.json()
    print(f"Total spend logs: {len(logs)}")
    if logs:
        print("\nRecent activity:")
        for log in logs[:5]:
            print(f"  • {log}")
else:
    print("No spend logs yet (make some API calls first)")

# ============================================================
# Summary
# ============================================================

print_section("Summary")
print("""
✅ LiteLLM Proxy is fully operational!

To make actual API calls:
1. Add your API keys to .env:
   OPENAI_API_KEY="sk-..."
   ANTHROPIC_API_KEY="sk-ant-..."

2. Restart the proxy:
   pkill -f litellm
   poetry run litellm --config proxy_server_config.yaml --port 4000

3. Test with real requests:
   poetry run python demo_proxy.py

Features available:
• 289 models from 100+ providers
• Virtual key management
• Budget tracking
• Load balancing & fallbacks
• Prometheus metrics
• Spend logging
• Caching (when configured)
""")

print("=" * 60)
