#!/usr/bin/env python3
"""
Things you can explore RIGHT NOW (no API keys needed)
"""

import requests
import json

BASE_URL = "http://localhost:4000"
MASTER_KEY = "sk-1234"

print("🎮 Exploring LiteLLM Features (No API Keys Required)")
print("=" * 70)
print()

# 1. Create a team with budget
print("1️⃣  Creating a Team with Budget Limits")
print("-" * 70)

team_config = {
    "team_alias": "engineering_team",
    "models": ["gpt-4o", "gpt-3.5-turbo", "claude-sonnet-4"],
    "max_budget": 1000.0,
    "budget_duration": "30d",
    "metadata": {
        "department": "Engineering",
        "cost_center": "R&D"
    }
}

response = requests.post(
    f"{BASE_URL}/team/new",
    headers={
        "Authorization": f"Bearer {MASTER_KEY}",
        "Content-Type": "application/json"
    },
    json=team_config
)

if response.status_code == 200:
    team = response.json()
    print(f"✅ Team created: {team.get('team_alias', 'N/A')}")
    print(f"   Budget: ${team.get('max_budget', 0)}")
    print(f"   Models: {len(team.get('models', []))} models")
else:
    print(f"Status: {response.status_code}")

# 2. Create multiple virtual keys for different users
print("\n2️⃣  Creating Virtual Keys for Team Members")
print("-" * 70)

users = [
    {"name": "alice", "role": "senior_dev", "budget": 100},
    {"name": "bob", "role": "junior_dev", "budget": 50},
    {"name": "charlie", "role": "data_scientist", "budget": 200}
]

created_keys = []

for user in users:
    key_config = {
        "models": ["gpt-4o", "gpt-3.5-turbo"],
        "max_budget": user["budget"],
        "duration": "30d",
        "metadata": {
            "user": user["name"],
            "role": user["role"]
        }
    }
    
    response = requests.post(
        f"{BASE_URL}/key/generate",
        headers={
            "Authorization": f"Bearer {MASTER_KEY}",
            "Content-Type": "application/json"
        },
        json=key_config
    )
    
    if response.status_code == 200:
        key_data = response.json()
        key = key_data.get("key", "")
        created_keys.append({"user": user["name"], "key": key, "budget": user["budget"]})
        print(f"✅ {user['name']:10} | Budget: ${user['budget']:3} | Key: {key[:30]}...")

# 3. Check model availability by provider
print("\n3️⃣  Models Available by Provider")
print("-" * 70)

response = requests.get(
    f"{BASE_URL}/v1/models",
    headers={"Authorization": f"Bearer {MASTER_KEY}"}
)

if response.status_code == 200:
    models = response.json()
    
    # Group by provider
    providers = {}
    for model in models['data']:
        model_id = model['id']
        if '/' in model_id:
            provider = model_id.split('/')[0]
        else:
            provider = 'openai'
        
        if provider not in providers:
            providers[provider] = []
        providers[provider].append(model_id)
    
    # Show top providers
    for provider, model_list in sorted(providers.items(), key=lambda x: len(x[1]), reverse=True)[:10]:
        print(f"   {provider:20} {len(model_list):3} models")

# 4. View proxy configuration
print("\n4️⃣  Proxy Configuration")
print("-" * 70)

response = requests.get(
    f"{BASE_URL}/health/readiness",
    headers={"Authorization": f"Bearer {MASTER_KEY}"}
)

if response.status_code == 200:
    health = response.json()
    print(f"   Status: {health['status']}")
    print(f"   Database: {health['db']}")
    print(f"   Version: {health['litellm_version']}")
    print(f"   Callbacks: {len(health['success_callbacks'])} active")
    print(f"   Transport: {'aiohttp' if health['use_aiohttp_transport'] else 'httpx'}")

# 5. Simulate usage tracking
print("\n5️⃣  Usage Tracking Simulation")
print("-" * 70)

print("   When you make API calls, LiteLLM tracks:")
print("   • Cost per request")
print("   • Tokens used (prompt + completion)")
print("   • Model used")
print("   • User/team attribution")
print("   • Timestamp and duration")
print()
print("   View logs at: http://localhost:4000/spend/logs")

# 6. Show available endpoints
print("\n6️⃣  Available API Endpoints")
print("-" * 70)

endpoints = [
    ("POST", "/v1/chat/completions", "Chat completions"),
    ("POST", "/v1/completions", "Text completions"),
    ("POST", "/v1/embeddings", "Generate embeddings"),
    ("POST", "/v1/images/generations", "Generate images"),
    ("GET", "/v1/models", "List models"),
    ("POST", "/key/generate", "Create virtual key"),
    ("GET", "/key/info", "List all keys"),
    ("POST", "/team/new", "Create team"),
    ("GET", "/spend/logs", "View spending"),
    ("GET", "/health", "Health check"),
    ("GET", "/metrics", "Prometheus metrics"),
]

for method, path, description in endpoints:
    print(f"   {method:6} {path:30} {description}")

# Summary
print("\n" + "=" * 70)
print("🎯 What You Can Do Next")
print("=" * 70)
print()
print("WITHOUT API Keys (explore now):")
print("  • Create more virtual keys with different budgets")
print("  • Set up teams and user hierarchies")
print("  • Explore the Swagger UI: http://localhost:4000/")
print("  • Check Prometheus metrics: http://localhost:4000/metrics")
print("  • View the database: poetry run prisma studio")
print()
print("WITH API Keys (add to .env):")
print("  • Make real API calls to GPT-4, Claude, Gemini, etc.")
print("  • Test streaming responses")
print("  • Try function calling")
print("  • Set up caching and logging")
print("  • Load test with multiple concurrent requests")
print()
print("Development:")
print("  • Read ARCHITECTURE_GUIDE.md to understand the code")
print("  • Explore litellm/llms/ to see provider implementations")
print("  • Run tests: make test-unit")
print("  • Add a custom callback or integration")
print()

