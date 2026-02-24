#!/usr/bin/env python3
"""
Practical examples you can run right now with LiteLLM
"""

import requests
import json

BASE_URL = "http://localhost:4000"
MASTER_KEY = "sk-1234"

print("🎮 Interactive LiteLLM Demo")
print("=" * 60)
print()

# Example 1: Create a virtual key for a specific user/team
print("1️⃣  Creating a Virtual Key")
print("-" * 60)

virtual_key_config = {
    "models": ["gpt-4o", "gpt-3.5-turbo", "claude-sonnet-4"],
    "max_budget": 50.0,  # $50 budget
    "duration": "30d",
    "metadata": {
        "user": "john_doe",
        "team": "engineering",
        "project": "chatbot_v2"
    },
    "aliases": {
        "my-gpt": "gpt-4o",
        "my-claude": "claude-sonnet-4"
    }
}

response = requests.post(
    f"{BASE_URL}/key/generate",
    headers={
        "Authorization": f"Bearer {MASTER_KEY}",
        "Content-Type": "application/json"
    },
    json=virtual_key_config
)

if response.status_code == 200:
    key_data = response.json()
    virtual_key = key_data.get("key", "")
    print(f"✅ Virtual key created!")
    print(f"   Key: {virtual_key[:30]}...")
    print(f"   Budget: ${virtual_key_config['max_budget']}")
    print(f"   Models: {', '.join(virtual_key_config['models'][:3])}")
    print(f"   User: {virtual_key_config['metadata']['user']}")
    print()

    # Save for later use
    with open("/tmp/virtual_key.txt", "w") as f:
        f.write(virtual_key)
else:
    print(f"❌ Failed to create key: {response.status_code}")
    print(f"   {response.text}")
    virtual_key = None

# Example 2: List all virtual keys
print("\n2️⃣  Listing All Virtual Keys")
print("-" * 60)

response = requests.get(
    f"{BASE_URL}/key/info",
    headers={"Authorization": f"Bearer {MASTER_KEY}"}
)

if response.status_code == 200:
    keys = response.json()
    print(f"Total keys: {len(keys.get('data', []))}")
    for key in keys.get('data', [])[:3]:
        print(f"   • {key.get('key', 'N/A')[:30]}... | Budget: ${key.get('max_budget', 0)}")
else:
    print(f"Status: {response.status_code}")

# Example 3: Check model availability
print("\n3️⃣  Checking Model Availability")
print("-" * 60)

models_to_check = ["gpt-4o", "claude-sonnet-4", "gemini-1.5-flash", "groq/llama-3.1-70b-versatile"]

response = requests.get(
    f"{BASE_URL}/v1/models",
    headers={"Authorization": f"Bearer {MASTER_KEY}"}
)

if response.status_code == 200:
    all_models = response.json()
    available_model_ids = [m['id'] for m in all_models['data']]

    for model in models_to_check:
        is_available = model in available_model_ids
        status = "✅" if is_available else "❌"
        print(f"   {status} {model}")

# Example 4: Get detailed model info
print("\n4️⃣  Model Configuration Details")
print("-" * 60)

response = requests.get(
    f"{BASE_URL}/model/info",
    headers={"Authorization": f"Bearer {MASTER_KEY}"}
)

if response.status_code == 200:
    model_info = response.json()
    configured_models = model_info.get('data', [])

    print(f"Configured models: {len(configured_models)}")

    # Show a few interesting ones
    for model in configured_models[:3]:
        print(f"\n   Model: {model['model_name']}")
        print(f"   Provider: {model['litellm_params']['model']}")
        if 'rpm' in model['litellm_params']:
            print(f"   Rate limit: {model['litellm_params']['rpm']} RPM")

# Example 5: Test with a mock endpoint (no API key needed)
print("\n5️⃣  Testing with Mock Endpoint")
print("-" * 60)

test_request = {
    "model": "fake-openai-endpoint",  # This is a mock endpoint in the config
    "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"}
    ],
    "max_tokens": 50
}

print("Sending test request to mock endpoint...")
response = requests.post(
    f"{BASE_URL}/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {MASTER_KEY}",
        "Content-Type": "application/json"
    },
    json=test_request,
    timeout=5
)

print(f"Response status: {response.status_code}")
if response.status_code == 200:
    result = response.json()
    print(f"✅ Mock endpoint working!")
    print(f"   Model: {result.get('model', 'N/A')}")
    print(f"   Response: {result['choices'][0]['message']['content'][:100]}...")
else:
    print(f"⚠️  Status: {response.status_code}")
    error = response.json().get('error', {})
    print(f"   Message: {error.get('message', 'Unknown error')[:100]}")

# Example 6: View Prometheus metrics
print("\n6️⃣  Prometheus Metrics Sample")
print("-" * 60)

response = requests.get(f"{BASE_URL}/metrics")

if response.status_code == 200:
    metrics = response.text.split('\n')

    # Show some interesting metrics
    print("Sample metrics:")
    for line in metrics[:15]:
        if line and not line.startswith('#'):
            print(f"   {line}")

# Example 7: Check spend logs
print("\n7️⃣  Spend Tracking")
print("-" * 60)

response = requests.get(
    f"{BASE_URL}/spend/logs",
    headers={"Authorization": f"Bearer {MASTER_KEY}"},
    params={"limit": 5}
)

if response.status_code == 200:
    logs = response.json()
    if logs:
        print(f"Recent API calls: {len(logs)}")
        for log in logs[:3]:
            print(f"   • Model: {log.get('model', 'N/A')} | Cost: ${log.get('spend', 0):.4f}")
    else:
        print("No spend logs yet (make some API calls first)")
else:
    print(f"Status: {response.status_code}")

# Summary
print("\n" + "=" * 60)
print("🎉 Demo Complete!")
print("=" * 60)
print()
print("What you can do next:")
print()
print("1. Add real API keys to .env:")
print("   OPENAI_API_KEY='sk-...'")
print("   ANTHROPIC_API_KEY='sk-ant-...'")
print()
print("2. Make real API calls:")
print("   curl -X POST http://localhost:4000/v1/chat/completions \\")
print("     -H 'Authorization: Bearer sk-1234' \\")
print("     -H 'Content-Type: application/json' \\")
print("     -d '{")
print('       "model": "gpt-4o",')
print('       "messages": [{"role": "user", "content": "Hello!"}]')
print("     }'")
print()
print("3. Use the virtual key you created:")
if virtual_key:
    print(f"   Authorization: Bearer {virtual_key[:40]}...")
print()
print("4. Explore the Swagger UI:")
print("   http://localhost:4000/")
print()
