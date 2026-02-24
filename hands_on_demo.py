#!/usr/bin/env python3
"""
Hands-on Demo - See LiteLLM in Action
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:4000"
MASTER_KEY = "sk-1234"

print("🎮 LiteLLM Hands-On Demo")
print("=" * 70)
print("Let's create a real multi-tenant setup!\n")

# Scenario: You're building a SaaS platform with 3 teams
teams = [
    {
        "name": "Startup Team",
        "budget": 500,
        "models": ["gpt-4o", "gpt-3.5-turbo"],
        "users": ["alice", "bob"]
    },
    {
        "name": "Enterprise Team", 
        "budget": 5000,
        "models": ["gpt-4o", "claude-sonnet-4", "gemini-1.5-flash"],
        "users": ["charlie", "diana", "eve"]
    },
    {
        "name": "Research Team",
        "budget": 2000,
        "models": ["gpt-4o", "claude-sonnet-4"],
        "users": ["frank"]
    }
]

print("📋 Scenario: Multi-Tenant SaaS Platform")
print("-" * 70)
print("You're building a platform with 3 teams:")
for team in teams:
    print(f"  • {team['name']}: ${team['budget']} budget, {len(team['users'])} users")
print()

# Step 1: Create teams
print("STEP 1: Creating Teams")
print("-" * 70)

created_teams = []
for team in teams:
    response = requests.post(
        f"{BASE_URL}/team/new",
        headers={
            "Authorization": f"Bearer {MASTER_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "team_alias": team["name"].lower().replace(" ", "_"),
            "models": team["models"],
            "max_budget": team["budget"],
            "budget_duration": "30d"
        }
    )
    
    if response.status_code == 200:
        team_data = response.json()
        created_teams.append(team_data)
        print(f"✅ {team['name']}: Team ID {team_data.get('team_id', 'N/A')[:8]}...")
    else:
        print(f"❌ {team['name']}: Failed")

print()

# Step 2: Create user keys
print("STEP 2: Creating User Keys")
print("-" * 70)

all_keys = []
for team in teams:
    team_name = team["name"]
    for user in team["users"]:
        response = requests.post(
            f"{BASE_URL}/key/generate",
            headers={
                "Authorization": f"Bearer {MASTER_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "models": team["models"],
                "max_budget": team["budget"] / len(team["users"]),
                "duration": "30d",
                "metadata": {
                    "user": user,
                    "team": team_name,
                    "created": datetime.now().isoformat()
                }
            }
        )
        
        if response.status_code == 200:
            key_data = response.json()
            key = key_data.get("key", "")
            all_keys.append({
                "user": user,
                "team": team_name,
                "key": key,
                "budget": team["budget"] / len(team["users"])
            })
            print(f"✅ {user:10} ({team_name:20}) | Key: {key[:25]}...")

print()

# Step 3: Show what you've built
print("STEP 3: Your Multi-Tenant Setup")
print("-" * 70)
print(f"Total teams: {len(created_teams)}")
print(f"Total users: {len(all_keys)}")
print(f"Total budget: ${sum(t['budget'] for t in teams)}")
print()

# Step 4: Show how users would use their keys
print("STEP 4: How Users Make API Calls")
print("-" * 70)

if all_keys:
    example_user = all_keys[0]
    print(f"Example: {example_user['user']} from {example_user['team']}")
    print()
    print("Python code:")
    print(f"""
import openai

client = openai.OpenAI(
    api_key="{example_user['key'][:30]}...",
    base_url="http://localhost:4000"
)

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{{"role": "user", "content": "Hello!"}}]
)
""")
    print()
    print("cURL command:")
    print(f"""
curl -X POST http://localhost:4000/v1/chat/completions \\
  -H "Authorization: Bearer {example_user['key'][:30]}..." \\
  -H "Content-Type: application/json" \\
  -d '{{"model":"gpt-4o","messages":[{{"role":"user","content":"Hello!"}}]}}'
""")

print()

# Step 5: Show monitoring capabilities
print("STEP 5: Monitoring & Analytics")
print("-" * 70)
print("Track usage per user/team:")
print(f"  • Spend logs: GET {BASE_URL}/spend/logs")
print(f"  • Metrics: GET {BASE_URL}/metrics")
print(f"  • Health: GET {BASE_URL}/health/readiness")
print()

# Step 6: Show what happens when budget is exceeded
print("STEP 6: Budget Protection")
print("-" * 70)
print("What happens when a user exceeds their budget?")
print("  ✅ API calls are automatically blocked")
print("  ✅ User receives clear error message")
print("  ✅ Admin can view spend in real-time")
print("  ✅ Budget resets after duration (30d)")
print()

# Summary
print("=" * 70)
print("🎉 Demo Complete!")
print("=" * 70)
print()
print("You've just built a production-ready multi-tenant LLM platform with:")
print(f"  ✅ {len(created_teams)} teams with separate budgets")
print(f"  ✅ {len(all_keys)} users with individual API keys")
print(f"  ✅ Budget tracking and enforcement")
print(f"  ✅ Model access control per team")
print(f"  ✅ Usage monitoring and analytics")
print()
print("Next steps:")
print("  1. Add your API keys to .env")
print("  2. Users can start making real API calls")
print("  3. Monitor usage at: http://localhost:4000/")
print("  4. View database: poetry run prisma studio")
print()
print("💡 This is just the beginning! LiteLLM can do much more:")
print("  • Load balancing across providers")
print("  • Automatic fallbacks")
print("  • Response caching")
print("  • Custom routing strategies")
print("  • Integration with Langfuse, Datadog, etc.")
print()

