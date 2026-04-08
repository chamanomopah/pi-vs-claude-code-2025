# LiveKit + Pi Integration - 5-Minute Implementation Guide

> **Quick Implementation Guide for LiveKit Voice Chat Extension**
> Created: 2026-04-06 | Based on proposal analysis

---

## Table of Contents
1. [Prerequisites](#1-prerequisites)
2. [5-Minute Setup](#2-5-minute-setup)
3. [Extension Installation](#3-extension-installation)
4. [Configuration](#4-configuration)
5. [Usage](#5-usage)
6. [Testing](#6-testing)
7. [Troubleshooting](#7-troubleshooting)

---

## 1. Prerequisites

### 1.1 Required Software

| Software | Version | Purpose |
|----------|---------|---------|
| **Node.js** | ≥20.0 | Runtime for Pi extension |
| **Python** | ≥3.10, <3.14 | Runtime for LiveKit agent |
| **LiveKit Server** | latest | Self-hosted WebRTC server |
| **Bun** | latest | Package manager for Pi |

### 1.2 Required API Keys

| Service | Key Name | Purpose |
|---------|----------|---------|
| **Deepgram** | `DEEPGRAM_API_KEY` | Speech-to-Text |
| **Cartesia** | `CARTESIA_API_KEY` | Text-to-Speech |
| **Google** | `GOOGLE_API_KEY` | Alternative STT/TTS (optional) |

**Note:** Your `.env` already has these keys configured.

### 1.3 System Requirements

- **OS:** Windows, macOS, or Linux
- **RAM:** 4GB minimum, 8GB recommended
- **Network:** Localhost connection (no internet required for core functionality)
- **Audio:** Microphone and speakers (or use browser client)

---

## 2. 5-Minute Setup

### Step 1: Install LiveKit Server (2 min)

**Windows (PowerShell):**
```powershell
# Download LiveKit Server
curl -L https://github.com/livekit/livekit/releases/download/v1.5.0/livekit_1.5.0_windows_amd64.zip -o livekit.zip
Expand-Archive livekit.zip -DestinationPath .
cd livekit_*

# Start in dev mode
.\livekit-server --dev
```

**macOS/Linux:**
```bash
# Download LiveKit Server
curl -sSL https://get.livekit.io/cli | bash
lk dev  # Starts LiveKit Server in dev mode
```

**Verify:** You should see output like:
```
[LiveKit] LiveKit Server started
[LiveKit] WebSocket server listening on: ws://localhost:7880
```

### Step 2: Install Python Dependencies (1 min)

```bash
# Navigate to the livekit-pi-extension directory
cd scripts/livekit-pi-extension

# Create virtual environment (optional but recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install livekit-agents[silero] livekit-plugins-openai livekit-plugins-deepgram livekit-plugins-cartesia python-dotenv
```

**Verify:**
```bash
python -c "import livekit; print('LiveKit installed successfully')"
```

### Step 3: Verify Environment Variables (1 min)

Check that your `.env` file has the required keys:

```bash
cd scripts/livekit-pi-extension
cat .env
```

You should see:
```
CARTESIA_API_KEY=sk_car_...
GOOGLE_API_KEY=AIzaSy...
DEEPGRAM_API_KEY=5c2194...
```

**If missing, add them:**
```bash
# Add LiveKit configuration
echo "LIVEKIT_URL=ws://localhost:7880" >> .env
echo "LIVEKIT_API_KEY=devkey" >> .env
echo "LIVEKIT_API_SECRET=secret" >> .env
```

### Step 4: Test Python Agent (1 min)

Run the existing Python agent to verify setup:

```bash
cd scripts/livekit-pi-extension
python livekit_basic_agent.py console
```

**Expected output:**
```
[LiveKit] Connecting to room...
[LiveKit] Connected to room: console_room
[LiveKit] Listening...
```

**Type "hello" and press Enter** - you should hear a response if TTS is configured.

---

## 3. Extension Installation

### Option A: Quick Test (Recommended for First Run)

```bash
# From project root
pi -e extensions/livekit.ts
```

This loads the extension without permanent installation.

### Option B: Permanent Installation

```bash
# Create symlink for auto-discovery
# Windows (PowerShell as Administrator):
New-Item -ItemType SymbolicLink -Path ".pi\extensions\livekit.ts" -Value "extensions\livekit.ts"

# macOS/Linux:
ln -s $(pwd)/extensions/livekit.ts .pi/extensions/livekit.ts
```

Now the extension loads automatically when you run `pi`.

---

## 4. Configuration

### 4.1 Extension Configuration

The extension reads configuration from:

**Priority order:**
1. `scripts/livekit-pi-extension/.env` (highest priority)
2. `~/.pi/agent/.env`
3. Environment variables
4. Default values

### 4.2 Configuration File

Create or edit `scripts/livekit-pi-extension/.env`:

```env
# LiveKit Server Configuration
LIVEKIT_URL=ws://localhost:7880
LIVEKIT_API_KEY=devkey
LIVEKIT_API_SECRET=secret
LIVEKIT_ROOM=default-room
LIVEKIT_IDENTITY=pi-assistant

# STT Configuration (Deepgram)
DEEPGRAM_API_KEY=5c2194e0b6b4c3063ee34ccfbbd3f3c3d31b06f3
DEEPGRAM_MODEL=nova-2
DEEPGRAM_LANGUAGE=en-US

# TTS Configuration (Cartesia)
CARTESIA_API_KEY=sk_car_85JMfuQWcNjk8QcAozreo1
CARTESIA_MODEL=sonic-3
CARTESIA_VOICE=79a125e8-cd45-4c93-9ae2-3f2e0f6a0c9a
CARTESIA_SAMPLE_RATE=24000

# Voice Activity Detection
VAD_ENABLED=true
VAD_THRESHOLD=0.5
VAD_SILENCE_DURATION_MS=800

# Session Configuration
SESSION_TIMEOUT_MS=300000
MAX_TRANSCRIPT_LENGTH=1000

# Display Configuration
DISPLAY_LAST_SENTENCE=true
```

### 4.3 Pi Configuration

No additional Pi configuration needed! The extension:
- Uses your current Pi model (from `/model` or settings)
- Respects your thinking level
- Works with your existing tools

---

## 5. Usage

### 5.1 Basic Usage

**Step 1: Start Pi**
```bash
pi
```

**Step 2: Activate Voice Mode**
```
/speak
```

**Step 3: Confirmation Dialog**
```
┌─────────────────────────────────────┐
│  Start Voice Chat?                  │
│                                     │
│  Room: default-room                 │
│  STT: Deepgram nova-2               │
│  TTS: Cartesia sonic-3              │
│                                     │
│  [Enter] Start    [Esc] Cancel      │
└─────────────────────────────────────┘
```

**Step 4: Speak!**
- The extension will connect to LiveKit
- You'll see status: "🎤 Listening..."
- Speak into your microphone
- Your words will be transcribed and sent to Pi
- Pi will respond via voice AND display the last sentence in the terminal

### 5.2 Commands

| Command | Description |
|---------|-------------|
| `/speak [room]` | Start voice mode (optional room name) |
| `/un speak` | Stop voice mode |
| `/speak-status` | Show current voice chat status |
| `/speak-room <name>` | Switch to a different room |

### 5.3 Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `Ctrl+C` (once) | Clear editor (when not in voice mode) |
| `Ctrl+C` (twice) | Stop voice mode and quit |
| `Escape` | Cancel current operation |

---

## 6. Testing

### 6.1 Quick Test (2 min)

**Test 1: Extension Loads**
```bash
pi -e extensions/livekit.ts
```
Expected: Pi starts without errors.

**Test 2: Speak Command**
```
/speak
```
Expected: Confirmation dialog appears.

**Test 3: Status Check**
```
/speak-status
```
Expected: Status display showing current state.

### 6.2 Full Integration Test (5 min)

**Prerequisites:**
- LiveKit Server running (`lk dev` or `livekit-server --dev`)
- Microphone connected
- Speakers/audio output

**Test Steps:**

1. **Start LiveKit Server** (if not running)
   ```bash
   lk dev
   ```

2. **Start Pi with extension**
   ```bash
   pi -e extensions/livekit.ts
   ```

3. **Activate voice mode**
   ```
   /speak
   ```

4. **Test speech**
   - Speak: "Hello, what's two plus two?"
   - Expected: Agent responds via voice
   - Expected: Last sentence displayed in terminal

5. **Test tool calls**
   - Speak: "Read the file .env and tell me the API keys"
   - Expected: Agent uses `read` tool
   - Expected: Agent responds with content

6. **Stop voice mode**
   ```
   /un speak
   ```

### 6.3 Browser Client Test (Optional)

If you want to test with a browser client:

1. **Open LiveKit Playground**
   - Navigate to https://cloud.livekit.io/playground
   - Or use local playground if installed

2. **Connect to your room**
   - URL: `ws://localhost:7880`
   - API Key: `devkey`
   - Secret: `secret`
   - Room: `default-room`

3. **Test audio**
   - Speak in browser
   - Should hear Pi's response

---

## 7. Troubleshooting

### 7.1 Common Issues

**Issue: "LiveKit connection failed"**

**Symptoms:**
- Error: `Failed to connect to LiveKit server`
- Extension doesn't start

**Solutions:**
```bash
# Check if LiveKit Server is running
# Windows:
Get-NetTCPConnection -LocalPort 7880

# macOS/Linux:
lsof -i :7880

# If not running, start it:
lk dev
# or
livekit-server --dev
```

---

**Issue: "DEEPGRAM_API_KEY not found"**

**Symptoms:**
- Error: `DEEPGRAM_API_KEY is required`
- Extension fails to start

**Solutions:**
```bash
# Check .env file
cat scripts/livekit-pi-extension/.env | grep DEEPGRAM

# If missing, add it:
echo "DEEPGRAM_API_KEY=your-key-here" >> scripts/livekit-pi-extension/.env

# Or export directly:
export DEEPGRAM_API_KEY=your-key-here
```

---

**Issue: "No audio output"**

**Symptoms:**
- Agent transcribes correctly
- But no voice response

**Solutions:**
```bash
# Check Cartesia API key
cat scripts/livekit-pi-extension/.env | grep CARTESIA

# Test Cartesia API directly:
curl -X POST https://api.cartesia.ai/tts \
  -H "Authorization: Bearer $CARTESIA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello", "model": "sonic-3", "voice": "79a125e8-cd45-4c93-9ae2-3f2e0f6a0c9a"}'

# Check system audio settings
# Windows:
powershell "Get-AudioDevice -List"

# macOS:
osascript -e "get volume settings"

# Linux:
alsamixer
```

---

**Issue: "Python agent not responding"**

**Symptoms:**
- Extension starts
- But no voice input/output

**Solutions:**
```bash
# Check if Python agent is running
ps aux | grep python | grep livekit

# Manually test Python agent
cd scripts/livekit-pi-extension
python livekit_basic_agent.py console

# Check Python version (must be >=3.10, <3.14)
python --version

# Reinstall dependencies
pip install --upgrade livekit-agents[silero] livekit-plugins-openai livekit-plugins-deepgram livekit-plugins-cartesia
```

---

### 7.2 Debug Mode

Enable debug logging:

```bash
# Set debug environment variable
export LIVEKIT_DEBUG=1
export PI_DEBUG=1

# Run Pi with verbose output
pi -e extensions/livekit.ts --verbose
```

### 7.3 Getting Help

If issues persist:

1. **Check logs:**
   ```bash
   # Pi logs
   cat ~/.pi/agent/sessions/*.jsonl | tail -100

   # LiveKit Server logs
   # Usually in console output
   ```

2. **Verify configuration:**
   ```bash
   # Test .env loading
   node -e "require('dotenv').config({path: 'scripts/livekit-pi-extension/.env'}); console.log(process.env.LIVEKIT_URL)"
   ```

3. **Minimal test:**
   ```bash
   # Test without extension
   pi

   # Test extension only
   pi -e extensions/livekit.ts --no-session
   ```

---

## 8. Next Steps

After successful setup:

1. **Customize voice**
   - Try different Cartesia voices
   - Adjust TTS sample rate
   - Tune VAD threshold

2. **Extend functionality**
   - Add custom commands
   - Integrate with other Pi tools
   - Build custom UI components

3. **Deploy to production**
   - Use production LiveKit Cloud or self-hosted server
   - Configure SSL/TLS
   - Set up authentication

4. **Multi-user support**
   - Create separate rooms for each user
   - Implement user authentication
   - Scale to multiple concurrent sessions

---

## 9. Quick Reference Card

```
╔══════════════════════════════════════════════════════════════════╗
║              LIVEKIT + PI QUICK REFERENCE                        ║
╠══════════════════════════════════════════════════════════════════╣
║  START:                                                         ║
║    1. lk dev                                    (LiveKit)       ║
║    2. pi -e extensions/livekit.ts              (Pi)            ║
║    3. /speak                                   (Voice mode)    ║
║                                                                  ║
║  COMMANDS:                                                       ║
║    /speak [room]     Start voice mode                           ║
║    /un speak         Stop voice mode                            ║
║    /speak-status     Show status                                ║
║    /speak-room <n>   Switch room                               ║
║                                                                  ║
║  TROUBLESHOOTING:                                                ║
║    Connection:    Check "lk dev" is running                     ║
║    API Keys:      Verify .env file                             ║
║    Audio:         Test mic/speakers work                        ║
║    Python:        Check version >=3.10, <3.14                   ║
║                                                                  ║
║  FILES:                                                         ║
║    Extension:     extensions/livekit.ts                        ║
║    Agent:         scripts/livekit-pi-extension/pi_agent.py     ║
║    Config:        scripts/livekit-pi-extension/.env            ║
║    Docs:          docs/LIVEKIT_IMPLEMENTATION_GUIDE.md         ║
╚══════════════════════════════════════════════════════════════════╝
```

---

**Implementation Time:** ~5 minutes for basic setup  
**Full Testing Time:** ~10-15 minutes  
**Production Ready:** After configuration tuning and testing

**For detailed implementation, see:** `extensions/livekit.ts`
