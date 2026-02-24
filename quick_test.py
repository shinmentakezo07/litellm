#!/usr/bin/env python3
"""
Quick test to verify LiteLLM is working with your API key
"""

import openai
import sys

def test_litellm():
    print("🧪 Testing LiteLLM Setup")
    print("=" * 60)
    print()

    # Test 1: Connection
    print("1️⃣  Testing connection to proxy...")
    try:
        client = openai.OpenAI(
            api_key="sk-1234",
            base_url="http://localhost:4000"
        )
        print("   ✅ Connected to proxy")
    except Exception as e:
        print(f"   ❌ Connection failed: {e}")
        return False

    # Test 2: List models
    print("\n2️⃣  Checking available models...")
    try:
        models = client.models.list()
        print(f"   ✅ Found {len(models.data)} models")
    except Exception as e:
        print(f"   ❌ Failed to list models: {e}")
        return False

    # Test 3: Make API call
    print("\n3️⃣  Making test API call...")
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "user", "content": "Say 'LiteLLM is working!' in exactly 5 words"}
            ],
            max_tokens=20
        )

        content = response.choices[0].message.content
        print(f"   ✅ API call successful!")
        print(f"   Response: {content}")
        print(f"   Model: {response.model}")
        print(f"   Tokens: {response.usage.total_tokens}")

        return True

    except Exception as e:
        error_msg = str(e)
        print(f"   ❌ API call failed")
        print(f"   Error: {error_msg[:200]}")

        # Provide helpful hints
        if "API key" in error_msg or "authentication" in error_msg.lower():
            print("\n💡 Hint: Add your API key to .env file:")
            print("   OPENAI_API_KEY='sk-...'")
            print("   Then restart the proxy")
        elif "not found" in error_msg.lower():
            print("\n💡 Hint: Check if the model is configured in proxy_server_config.yaml")

        return False

    print()


def main():
    success = test_litellm()

    print("\n" + "=" * 60)
    if success:
        print("🎉 All tests passed! LiteLLM is working correctly.")
        print("=" * 60)
        print()
        print("Next steps:")
        print("  • Try different models")
        print("  • Enable streaming")
        print("  • Set up function calling")
        print("  • Configure caching")
        print()
        print("See GETTING_STARTED.md for examples")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        print("=" * 60)
        print()
        print("Common fixes:")
        print("  1. Add your API key to .env")
        print("  2. Restart the proxy")
        print("  3. Check proxy logs for errors")
        print()
        print("Need help? Check DEV_GUIDE.md or GETTING_STARTED.md")

    print()
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
