#!/usr/bin/env python3
"""
Understanding How a Provider Works - OpenAI Example
"""

import os

print("🔬 Deep Dive: How the OpenAI Provider Works")
print("=" * 70)
print()

# 1. Provider structure
print("1️⃣  OpenAI Provider Structure")
print("-" * 70)

openai_dir = "litellm/llms/openai"
for root, dirs, files in os.walk(openai_dir):
    level = root.replace(openai_dir, '').count(os.sep)
    indent = ' ' * 2 * level
    print(f'{indent}{os.path.basename(root)}/')
    subindent = ' ' * 2 * (level + 1)
    for file in sorted(files):
        if file.endswith('.py'):
            print(f'{subindent}{file}')

# 2. Request flow
print("\n2️⃣  Request Flow for OpenAI")
print("-" * 70)

print("""
When you call: completion(model="gpt-4o", messages=[...])

Step 1: litellm/main.py:completion()
   ↓ Determines provider is "openai"
   
Step 2: litellm/llms/openai/chat/gpt_transformation.py
   ↓ OpenAIGPTConfig.transform_request()
   ↓ Converts LiteLLM format → OpenAI API format
   
Step 3: litellm/llms/openai/chat/gpt_transformation.py
   ↓ Makes HTTP request to OpenAI API
   ↓ Uses HTTPHandler or AsyncHTTPHandler
   
Step 4: litellm/llms/openai/chat/gpt_transformation.py
   ↓ OpenAIGPTConfig.transform_response()
   ↓ Converts OpenAI response → LiteLLM format
   
Step 5: litellm/_logging.py
   ↓ Logs via callbacks (Prometheus, Langfuse, etc.)
   
Step 6: Return to caller
   ↓ Standardized OpenAI-compatible response
""")

# 3. Key transformation methods
print("\n3️⃣  Key Transformation Methods")
print("-" * 70)

print("""
class OpenAIGPTConfig(BaseLLMException):
    
    def transform_request(self, messages, optional_params):
        '''
        Converts LiteLLM standard format to OpenAI API format
        
        Input:
          messages = [{"role": "user", "content": "Hello"}]
          optional_params = {"temperature": 0.7, "max_tokens": 100}
        
        Output:
          {
            "model": "gpt-4o",
            "messages": [{"role": "user", "content": "Hello"}],
            "temperature": 0.7,
            "max_tokens": 100
          }
        '''
        pass
    
    def transform_response(self, response):
        '''
        Converts OpenAI API response to LiteLLM standard format
        
        Input:
          OpenAI API response JSON
        
        Output:
          Standardized response object with:
          - choices[0].message.content
          - usage.total_tokens
          - model
          - etc.
        '''
        pass
""")

# 4. How other providers differ
print("\n4️⃣  How Other Providers Differ")
print("-" * 70)

print("""
Anthropic (litellm/llms/anthropic/):
  • Different message format (system message separate)
  • Different parameter names (max_tokens_to_sample)
  • Different response structure
  • Transformation handles these differences

Google (litellm/llms/vertex_ai/):
  • Uses Google Cloud authentication
  • Different API endpoint structure
  • Different safety settings format
  • Transformation normalizes everything

Azure (litellm/llms/azure/):
  • Same as OpenAI but different endpoint
  • Requires deployment name
  • Different authentication (API key + endpoint)
  • Minimal transformation needed
""")

# 5. Testing a provider
print("\n5️⃣  Testing the OpenAI Provider")
print("-" * 70)

print("""
Run OpenAI-specific tests:

   $ poetry run pytest tests/llm_translation/test_openai.py -v

Run a specific test:

   $ poetry run pytest tests/llm_translation/test_openai.py::test_completion -v

Run with output:

   $ poetry run pytest tests/llm_translation/test_openai.py -v -s

Mock tests (no API key needed):

   $ poetry run pytest tests/test_litellm/test_completion.py -k mock -v
""")

# 6. Adding a custom provider
print("\n6️⃣  Adding Your Own Provider")
print("-" * 70)

print("""
Let's say you want to add support for "MyLLM" API:

1. Create directory structure:
   $ mkdir -p litellm/llms/myllm/chat

2. Create transformation file:
   $ cat > litellm/llms/myllm/chat/transformation.py << 'PYTHON'
   from litellm.llms.base_llm.chat.transformation import BaseLLMException
   
   class MyLLMConfig(BaseLLMException):
       def __init__(self):
           super().__init__()
       
       def transform_request(self, messages, optional_params):
           # MyLLM expects: {"prompt": "...", "settings": {...}}
           prompt = messages[-1]["content"]
           
           return {
               "prompt": prompt,
               "settings": {
                   "temperature": optional_params.get("temperature", 0.7),
                   "max_length": optional_params.get("max_tokens", 100)
               }
           }
       
       def transform_response(self, response):
           # MyLLM returns: {"result": "...", "tokens": 50}
           return {
               "choices": [{
                   "message": {
                       "role": "assistant",
                       "content": response["result"]
                   },
                   "finish_reason": "stop"
               }],
               "usage": {
                   "total_tokens": response["tokens"]
               }
           }
   PYTHON

3. Register in litellm/llms/__init__.py:
   from .myllm.chat.transformation import MyLLMConfig
   
   PROVIDER_MAP = {
       "myllm": MyLLMConfig,
       # ... other providers
   }

4. Use it:
   from litellm import completion
   
   response = completion(
       model="myllm/my-model",
       messages=[{"role": "user", "content": "Hello"}]
   )
""")

# 7. Debugging tips
print("\n7️⃣  Debugging Tips")
print("-" * 70)

print("""
Enable debug logging:
   $ export LITELLM_LOG=DEBUG
   $ poetry run python your_script.py

Print request/response:
   import litellm
   litellm.set_verbose = True
   
   response = completion(...)  # Will print full request/response

Use custom logger:
   from litellm.integrations.custom_logger import CustomLogger
   
   class DebugLogger(CustomLogger):
       def log_pre_api_call(self, model, messages, kwargs):
           print(f"REQUEST: {kwargs}")
       
       def log_post_api_call(self, kwargs, response_obj, start_time, end_time):
           print(f"RESPONSE: {response_obj}")
   
   litellm.callbacks = [DebugLogger()]

Run tests with verbose output:
   $ poetry run pytest tests/ -v -s --log-cli-level=DEBUG
""")

# Summary
print("\n" + "=" * 70)
print("🎯 Next Steps to Master LiteLLM")
print("=" * 70)
print()
print("Hands-on Learning:")
print("  1. Read litellm/llms/openai/chat/gpt_transformation.py")
print("  2. Run: poetry run pytest tests/llm_translation/test_openai.py -v")
print("  3. Add print statements to see the flow")
print("  4. Try modifying a transformation and see what breaks")
print()
print("Build Something:")
print("  5. Create a custom logger that tracks token usage")
print("  6. Add a new provider for a local LLM")
print("  7. Implement custom routing logic")
print("  8. Build a cost optimization system")
print()
print("Contribute:")
print("  9. Fix a bug or add a feature")
print("  10. Submit a PR to the GitHub repo")
print()

