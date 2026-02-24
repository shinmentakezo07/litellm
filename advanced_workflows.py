#!/usr/bin/env python3
"""
Advanced LiteLLM Features & Workflows

This demonstrates real-world usage patterns once you add your API keys.
"""

import asyncio
import time
from typing import List, Dict
import os

# Uncomment these when you add your API keys to .env
# from litellm import completion, acompletion, Router
# import litellm

print("🚀 Advanced LiteLLM Workflows")
print("=" * 70)
print()

# ============================================================
# Workflow 1: Multi-Provider Fallback Strategy
# ============================================================

def workflow_1_fallback_strategy():
    """
    Use multiple providers with automatic fallbacks.
    If OpenAI fails, automatically try Anthropic, then Google.
    """
    print("1️⃣  Multi-Provider Fallback Strategy")
    print("-" * 70)
    print()

    print("Configuration:")
    print("""
    from litellm import Router

    router = Router(
        model_list=[
            # Primary: OpenAI
            {
                "model_name": "gpt-4",
                "litellm_params": {
                    "model": "gpt-4o",
                    "api_key": os.environ["OPENAI_API_KEY"]
                }
            },
            # Fallback 1: Anthropic
            {
                "model_name": "claude",
                "litellm_params": {
                    "model": "anthropic/claude-sonnet-4",
                    "api_key": os.environ["ANTHROPIC_API_KEY"]
                }
            },
            # Fallback 2: Google
            {
                "model_name": "gemini",
                "litellm_params": {
                    "model": "gemini/gemini-1.5-flash",
                    "api_key": os.environ["GOOGLE_API_KEY"]
                }
            }
        ],
        fallbacks=[
            {"gpt-4": ["claude", "gemini"]}  # If GPT-4 fails, try Claude, then Gemini
        ],
        num_retries=3,
        timeout=30
    )

    # Make a call - will automatically fallback if primary fails
    response = router.completion(
        model="gpt-4",
        messages=[{"role": "user", "content": "Explain quantum computing"}]
    )
    """)
    print()
    print("✅ Benefits:")
    print("   • Automatic failover if provider is down")
    print("   • No code changes needed when switching providers")
    print("   • Improved reliability and uptime")
    print()


# ============================================================
# Workflow 2: Load Balancing Across Multiple Deployments
# ============================================================

def workflow_2_load_balancing():
    """
    Distribute load across multiple API keys or deployments.
    """
    print("2️⃣  Load Balancing Across Deployments")
    print("-" * 70)
    print()

    print("Configuration:")
    print("""
    router = Router(
        model_list=[
            # Deployment 1: OpenAI US
            {
                "model_name": "gpt-4",
                "litellm_params": {
                    "model": "gpt-4o",
                    "api_key": os.environ["OPENAI_API_KEY_1"]
                }
            },
            # Deployment 2: OpenAI EU
            {
                "model_name": "gpt-4",
                "litellm_params": {
                    "model": "gpt-4o",
                    "api_key": os.environ["OPENAI_API_KEY_2"]
                }
            },
            # Deployment 3: Azure OpenAI
            {
                "model_name": "gpt-4",
                "litellm_params": {
                    "model": "azure/gpt-4",
                    "api_key": os.environ["AZURE_API_KEY"],
                    "api_base": os.environ["AZURE_API_BASE"]
                }
            }
        ],
        routing_strategy="simple-shuffle",  # Randomly distribute
        # Other strategies: "least-busy", "usage-based-routing"
    )

    # All calls to "gpt-4" will be distributed across the 3 deployments
    for i in range(10):
        response = router.completion(
            model="gpt-4",
            messages=[{"role": "user", "content": f"Request {i}"}]
        )
    """)
    print()
    print("✅ Benefits:")
    print("   • Distribute load to avoid rate limits")
    print("   • Geographic redundancy")
    print("   • Cost optimization across providers")
    print()


# ============================================================
# Workflow 3: Streaming Responses
# ============================================================

def workflow_3_streaming():
    """
    Stream responses for better UX in chat applications.
    """
    print("3️⃣  Streaming Responses")
    print("-" * 70)
    print()

    print("Implementation:")
    print("""
    from litellm import completion

    response = completion(
        model="gpt-4o",
        messages=[{"role": "user", "content": "Write a story about AI"}],
        stream=True  # Enable streaming
    )

    # Stream tokens as they arrive
    for chunk in response:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)
    """)
    print()
    print("✅ Use Cases:")
    print("   • Chat interfaces (like ChatGPT)")
    print("   • Real-time content generation")
    print("   • Better perceived performance")
    print()


# ============================================================
# Workflow 4: Function Calling / Tool Use
# ============================================================

def workflow_4_function_calling():
    """
    Use function calling for structured outputs and tool integration.
    """
    print("4️⃣  Function Calling / Tool Use")
    print("-" * 70)
    print()

    print("Implementation:")
    print("""
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": "Get current weather for a location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "City name"
                        },
                        "unit": {
                            "type": "string",
                            "enum": ["celsius", "fahrenheit"]
                        }
                    },
                    "required": ["location"]
                }
            }
        }
    ]

    response = completion(
        model="gpt-4o",
        messages=[{"role": "user", "content": "What's the weather in Tokyo?"}],
        tools=tools,
        tool_choice="auto"
    )

    # Check if model wants to call a function
    if response.choices[0].message.tool_calls:
        tool_call = response.choices[0].message.tool_calls[0]
        function_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)

        # Execute the function
        if function_name == "get_weather":
            weather_data = get_weather(**arguments)

            # Send result back to model
            response = completion(
                model="gpt-4o",
                messages=[
                    {"role": "user", "content": "What's the weather in Tokyo?"},
                    response.choices[0].message,
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": json.dumps(weather_data)
                    }
                ],
                tools=tools
            )
    """)
    print()
    print("✅ Use Cases:")
    print("   • Database queries")
    print("   • API integrations")
    print("   • Structured data extraction")
    print()


# ============================================================
# Workflow 5: Async Batch Processing
# ============================================================

def workflow_5_async_batch():
    """
    Process multiple requests concurrently for better throughput.
    """
    print("5️⃣  Async Batch Processing")
    print("-" * 70)
    print()

    print("Implementation:")
    print("""
    import asyncio
    from litellm import acompletion

    async def process_batch(prompts: List[str]):
        tasks = []

        for prompt in prompts:
            task = acompletion(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}]
            )
            tasks.append(task)

        # Process all requests concurrently
        responses = await asyncio.gather(*tasks)
        return responses

    # Process 100 requests concurrently
    prompts = [f"Summarize topic {i}" for i in range(100)]
    responses = asyncio.run(process_batch(prompts))
    """)
    print()
    print("✅ Benefits:")
    print("   • 10-100x faster than sequential processing")
    print("   • Efficient use of API rate limits")
    print("   • Better resource utilization")
    print()


# ============================================================
# Workflow 6: Custom Logging & Observability
# ============================================================

def workflow_6_custom_logging():
    """
    Add custom logging for debugging and monitoring.
    """
    print("6️⃣  Custom Logging & Observability")
    print("-" * 70)
    print()

    print("Implementation:")
    print("""
    from litellm.integrations.custom_logger import CustomLogger
    import litellm

    class MyLogger(CustomLogger):
        def log_pre_api_call(self, model, messages, kwargs):
            print(f"[PRE] Calling {model}")
            print(f"[PRE] Messages: {len(messages)}")

        def log_post_api_call(self, kwargs, response_obj, start_time, end_time):
            duration = end_time - start_time
            tokens = response_obj.usage.total_tokens
            print(f"[POST] Duration: {duration:.2f}s")
            print(f"[POST] Tokens: {tokens}")

        def log_failure_event(self, kwargs, response_obj, start_time, end_time):
            print(f"[ERROR] Request failed: {response_obj}")

    # Register the logger
    litellm.callbacks = [MyLogger()]

    # Now all completion calls will be logged
    response = completion(
        model="gpt-4o",
        messages=[{"role": "user", "content": "Hello"}]
    )
    """)
    print()
    print("✅ Integrations Available:")
    print("   • Langfuse - LLM observability")
    print("   • Prometheus - Metrics")
    print("   • Datadog - APM")
    print("   • Weights & Biases - Experiment tracking")
    print()


# ============================================================
# Workflow 7: Cost Tracking & Budget Management
# ============================================================

def workflow_7_cost_tracking():
    """
    Track costs and enforce budgets per user/team.
    """
    print("7️⃣  Cost Tracking & Budget Management")
    print("-" * 70)
    print()

    print("Via Proxy Server:")
    print("""
    # Create a virtual key with budget limit
    curl -X POST http://localhost:4000/key/generate \\
      -H 'Authorization: Bearer sk-1234' \\
      -d '{
        "models": ["gpt-4o"],
        "max_budget": 100.0,
        "duration": "30d",
        "metadata": {"team": "engineering"}
      }'

    # Key will automatically stop working when budget is exceeded
    # View spend logs:
    curl http://localhost:4000/spend/logs \\
      -H 'Authorization: Bearer sk-1234'
    """)
    print()
    print("✅ Features:")
    print("   • Per-key budget limits")
    print("   • Real-time spend tracking")
    print("   • Cost breakdown by model/user/team")
    print("   • Automatic budget enforcement")
    print()


# ============================================================
# Workflow 8: Caching for Cost Reduction
# ============================================================

def workflow_8_caching():
    """
    Cache responses to reduce costs and latency.
    """
    print("8️⃣  Response Caching")
    print("-" * 70)
    print()

    print("Configuration (proxy_server_config.yaml):")
    print("""
    litellm_settings:
      cache: true
      cache_params:
        type: redis
        host: localhost
        port: 6379
        ttl: 3600  # Cache for 1 hour
    """)
    print()
    print("Usage:")
    print("""
    # First call - hits the API
    response1 = completion(
        model="gpt-4o",
        messages=[{"role": "user", "content": "What is Python?"}],
        caching=True
    )

    # Second call - returns cached response (instant, free)
    response2 = completion(
        model="gpt-4o",
        messages=[{"role": "user", "content": "What is Python?"}],
        caching=True
    )
    """)
    print()
    print("✅ Benefits:")
    print("   • 50-90% cost reduction for repeated queries")
    print("   • Instant responses for cached queries")
    print("   • Configurable TTL per request")
    print()


# ============================================================
# Main
# ============================================================

def main():
    workflow_1_fallback_strategy()
    workflow_2_load_balancing()
    workflow_3_streaming()
    workflow_4_function_calling()
    workflow_5_async_batch()
    workflow_6_custom_logging()
    workflow_7_cost_tracking()
    workflow_8_caching()

    print("=" * 70)
    print("🎓 Next Steps to Implement These Workflows")
    print("=" * 70)
    print()
    print("1. Add your API keys to .env:")
    print("   OPENAI_API_KEY='sk-...'")
    print("   ANTHROPIC_API_KEY='sk-ant-...'")
    print("   GOOGLE_API_KEY='...'")
    print()
    print("2. Restart the proxy:")
    print("   pkill -f litellm")
    print("   poetry run litellm --config proxy_server_config.yaml --port 4000")
    print()
    print("3. Try the examples:")
    print("   • Uncomment code in examples_sdk.py")
    print("   • Run: poetry run python examples_sdk.py")
    print()
    print("4. Customize for your use case:")
    print("   • Edit proxy_server_config.yaml")
    print("   • Add custom callbacks")
    print("   • Configure caching and logging")
    print()
    print("📚 Full documentation: DEV_GUIDE.md & ARCHITECTURE_GUIDE.md")
    print()


if __name__ == "__main__":
    main()
