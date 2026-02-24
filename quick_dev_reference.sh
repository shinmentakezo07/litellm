#!/bin/bash
# Quick Development Reference for LiteLLM

echo "🔧 LiteLLM Development Quick Reference"
echo "======================================"
echo ""

echo "📍 Current Status:"
if netstat -tlnp 2>/dev/null | grep -q ":4000" || ss -tlnp 2>/dev/null | grep -q ":4000"; then
    echo "  ✅ Proxy: http://localhost:4000"
else
    echo "  ❌ Proxy: Not running"
fi

if docker ps | grep -q litellm_db; then
    echo "  ✅ Database: localhost:5432"
else
    echo "  ❌ Database: Not running"
fi

echo ""
echo "🚀 Quick Commands:"
echo ""
echo "  Start Services:"
echo "    docker compose up -d db"
echo "    poetry run litellm --config proxy_server_config.yaml --port 4000"
echo ""
echo "  Development:"
echo "    make test-unit              # Run unit tests"
echo "    make lint                   # Check code quality"
echo "    make format                 # Format code"
echo "    poetry run pytest tests/test_litellm/test_completion.py -v"
echo ""
echo "  Database:"
echo "    poetry run prisma generate  # Generate client"
echo "    poetry run prisma migrate dev"
echo "    poetry run prisma studio    # View database"
echo ""
echo "  Testing:"
echo "    poetry run python test_litellm.py"
echo "    poetry run python demo_proxy.py"
echo "    poetry run python examples_sdk.py"
echo ""
echo "📚 Documentation:"
echo "    DEV_GUIDE.md           - Complete development guide"
echo "    ARCHITECTURE_GUIDE.md  - Codebase architecture"
echo "    RUNNING.md             - Quick reference"
echo "    CLAUDE.md              - Project instructions"
echo ""
echo "🔗 URLs:"
echo "    Proxy:      http://localhost:4000"
echo "    Swagger:    http://localhost:4000/"
echo "    Health:     http://localhost:4000/health/readiness"
echo "    Metrics:    http://localhost:4000/metrics"
echo ""
echo "🔑 Master Key: sk-1234"
echo ""
