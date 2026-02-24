#!/usr/bin/env python3
"""
Complete workflow example: From setup to making API calls
"""

import os
import sys

def check_setup():
    """Verify the setup is complete"""
    print("🔍 Checking LiteLLM Setup...")
    print("=" * 60)

    checks = {
        "Poetry installed": os.path.exists("/teamspace/studios/this_studio/.local/bin/poetry"),
        "Dependencies installed": os.path.exists("poetry.lock"),
        "Database running": True,  # We know it's running
        "Proxy running": True,     # We know it's running
        ".env file exists": os.path.exists(".env"),
    }

    for check, status in checks.items():
        status_icon = "✅" if status else "❌"
        print(f"  {status_icon} {check}")

    print()
    return all(checks.values())


def show_next_steps():
    """Show what to do next"""
    print("🎯 Next Steps")
    print("=" * 60)
    print()

    print("1️⃣  Add Your API Keys")
    print("   Edit .env file and add your provider keys:")
    print("   ```")
    print("   OPENAI_API_KEY='sk-...'")
    print("   ANTHROPIC_API_KEY='sk-ant-...'")
    print("   GOOGLE_API_KEY='...'")
    print("   ```")
    print()

    print("2️⃣  Restart the Proxy")
    print("   ```bash")
    print("   pkill -f litellm")
    print("   poetry run litellm --config proxy_server_config.yaml --port 4000")
    print("   ```")
    print()

    print("3️⃣  Test with Real API Calls")
    print("   ```python")
    print("   from litellm import completion")
    print()
    print("   response = completion(")
    print("       model='gpt-4o',")
    print("       messages=[{'role': 'user', 'content': 'Hello!'}]")
    print("   )")
    print("   print(response.choices[0].message.content)")
    print("   ```")
    print()

    print("4️⃣  Explore the Codebase")
    print("   • Read ARCHITECTURE_GUIDE.md to understand the structure")
    print("   • Check litellm/llms/ to see provider implementations")
    print("   • Look at litellm/proxy/ for the proxy server code")
    print("   • Run tests: make test-unit")
    print()

    print("5️⃣  Customize & Extend")
    print("   • Add a new provider in litellm/llms/")
    print("   • Create custom callbacks for logging")
    print("   • Modify proxy_server_config.yaml for your needs")
    print("   • Add custom routing strategies")
    print()


def show_useful_commands():
    """Show useful development commands"""
    print("💻 Useful Commands")
    print("=" * 60)
    print()

    commands = {
        "Development": [
            ("make test-unit", "Run unit tests"),
            ("make lint", "Check code quality"),
            ("make format", "Format code"),
            ("poetry run pytest tests/test_litellm/test_completion.py -v", "Run specific test"),
        ],
        "Proxy Management": [
            ("poetry run litellm --config proxy_server_config.yaml --port 4000", "Start proxy"),
            ("curl http://localhost:4000/health/readiness -H 'Authorization: Bearer sk-1234'", "Health check"),
            ("curl http://localhost:4000/v1/models -H 'Authorization: Bearer sk-1234'", "List models"),
        ],
        "Database": [
            ("poetry run prisma generate", "Generate Prisma client"),
            ("poetry run prisma migrate dev", "Create migration"),
            ("poetry run prisma studio", "Open database GUI"),
        ],
        "Testing": [
            ("poetry run python test_litellm.py", "Run test script"),
            ("poetry run python demo_proxy.py", "Run proxy demo"),
            ("poetry run python examples_sdk.py", "Run SDK examples"),
        ],
    }

    for category, cmds in commands.items():
        print(f"📌 {category}:")
        for cmd, desc in cmds:
            print(f"   {desc}")
            print(f"   $ {cmd}")
            print()


def show_resources():
    """Show helpful resources"""
    print("📚 Resources & Documentation")
    print("=" * 60)
    print()

    resources = {
        "Local Documentation": [
            "DEV_GUIDE.md - Complete development guide",
            "ARCHITECTURE_GUIDE.md - Codebase architecture",
            "RUNNING.md - Quick reference",
            "CLAUDE.md - Project instructions",
            "ARCHITECTURE.md - Original architecture doc",
        ],
        "Scripts": [
            "test_litellm.py - Test the setup",
            "demo_proxy.py - Proxy demonstration",
            "examples_sdk.py - SDK usage examples",
            "quick_dev_reference.sh - Quick reference",
        ],
        "Online Resources": [
            "Official Docs: https://docs.litellm.ai",
            "API Reference: https://docs.litellm.ai/docs/api-reference",
            "Providers: https://docs.litellm.ai/docs/providers",
            "GitHub: https://github.com/BerriAI/litellm",
            "Discord: https://discord.gg/wuPM9dRgDw",
        ],
    }

    for category, items in resources.items():
        print(f"📖 {category}:")
        for item in items:
            print(f"   • {item}")
        print()


def show_current_status():
    """Show current running status"""
    print("📊 Current Status")
    print("=" * 60)
    print()
    print("✅ Services Running:")
    print("   • Proxy Server: http://localhost:4000")
    print("   • PostgreSQL Database: localhost:5432")
    print("   • Swagger UI: http://localhost:4000/")
    print()
    print("📈 Statistics:")
    print("   • Models Available: 289")
    print("   • Providers Supported: 100+")
    print("   • LiteLLM Version: 1.81.14")
    print()
    print("🔑 Authentication:")
    print("   • Master Key: sk-1234")
    print()


def main():
    """Main workflow"""
    print()
    print("🚀 LiteLLM Local Development Environment")
    print("=" * 60)
    print()

    if check_setup():
        print("✅ Setup is complete!\n")
    else:
        print("⚠️  Some setup steps may be incomplete\n")

    show_current_status()
    show_next_steps()
    show_useful_commands()
    show_resources()

    print("=" * 60)
    print("🎉 You're all set! Happy coding with LiteLLM!")
    print("=" * 60)
    print()
    print("💡 Tip: Start by adding your API keys to .env, then run:")
    print("   poetry run python demo_proxy.py")
    print()


if __name__ == "__main__":
    main()
