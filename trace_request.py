#!/usr/bin/env python3
"""
Tracing a Request Through LiteLLM - Step by Step
"""

print("🔍 Tracing a Request Through LiteLLM")
print("=" * 70)
print()

print("Let's trace what happens when you call:")
print("  completion(model='gpt-4o', messages=[{'role': 'user', 'content': 'Hi'}])")
print()

# Step 1
print("STEP 1: Entry Point (litellm/main.py)")
print("-" * 70)
print("""
def completion(
    model: str,
    messages: List[Dict],
    **kwargs
) -> ModelResponse:
    
    # 1. Parse the model string
    model_parts = model.split('/')
    if len(model_parts) > 1:
        custom_llm_provider = model_parts[0]  # e.g., "openai"
        model = model_parts[1]                 # e.g., "gpt-4o"
    else:
        custom_llm_provider = None
        model = model_parts[0]
    
    # 2. Determine the provider
    if custom_llm_provider is None:
        custom_llm_provider = get_llm_provider(model)  # Returns "openai"
    
    # 3. Get optional parameters
    optional_params = get_optional_params(
        temperature=kwargs.get('temperature'),
        max_tokens=kwargs.get('max_tokens'),
        # ... other params
    )
    
    # 4. Route to provider-specific handler
    if custom_llm_provider == "openai":
        response = openai_chat_completions.completion(
            model=model,
            messages=messages,
            optional_params=optional_params,
            **kwargs
        )
    
    return response
""")

# Step 2
print("\nSTEP 2: Provider Detection (litellm/utils.py)")
print("-" * 70)
print("""
def get_llm_provider(model: str) -> str:
    '''
    Determines which provider to use based on model name
    '''
    
    # Check model name patterns
    if model.startswith("gpt-"):
        return "openai"
    elif model.startswith("claude-"):
        return "anthropic"
    elif model.startswith("gemini-"):
        return "vertex_ai"
    # ... 100+ other providers
    
    # Default to openai for unknown models
    return "openai"
""")

# Step 3
print("\nSTEP 3: OpenAI Handler (litellm/llms/openai/openai.py)")
print("-" * 70)
print("""
def completion(
    model: str,
    messages: List[Dict],
    optional_params: Dict,
    **kwargs
) -> ModelResponse:
    
    # 1. Get API configuration
    api_key = get_secret_str("OPENAI_API_KEY")
    api_base = "https://api.openai.com/v1"
    
    # 2. Transform request using OpenAIGPTConfig
    config = OpenAIGPTConfig()
    
    request_data = config.transform_request(
        messages=messages,
        model=model,
        optional_params=optional_params
    )
    
    # 3. Make HTTP request
    response = httpx.post(
        f"{api_base}/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        json=request_data,
        timeout=kwargs.get('timeout', 600)
    )
    
    # 4. Transform response
    model_response = config.transform_response(
        response=response.json(),
        model=model
    )
    
    return model_response
""")

# Step 4
print("\nSTEP 4: Request Transformation (litellm/llms/openai/chat/gpt_transformation.py)")
print("-" * 70)
print("""
class OpenAIGPTConfig(BaseConfig):
    
    def transform_request(
        self,
        messages: List[Dict],
        model: str,
        optional_params: Dict
    ) -> Dict:
        '''
        Converts LiteLLM format to OpenAI API format
        '''
        
        # Build the request
        data = {
            "model": model,
            "messages": messages
        }
        
        # Add optional parameters
        if "temperature" in optional_params:
            data["temperature"] = optional_params["temperature"]
        
        if "max_tokens" in optional_params:
            data["max_tokens"] = optional_params["max_tokens"]
        
        if "stream" in optional_params:
            data["stream"] = optional_params["stream"]
        
        # Handle function calling
        if "tools" in optional_params:
            data["tools"] = optional_params["tools"]
        
        return data
""")

# Step 5
print("\nSTEP 5: Response Transformation")
print("-" * 70)
print("""
def transform_response(
    self,
    response: Dict,
    model: str
) -> ModelResponse:
    '''
    Converts OpenAI response to LiteLLM standard format
    '''
    
    # OpenAI response structure:
    # {
    #   "id": "chatcmpl-123",
    #   "object": "chat.completion",
    #   "created": 1677652288,
    #   "model": "gpt-4o",
    #   "choices": [{
    #     "index": 0,
    #     "message": {
    #       "role": "assistant",
    #       "content": "Hello! How can I help you?"
    #     },
    #     "finish_reason": "stop"
    #   }],
    #   "usage": {
    #     "prompt_tokens": 9,
    #     "completion_tokens": 12,
    #     "total_tokens": 21
    #   }
    # }
    
    # Convert to LiteLLM ModelResponse
    return ModelResponse(
        id=response["id"],
        choices=[
            Choices(
                index=choice["index"],
                message=Message(
                    role=choice["message"]["role"],
                    content=choice["message"]["content"]
                ),
                finish_reason=choice["finish_reason"]
            )
            for choice in response["choices"]
        ],
        created=response["created"],
        model=response["model"],
        usage={
            "prompt_tokens": response["usage"]["prompt_tokens"],
            "completion_tokens": response["usage"]["completion_tokens"],
            "total_tokens": response["usage"]["total_tokens"]
        }
    )
""")

# Step 6
print("\nSTEP 6: Logging & Callbacks (litellm/_logging.py)")
print("-" * 70)
print("""
# After the response is received, LiteLLM logs it

for callback in litellm.callbacks:
    callback.log_post_api_call(
        kwargs={
            "model": model,
            "messages": messages,
            "optional_params": optional_params
        },
        response_obj=model_response,
        start_time=start_time,
        end_time=end_time
    )

# Callbacks can be:
# - PrometheusLogger (metrics)
# - LangfuseLogger (observability)
# - DatadogLogger (APM)
# - Custom loggers
""")

# Step 7
print("\nSTEP 7: Return to Caller")
print("-" * 70)
print("""
# The standardized response is returned

response = completion(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hi"}]
)

# You can now access:
print(response.choices[0].message.content)  # "Hello! How can I help you?"
print(response.usage.total_tokens)          # 21
print(response.model)                       # "gpt-4o"
""")

# Comparison with other providers
print("\n" + "=" * 70)
print("🔄 How This Differs for Other Providers")
print("=" * 70)
print()

print("Anthropic (Claude):")
print("-" * 70)
print("""
# Anthropic has different request format:
{
  "model": "claude-sonnet-4",
  "max_tokens": 1024,           # Required!
  "system": "You are helpful",  # Separate from messages
  "messages": [
    {"role": "user", "content": "Hi"}
  ]
}

# LiteLLM transformation handles:
# 1. Extracting system message from messages array
# 2. Adding required max_tokens parameter
# 3. Converting parameter names (max_tokens vs max_tokens_to_sample)
# 4. Transforming response format back to OpenAI standard
""")

print("\nGoogle Vertex AI (Gemini):")
print("-" * 70)
print("""
# Vertex AI uses different structure:
{
  "contents": [
    {
      "role": "user",
      "parts": [{"text": "Hi"}]
    }
  ],
  "generationConfig": {
    "temperature": 0.7,
    "maxOutputTokens": 100
  }
}

# LiteLLM transformation handles:
# 1. Converting messages to contents/parts format
# 2. Mapping parameter names (max_tokens -> maxOutputTokens)
# 3. Handling Google Cloud authentication
# 4. Converting response format
""")

# Summary
print("\n" + "=" * 70)
print("💡 Key Takeaways")
print("=" * 70)
print()
print("1. Single Entry Point:")
print("   All requests go through litellm.completion()")
print()
print("2. Provider Detection:")
print("   Model name determines which provider to use")
print()
print("3. Transformation Layer:")
print("   Each provider has transform_request() and transform_response()")
print()
print("4. Standardized Output:")
print("   All providers return the same ModelResponse format")
print()
print("5. Extensibility:")
print("   Add new providers by implementing transformation methods")
print()
print("📚 To explore further:")
print("   • Read: litellm/main.py (entry point)")
print("   • Read: litellm/llms/openai/chat/gpt_transformation.py")
print("   • Read: litellm/llms/anthropic/chat/transformation.py")
print("   • Compare different provider implementations")
print()

