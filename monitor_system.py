#!/usr/bin/env python3
"""
Monitoring Your LiteLLM System
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:4000"
MASTER_KEY = "sk-1234"

print("📊 LiteLLM System Monitoring")
print("=" * 70)
print()

# 1. View all virtual keys
print("1️⃣  All Virtual Keys")
print("-" * 70)

response = requests.get(
    f"{BASE_URL}/key/info",
    headers={"Authorization": f"Bearer {MASTER_KEY}"}
)

if response.status_code == 200:
    keys_data = response.json()
    keys = keys_data.get('data', [])
    
    print(f"Total keys: {len(keys)}")
    print()
    print(f"{'User/Team':<30} {'Budget':<15} {'Models':<20} {'Key':<30}")
    print("-" * 95)
    
    for key in keys[:10]:  # Show first 10
        metadata = key.get('metadata', {})
        user = metadata.get('user', 'N/A')
        team = metadata.get('team', 'N/A')
        budget = key.get('max_budget', 0)
        models = key.get('models', [])
        key_str = key.get('key', 'N/A')
        
        user_team = f"{user} ({team})"
        models_str = ', '.join(models[:2]) if models else 'All'
        
        print(f"{user_team:<30} ${budget:<14.2f} {models_str:<20} {key_str[:25]}...")
else:
    print(f"Status: {response.status_code}")

print()

# 2. View teams
print("2️⃣  All Teams")
print("-" * 70)

response = requests.get(
    f"{BASE_URL}/team/list",
    headers={"Authorization": f"Bearer {MASTER_KEY}"}
)

if response.status_code == 200:
    teams = response.json()
    print(f"Total teams: {len(teams)}")
    print()
    for team in teams[:5]:
        print(f"  • {team.get('team_alias', 'N/A')}")
        print(f"    Budget: ${team.get('max_budget', 0)}")
        print(f"    Models: {len(team.get('models', []))} configured")
        print()
else:
    print(f"Status: {response.status_code}")

# 3. System health
print("3️⃣  System Health")
print("-" * 70)

response = requests.get(
    f"{BASE_URL}/health/readiness",
    headers={"Authorization": f"Bearer {MASTER_KEY}"}
)

if response.status_code == 200:
    health = response.json()
    print(f"  Status: {health['status']}")
    print(f"  Database: {health['db']}")
    print(f"  Version: {health['litellm_version']}")
    print(f"  Active callbacks: {len(health['success_callbacks'])}")
    print()

# 4. Available models
print("4️⃣  Available Models")
print("-" * 70)

response = requests.get(
    f"{BASE_URL}/v1/models",
    headers={"Authorization": f"Bearer {MASTER_KEY}"}
)

if response.status_code == 200:
    models = response.json()
    total = len(models['data'])
    
    # Group by provider
    providers = {}
    for model in models['data']:
        model_id = model['id']
        if '/' in model_id:
            provider = model_id.split('/')[0]
        else:
            provider = 'openai'
        providers[provider] = providers.get(provider, 0) + 1
    
    print(f"Total models: {total}")
    print()
    print("Top providers:")
    for provider, count in sorted(providers.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"  {provider:20} {count:3} models")

print()

# 5. Spend logs
print("5️⃣  Recent Activity")
print("-" * 70)

response = requests.get(
    f"{BASE_URL}/spend/logs",
    headers={"Authorization": f"Bearer {MASTER_KEY}"},
    params={"limit": 10}
)

if response.status_code == 200:
    logs = response.json()
    if logs:
        print(f"Recent API calls: {len(logs)}")
        print()
        for log in logs[:5]:
            print(f"  • Model: {log.get('model', 'N/A')}")
            print(f"    Cost: ${log.get('spend', 0):.4f}")
            print(f"    Tokens: {log.get('total_tokens', 0)}")
            print()
    else:
        print("No activity yet (add API keys and make calls)")
else:
    print(f"Status: {response.status_code}")

# 6. Prometheus metrics
print("6️⃣  Prometheus Metrics")
print("-" * 70)

response = requests.get(f"{BASE_URL}/metrics")

if response.status_code == 200:
    metrics = response.text
    
    # Extract LiteLLM-specific metrics
    litellm_metrics = [line for line in metrics.split('\n') 
                       if line.startswith('litellm_') and not line.startswith('#')]
    
    if litellm_metrics:
        print("Sample metrics:")
        for metric in litellm_metrics[:5]:
            print(f"  {metric}")
    else:
        print("No LiteLLM metrics yet (make some API calls)")

print()

# 7. Management actions
print("7️⃣  Management Actions")
print("-" * 70)
print("What you can do:")
print()
print("View database:")
print("  $ poetry run prisma studio")
print("  Opens at: http://localhost:5555")
print()
print("Update a key's budget:")
print(f"  $ curl -X POST {BASE_URL}/key/update \\")
print(f"    -H 'Authorization: Bearer {MASTER_KEY}' \\")
print(f"    -d '{{'key': 'sk-...', 'max_budget': 1000}}'")
print()
print("Delete a key:")
print(f"  $ curl -X POST {BASE_URL}/key/delete \\")
print(f"    -H 'Authorization: Bearer {MASTER_KEY}' \\")
print(f"    -d '{{'keys': ['sk-...']}}'")
print()
print("View spend by user:")
print(f"  $ curl {BASE_URL}/spend/logs?api_key=sk-... \\")
print(f"    -H 'Authorization: Bearer {MASTER_KEY}'")
print()

# Summary
print("=" * 70)
print("🎯 Next Steps")
print("=" * 70)
print()
print("1. View in Database:")
print("   $ poetry run prisma studio")
print()
print("2. Monitor in Real-Time:")
print("   Open: http://localhost:4000/")
print("   Check: http://localhost:4000/metrics")
print()
print("3. Make Test Calls:")
print("   Add API keys to .env and restart proxy")
print("   Use the keys created above")
print()
print("4. Set Up Alerts:")
print("   Configure Prometheus alerts for:")
print("   • Budget thresholds")
print("   • Error rates")
print("   • Response times")
print()
print("5. Production Checklist:")
print("   ✓ Change master key from sk-1234")
print("   ✓ Set up SSL/TLS")
print("   ✓ Configure Redis for caching")
print("   ✓ Enable logging (Langfuse, Datadog)")
print("   ✓ Set up backup for database")
print()

