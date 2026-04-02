# Agent View v1.2.0 - Fixes Applied

## Summary of Corrections

This document summarizes the fixes applied to agent-view extension to resolve the identified issues.

## Issues Fixed

### 1. Progress Calculation (monitor.ts)
**Problem:** Progress grows 5% per refresh regardless of actual activity.

**Solution:**
- Calculate progress based on completed turns, tools executed, and messages exchanged
- Only increment progress when actual activity is detected
- Set progress to 100% only on completion

```typescript
// In updateElapsedTimes():
// Track turns, tools, messages in AgentState
// Calculate: (turns * 10 + tools * 5 + messages * 2) / expectedMax * 100
```

### 2. extractAgentInfo() Logic (index.ts:262-301)
**Problem:** Assumes only `prompt-{name}.md` format, fragile implementation.

**Solution:**
- Added 4 fallback formats for agent name extraction:
  1. `prompt-{name}.md` (agent-team)
  2. `{name}.md` (agent-chain, direct)
  3. `-c/--config {name}.md` (subagent extension)
  4. Last .md argument (fallback)
- Documented as implementation-specific

### 3. Agent View Events (monitor.ts)
**Problem:** Code listens to `subagent:*` but doesn't emit `agent_view:*` events.

**Solution:**
- Emit `agent_view:opened` when view opens
- Emit `agent_view:closed` when view closes
- Emit `agent_view:update` on agent changes

```typescript
pi.events?.emit("agent_view:update", {
  agents: Array.from(this.agents.values()),
  timestamp: Date.now(),
});
```

### 4. Agent Filters (SPEC 9.1)
**Problem:** Filter commands and interface missing.

**Solution:**
- Added `AgentFilters` interface:
```typescript
interface AgentFilters {
  status?: AgentStatus;
  name?: string;  // wildcard supported
  source?: AgentSource;
}
```
- Added filter commands:
  - `/agent-view filter status:running`
  - `/agent-view filter name:scout-*`
  - `/agent-view filter --clear`
- Implemented `setFilters()` method in AgentMonitor
- Implemented wildcard matching for name filter

### 5. Source Detection (index.ts)
**Problem:** Detection may fail for some orchestrator types.

**Solution:**
- Enhanced detection with multiple flag checks:
  - Explicit flags: `--agent-team`, `--agent-chain`, `--pi-pi`, `--subagent`
  - Pattern matching: args containing "team", "chain", "pi-pi"
  - Config file analysis: `-c` flag usage
- Improved fallback logic

### 6. isToolCallEventType() (CLAUDE.md:7)
**Problem:** Mentioned but not defined.

**Solution:**
- Comment is documentation reference for Pi extensions
- Not applicable to this extension (not needed)
- Left as documentation note only

## Files Modified

1. **index.ts** - Main extension file
   - Added `AgentFilters` import
   - Added `filters` to `AgentViewExtension` interface
   - Added `handleFilterCommand()` function
   - Enhanced `extractAgentInfo()` with 4 fallback methods
   - Added event emissions for `agent_view:opened/closed`
   - Added filter commands registration

2. **monitor.ts** - Monitor module
   - Added `AgentFilters` interface export
   - Added `filters` field to `AgentMonitor` class
   - Added `setFilters()` method
   - Added wildcard matching helper `matchWildcard()`
   - Fixed progress calculation in `updateElapsedTimes()`
   - Added `agent_view:update` event emission
   - Enhanced `StateManager` to support filtering

## Testing

```bash
# Test filter commands
/agent-view filter status:running
/agent-view filter name:scout-*
/agent-view filter source:agent-team
/agent-view filter --clear

# Test events
pi -e extensions/agent-view/index.ts
# Check that agent_view:opened/closed/update events are emitted

# Test extractAgentInfo with various formats
pi --mode json -p --append-system-prompt .pi/agents/prompt-test.md "task"
pi --mode json -p -c .pi/agents/test.md "task"
```

## Backward Compatibility

All changes are backward compatible:
- Existing commands work unchanged
- New filter commands are optional
- Event emissions are additions, not modifications
- Progress calculation changes are internal

## Version

v1.2.0 - All moderate issues resolved
