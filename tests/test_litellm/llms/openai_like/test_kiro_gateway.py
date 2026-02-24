"""
Tests for Kiro Gateway provider configuration and integration.
"""

import os
import sys

try:
    import pytest
except ImportError:
    pytest = None

# Add workspace to path
workspace_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.."))
sys.path.insert(0, workspace_path)

import litellm


class TestKiroGatewayProviderConfig:
    """Test Kiro Gateway provider configuration"""

    def test_kiro_gateway_in_provider_list(self):
        """Test that kiro_gateway is in the provider list."""
        from litellm import LlmProviders

        assert hasattr(LlmProviders, "KIRO_GATEWAY")
        assert LlmProviders.KIRO_GATEWAY.value == "kiro_gateway"
        assert "kiro_gateway" in litellm.provider_list

    def test_kiro_gateway_json_config_exists(self):
        """Test that kiro_gateway is configured in providers.json."""
        from litellm.llms.openai_like.json_loader import JSONProviderRegistry

        assert JSONProviderRegistry.exists("kiro_gateway")

        kiro_gateway = JSONProviderRegistry.get("kiro_gateway")
        assert kiro_gateway is not None
        assert kiro_gateway.base_url == "http://localhost:8000/v1"
        assert kiro_gateway.api_key_env == "KIRO_GATEWAY_API_KEY"
        assert kiro_gateway.api_base_env == "KIRO_GATEWAY_API_BASE"
        assert kiro_gateway.base_class == "openai_gpt"
        assert kiro_gateway.param_mappings.get("max_completion_tokens") == "max_tokens"

    def test_kiro_gateway_provider_resolution(self):
        """Test that provider resolution finds kiro_gateway."""
        from litellm.litellm_core_utils.get_llm_provider_logic import get_llm_provider

        model, provider, api_key, api_base = get_llm_provider(
            model="kiro_gateway/claude-sonnet-4-5",
            custom_llm_provider=None,
            api_base=None,
            api_key=None,
        )

        assert model == "claude-sonnet-4-5"
        assert provider == "kiro_gateway"
        assert api_base == "http://localhost:8000/v1"

    def test_kiro_gateway_router_config(self):
        """Test that kiro_gateway can be used in Router configuration."""
        from litellm import Router

        router = Router(
            model_list=[
                {
                    "model_name": "kiro-sonnet",
                    "litellm_params": {
                        "model": "kiro_gateway/claude-sonnet-4-5",
                        "api_key": "test-key",
                    },
                }
            ]
        )

        assert len(router.model_list) == 1
        assert router.model_list[0]["model_name"] == "kiro-sonnet"


class TestKiroGatewayIntegration:
    """Integration tests for Kiro Gateway provider"""

    def test_kiro_gateway_completion_basic(self):
        """Test basic completion call to Kiro Gateway."""
        if not os.environ.get("KIRO_GATEWAY_API_KEY"):
            if pytest:
                pytest.skip("KIRO_GATEWAY_API_KEY not set")
            return

        if not os.environ.get("KIRO_GATEWAY_API_BASE"):
            if pytest:
                pytest.skip("KIRO_GATEWAY_API_BASE not set")
            return

        try:
            response = litellm.completion(
                model="kiro_gateway/claude-sonnet-4-5",
                messages=[{"role": "user", "content": "Say 'test successful' and nothing else"}],
                max_tokens=16,
            )

            assert response is not None
            assert hasattr(response, "choices")
            assert len(response.choices) > 0
            assert hasattr(response.choices[0], "message")
            assert hasattr(response.choices[0].message, "content")
            assert response.choices[0].message.content is not None
        except Exception as e:
            if pytest:
                pytest.fail(f"Kiro Gateway completion failed: {str(e)}")
            else:
                raise
