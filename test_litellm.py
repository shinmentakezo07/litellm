#!/usr/bin/env python3
"""
Test script for LiteLLM proxy running locally
"""

import os
from litellm import completion

# Test 1: Direct SDK usage (no proxy)
print("=" * 60)
print("Test 1: Using LiteLLM SDK directly")
print("=" * 60)

# Uncomment and add your API key to test
# os.environ["OPENAI_API_KEY"] = "your-key-here"

# Example: Direct completion call
# response = completion(
#     model="gpt-4o",
#     messages=[{"role": "user", "content": "Say 'Hello from LiteLLM!'"}]
# )
# print(response.choices[0].message.content)

print("Note: Add your OPENAI_API_KEY to .env to test direct SDK calls\n")

# Test 2: Using OpenAI SDK with LiteLLM Proxy
print("=" * 60)
print("Test 2: Using OpenAI SDK with LiteLLM Proxy")
print("=" * 60)

try:
    import openai

    client = openai.OpenAI(
        api_key="sk-1234",  # LiteLLM master key
        base_url="http://localhost:4000"
    )

    # List available models
    print("\nAvailable models:")
    models = client.models.list()
    for model in models.data[:5]:  # Show first 5 models
        print(f"  - {model.id}")

    print(f"\nTotal models available: {len(models.data)}")

    # Uncomment to test completion (requires valid API key in .env)
    # response = client.chat.completions.create(
    #     model="gpt-4o",
    #     messages=[{"role": "user", "content": "Hello!"}]
    # )
    # print(f"\nResponse: {response.choices[0].message.content}")

except Exception as e:
    print(f"Error: {e}")

# Test 3: Using requests library
print("\n" + "=" * 60)
print("Test 3: Using requests library (raw HTTP)")
print("=" * 60)

try:
    import requests

    # Health check
    response = requests.get(
        "http://localhost:4000/health/readiness",
        headers={"Authorization": "Bearer sk-1234"}
    )
    print(f"\nHealth check: {response.json()}")

    # Uncomment to test completion
    # response = requests.post(
    #     "http://localhost:4000/v1/chat/completions",
    #     headers={
    #         "Authorization": "Bearer sk-1234",
    #         "Content-Type": "application/json"
    #     },
    #     json={
    #         "model": "gpt-4o",
    #         "messages": [{"role": "user", "content": "Hello!"}]
    #     }
    # )
    # print(f"\nResponse: {response.json()}")

except Exception as e:
    print(f"Error: {e}")

print("\n" + "=" * 60)
print("Setup complete! LiteLLM is running on http://localhost:4000")
print("=" * 60)
print("\nTo make actual API calls:")
print("1. Add your API keys to .env file")
print("2. Uncomment the test code above")
print("3. Run: poetry run python test_litellm.py")
