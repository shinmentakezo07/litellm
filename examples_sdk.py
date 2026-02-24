#!/usr/bin/env python3
"""
Example: Using LiteLLM SDK for development and testing
"""

import os
from litellm import completion, embedding, image_generation
from litellm import Router

# ============================================================
# Example 1: Direct API calls (no proxy)
# ============================================================

def test_direct_completion():
    """Test direct completion without proxy"""
    # Set your API key
    os.environ["OPENAI_API_KEY"] = "your-key-here"

    response = completion(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "What is LiteLLM?"}
        ],
        temperature=0.7,
        max_tokens=100
    )

    print("Direct completion response:")
    print(response.choices[0].message.content)
    return response


def test_multiple_providers():
    """Test calling multiple providers"""
    providers = [
        "gpt-4o",                           # OpenAI
        "anthropic/claude-sonnet-4",        # Anthropic
        "gemini/gemini-1.5-flash",          # Google
        "groq/llama-3.1-70b-versatile",     # Groq
    ]

    for model in providers:
        try:
            response = completion(
                model=model,
                messages=[{"role": "user", "content": "Say hello!"}],
                max_tokens=20
            )
            print(f"✅ {model}: {response.choices[0].message.content}")
        except Exception as e:
            print(f"❌ {model}: {str(e)}")


# ============================================================
# Example 2: Using Router for load balancing
# ============================================================

def test_router():
    """Test Router with fallbacks and load balancing"""

    router = Router(
        model_list=[
            {
                "model_name": "gpt-4",
                "litellm_params": {
                    "model": "gpt-4o",
                    "api_key": os.environ.get("OPENAI_API_KEY"),
                },
            },
            {
                "model_name": "gpt-4",  # Same model_name for load balancing
                "litellm_params": {
                    "model": "azure/gpt-4",
                    "api_key": os.environ.get("AZURE_API_KEY"),
                    "api_base": os.environ.get("AZURE_API_BASE"),
                },
            },
            {
                "model_name": "claude",
                "litellm_params": {
                    "model": "anthropic/claude-sonnet-4",
                    "api_key": os.environ.get("ANTHROPIC_API_KEY"),
                },
            },
        ],
        fallbacks=[{"gpt-4": ["claude"]}],  # Fallback to Claude if GPT-4 fails
        routing_strategy="simple-shuffle",   # Load balance between deployments
    )

    response = router.completion(
        model="gpt-4",
        messages=[{"role": "user", "content": "Hello!"}]
    )

    print(f"Router response: {response.choices[0].message.content}")
    return response


# ============================================================
# Example 3: Streaming responses
# ============================================================

def test_streaming():
    """Test streaming completion"""
    response = completion(
        model="gpt-4o",
        messages=[{"role": "user", "content": "Count from 1 to 5"}],
        stream=True
    )

    print("Streaming response:")
    for chunk in response:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)
    print()


# ============================================================
# Example 4: Function calling
# ============================================================

def test_function_calling():
    """Test function calling with tools"""

    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": "Get the current weather in a location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city and state, e.g. San Francisco, CA",
                        },
                        "unit": {
                            "type": "string",
                            "enum": ["celsius", "fahrenheit"],
                        },
                    },
                    "required": ["location"],
                },
            },
        }
    ]

    response = completion(
        model="gpt-4o",
        messages=[{"role": "user", "content": "What's the weather in San Francisco?"}],
        tools=tools,
        tool_choice="auto"
    )

    print("Function calling response:")
    print(response.choices[0].message)
    return response


# ============================================================
# Example 5: Embeddings
# ============================================================

def test_embeddings():
    """Test embedding generation"""
    response = embedding(
        model="text-embedding-ada-002",
        input=["Hello world", "LiteLLM is awesome"]
    )

    print(f"Generated {len(response.data)} embeddings")
    print(f"Embedding dimension: {len(response.data[0].embedding)}")
    return response


# ============================================================
# Example 6: Image generation
# ============================================================

def test_image_generation():
    """Test image generation"""
    response = image_generation(
        model="dall-e-3",
        prompt="A cute baby sea otter",
        n=1,
        size="1024x1024"
    )

    print(f"Generated image URL: {response.data[0].url}")
    return response


# ============================================================
# Example 7: Async completion
# ============================================================

async def test_async_completion():
    """Test async completion"""
    from litellm import acompletion

    response = await acompletion(
        model="gpt-4o",
        messages=[{"role": "user", "content": "Hello async!"}]
    )

    print(f"Async response: {response.choices[0].message.content}")
    return response


# ============================================================
# Example 8: Batch completion
# ============================================================

async def test_batch_completion():
    """Test batch completion for multiple requests"""
    from litellm import batch_completion

    requests = [
        {
            "model": "gpt-4o",
            "messages": [{"role": "user", "content": f"What is {i}+{i}?"}]
        }
        for i in range(5)
    ]

    responses = await batch_completion(requests)

    for i, response in enumerate(responses):
        print(f"Request {i}: {response.choices[0].message.content}")

    return responses


# ============================================================
# Main
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("LiteLLM SDK Examples")
    print("=" * 60)
    print()
    print("⚠️  Add your API keys to .env file before running:")
    print("   OPENAI_API_KEY=your-key")
    print("   ANTHROPIC_API_KEY=your-key")
    print("   GOOGLE_API_KEY=your-key")
    print()
    print("Then uncomment the examples you want to test.")
    print("=" * 60)

    # Uncomment to test:
    # test_direct_completion()
    # test_multiple_providers()
    # test_router()
    # test_streaming()
    # test_function_calling()
    # test_embeddings()
    # test_image_generation()

    # For async examples:
    # import asyncio
    # asyncio.run(test_async_completion())
    # asyncio.run(test_batch_completion())
