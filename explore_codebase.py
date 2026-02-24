#!/usr/bin/env python3
"""
Exploring the LiteLLM Codebase - Understanding How It Works
"""

import os
import subprocess

print("🔍 LiteLLM Codebase Deep Dive")
print("=" * 70)
print()

# 1. Show provider structure
print("1️⃣  Provider Implementations")
print("-" * 70)

providers_dir = "litellm/llms"
providers = [d for d in os.listdir(providers_dir) 
             if os.path.isdir(os.path.join(providers_dir, d)) 
             and not d.startswith('_')]

print(f"Total providers: {len(providers)}")
print("\nSample providers:")
for provider in sorted(providers)[:15]:
    provider_path = os.path.join(providers_dir, provider)
    files = os.listdir(provider_path)
    has_chat = any('chat' in f or 'completion' in f for f in files)
    has_embed = any('embed' in f for f in files)
    
    features = []
    if has_chat:
        features.append("chat")
    if has_embed:
        features.append("embed")
    
    print(f"   {provider:20} {', '.join(features) if features else 'base'}")

# 2. Show main entry points
print("\n2️⃣  Main Entry Points")
print("-" * 70)

entry_points = [
    ("litellm/main.py", "Core completion() function"),
    ("litellm/router.py", "Load balancing & routing"),
    ("litellm/proxy/proxy_server.py", "FastAPI proxy server"),
    ("litellm/proxy/proxy_cli.py", "CLI entry point"),
    ("litellm/utils.py", "Core utilities"),
]

for file_path, description in entry_points:
    if os.path.exists(file_path):
        lines = len(open(file_path).readlines())
        print(f"   {file_path:35} {lines:5} lines | {description}")

# 3. Show integration points
print("\n3️⃣  Integration Points")
print("-" * 70)

integrations_dir = "litellm/integrations"
if os.path.exists(integrations_dir):
    integrations = [f.replace('.py', '') for f in os.listdir(integrations_dir) 
                   if f.endswith('.py') and not f.startswith('_')]
    
    print(f"Available integrations: {len(integrations)}")
    for integration in sorted(integrations)[:10]:
        print(f"   • {integration}")

# 4. Show test structure
print("\n4️⃣  Test Structure")
print("-" * 70)

test_dirs = [
    ("tests/test_litellm", "Unit tests"),
    ("tests/llm_translation", "Provider integration tests"),
    ("tests/proxy_unit_tests", "Proxy tests"),
    ("tests/load_tests", "Performance tests"),
]

for test_dir, description in test_dirs:
    if os.path.exists(test_dir):
        test_files = [f for f in os.listdir(test_dir) if f.startswith('test_')]
        print(f"   {test_dir:30} {len(test_files):3} files | {description}")

# 5. Show how to add a custom provider
print("\n5️⃣  How to Add a Custom Provider")
print("-" * 70)

print("""
Step 1: Create provider directory
   $ mkdir -p litellm/llms/my_provider/chat

Step 2: Create completion.py
   $ cat > litellm/llms/my_provider/chat/completion.py << 'PYTHON'
   from litellm.llms.base_llm.chat.transformation import BaseLLMException
   
   class MyProviderConfig(BaseLLMException):
       def transform_request(self, messages, optional_params):
           # Convert OpenAI format to your provider's format
           return {
               "prompt": messages[-1]["content"],
               "max_tokens": optional_params.get("max_tokens", 100)
           }
       
       def transform_response(self, response):
           # Convert provider's format to OpenAI format
           return {
               "choices": [{
                   "message": {
                       "role": "assistant",
                       "content": response["text"]
                   }
               }]
           }
   PYTHON

Step 3: Register in litellm/llms/__init__.py
   Add your provider to the PROVIDER_MAP

Step 4: Add tests
   $ cat > tests/llm_translation/test_my_provider.py
""")

# 6. Show how to add custom logging
print("\n6️⃣  How to Add Custom Logging")
print("-" * 70)

print("""
Create a custom logger:

   from litellm.integrations.custom_logger import CustomLogger
   import litellm
   
   class MyLogger(CustomLogger):
       def log_pre_api_call(self, model, messages, kwargs):
           print(f"Calling {model}")
       
       def log_post_api_call(self, kwargs, response_obj, start_time, end_time):
           duration = end_time - start_time
           print(f"Completed in {duration:.2f}s")
       
       def log_failure_event(self, kwargs, response_obj, start_time, end_time):
           print(f"Failed: {response_obj}")
   
   # Register it
   litellm.callbacks = [MyLogger()]
   
   # Now all calls will be logged
   response = litellm.completion(
       model="gpt-4o",
       messages=[{"role": "user", "content": "Hello"}]
   )
""")

# 7. Show configuration options
print("\n7️⃣  Configuration Options")
print("-" * 70)

print("""
proxy_server_config.yaml structure:

model_list:              # Define available models
  - model_name: gpt-4
    litellm_params:
      model: gpt-4o
      api_key: os.environ/OPENAI_API_KEY
      rpm: 100           # Rate limit
      timeout: 60        # Request timeout

litellm_settings:        # Global settings
  drop_params: true      # Drop unsupported params
  success_callback:      # Logging integrations
    - prometheus
    - langfuse
  cache: true           # Enable caching
  num_retries: 3        # Retry failed requests

router_settings:         # Router configuration
  routing_strategy: usage-based-routing-v2
  enable_pre_call_checks: true

general_settings:        # Proxy settings
  master_key: sk-1234
  database_url: postgresql://...
  store_model_in_db: true
""")

# 8. Show useful development commands
print("\n8️⃣  Development Commands")
print("-" * 70)

commands = [
    ("make test-unit", "Run unit tests"),
    ("make test-integration", "Run integration tests"),
    ("make lint", "Check code quality"),
    ("make format", "Format code with Black"),
    ("poetry run pytest tests/test_litellm/test_completion.py -v", "Run specific test"),
    ("poetry run pytest tests/ -k 'openai' -v", "Run tests matching pattern"),
    ("poetry run prisma generate", "Regenerate Prisma client"),
    ("poetry run prisma studio", "Open database GUI"),
]

for cmd, description in commands:
    print(f"   {description}")
    print(f"   $ {cmd}")
    print()

# Summary
print("=" * 70)
print("🎓 Learning Path")
print("=" * 70)
print()
print("Beginner:")
print("  1. Read litellm/main.py - understand the completion() function")
print("  2. Look at litellm/llms/openai/ - see a simple provider")
print("  3. Run tests: make test-unit")
print()
print("Intermediate:")
print("  4. Read litellm/router.py - understand load balancing")
print("  5. Explore litellm/proxy/proxy_server.py - FastAPI endpoints")
print("  6. Add a custom callback in litellm/integrations/")
print()
print("Advanced:")
print("  7. Implement a new provider in litellm/llms/")
print("  8. Add custom routing strategy in litellm/router_strategy/")
print("  9. Contribute to the project on GitHub")
print()
print("📚 Documentation:")
print("   • ARCHITECTURE_GUIDE.md - Detailed codebase walkthrough")
print("   • DEV_GUIDE.md - Development workflows")
print("   • CONTRIBUTING.md - Contribution guidelines")
print()

