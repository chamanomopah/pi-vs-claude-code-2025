#!/bin/bash

# LiveKit + Pi Setup Test Script
# Tests if all components are properly configured

echo "========================================"
echo "LiveKit + Pi Setup Test"
echo "========================================"
echo ""

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counters
PASSED=0
FAILED=0

# Function to print test result
print_result() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✓ PASS${NC}: $2"
        PASSED=$((PASSED + 1))
    else
        echo -e "${RED}✗ FAIL${NC}: $2"
        FAILED=$((FAILED + 1))
    fi
}

# Test 1: Check Python version
echo "Testing Python version..."
PYTHON_VERSION=$(python --version 2>&1 | awk '{print $2}')
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

if [ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -ge 10 ] && [ "$PYTHON_MINOR" -lt 14 ]; then
    print_result 0 "Python version $PYTHON_VERSION (>=3.10, <3.14)"
else
    print_result 1 "Python version $PYTHON_VERSION (need >=3.10, <3.14)"
fi
echo ""

# Test 2: Check if required Python packages are installed
echo "Testing Python packages..."
python -c "import livekit" 2>/dev/null
print_result $? "livekit-agents package"

python -c "from livekit.plugins import deepgram" 2>/dev/null
print_result $? "livekit-plugins-deepgram"

python -c "from livekit.plugins import cartesia" 2>/dev/null
print_result $? "livekit-plugins-cartesia"

python -c "from livekit.plugins import openai" 2>/dev/null
print_result $? "livekit-plugins-openai"

python -c "import dotenv" 2>/dev/null
print_result $? "python-dotenv"
echo ""

# Test 3: Check if .env file exists
echo "Testing configuration..."
if [ -f ".env" ]; then
    print_result 0 ".env file exists"
else
    print_result 1 ".env file not found"
fi
echo ""

# Test 4: Check required environment variables
if [ -f ".env" ]; then
    echo "Testing environment variables..."
    grep -q "LIVEKIT_URL" .env
    print_result $? "LIVEKIT_URL configured"

    grep -q "DEEPGRAM_API_KEY" .env
    print_result $? "DEEPGRAM_API_KEY configured"

    grep -q "CARTESIA_API_KEY" .env
    print_result $? "CARTESIA_API_KEY configured"
    echo ""
fi

# Test 5: Check if pi_agent.py exists
echo "Testing Python agent..."
if [ -f "pi_agent.py" ]; then
    print_result 0 "pi_agent.py exists"
else
    print_result 1 "pi_agent.py not found"
fi

if [ -f "livekit_basic_agent.py" ]; then
    print_result 0 "livekit_basic_agent.py exists (reference)"
else
    print_result 1 "livekit_basic_agent.py not found"
fi
echo ""

# Test 6: Check if LiveKit Server is running
echo "Testing LiveKit Server..."
if command -v lsof &> /dev/null; then
    lsof -i :7880 &> /dev/null
    print_result $? "LiveKit Server running on port 7880"
elif command -v netstat &> /dev/null; then
    netstat -an | grep 7880 | grep LISTEN &> /dev/null
    print_result $? "LiveKit Server running on port 7880"
else
    echo -e "${YELLOW}⚠ SKIP${NC}: Cannot check port 7880 (no lsof/netstat)"
fi
echo ""

# Test 7: Check if Pi extension exists
echo "Testing Pi extension..."
if [ -f "../../extensions/livekit.ts" ]; then
    print_result 0 "livekit.ts extension exists"
else
    print_result 1 "livekit.ts extension not found"
fi

if [ -f "../../.pi/extensions/livekit.ts" ]; then
    print_result 0 "livekit.ts symlink exists"
else
    echo -e "${YELLOW}⚠ SKIP${NC}: livekit.ts symlink not found (optional)"
fi
echo ""

# Summary
echo "========================================"
echo "Test Summary"
echo "========================================"
echo -e "${GREEN}Passed: $PASSED${NC}"
echo -e "${RED}Failed: $FAILED${NC}"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}All tests passed!${NC}"
    echo ""
    echo "You can now run:"
    echo "  1. Start LiveKit Server: lk dev"
    echo "  2. Start Pi: pi -e extensions/livekit.ts"
    echo "  3. Activate voice mode: /speak"
    exit 0
else
    echo -e "${RED}Some tests failed. Please fix the issues above.${NC}"
    echo ""
    echo "Common fixes:"
    echo "  - Install Python packages: pip install livekit-agents[silero] livekit-plugins-openai livekit-plugins-deepgram livekit-plugins-cartesia python-dotenv"
    echo "  - Start LiveKit Server: lk dev"
    echo "  - Create .env file with API keys"
    exit 1
fi
