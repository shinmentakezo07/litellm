#!/bin/bash
# Quick start script for LiteLLM development

export PATH="/teamspace/studios/this_studio/.local/bin:$PATH"

echo "🚀 LiteLLM Local Development Environment"
echo "========================================"
echo ""

# Check if services are running
if docker ps | grep -q litellm_db; then
    echo "✅ Database: Running on localhost:5432"
else
    echo "❌ Database: Not running"
    echo "   Start with: docker compose up -d db"
fi

if netstat -tlnp 2>/dev/null | grep -q ":4000" || ss -tlnp 2>/dev/null | grep -q ":4000"; then
    echo "✅ Proxy Server: Running on http://localhost:4000"
else
    echo "❌ Proxy Server: Not running"
    echo "   Start with: poetry run litellm --config proxy_server_config.yaml --port 4000"
fi

echo ""
echo "📚 Quick Commands:"
echo "   poetry run python test_litellm.py    # Test the setup"
echo "   poetry run litellm --help            # See all options"
echo "   make test-unit                       # Run tests"
echo "   make lint                            # Check code quality"
echo ""
echo "🌐 Access Points:"
echo "   Swagger UI: http://localhost:4000/"
echo "   Health: http://localhost:4000/health/readiness"
echo "   Models: http://localhost:4000/v1/models"
echo ""
echo "🔑 Master Key: sk-1234"
echo ""
