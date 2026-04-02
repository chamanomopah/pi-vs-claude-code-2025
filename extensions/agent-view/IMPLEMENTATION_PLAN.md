# Agent View Extension - Implementation Plan for Fixes

## Current State

- ✅ config.ts - Configuration system exists
- ✅ storage.ts - Preset persistence exists
- ✅ logger.ts - Logging system exists
- ✅ error-handler.ts - Error handling exists
- ✅ health-monitor.ts - Health monitoring exists
- ⚠️ index.ts - Exists but incomplete
- ❌ monitor.ts - MISSING
- ❌ widget.ts - MISSING

## Fixes Required (Per User Request)

### 1. Progress Calculation (monitor.ts:334-354)
**Issue:** Progress grows 5% per refresh regardless of activity
**Fix:** Base calculation on turns, tools executed, messages exchanged

```typescript
// In AgentState, add tracking:
interface AgentState {
  // ... existing fields
  turnsCompleted: number;
  messagesExchanged: number;
  expectedMaxTurns?: number;
}

// In updateElapsedTimes():
private updateElapsedTimes(): void {
  const now = Date.now();
  for (const agent of this.state.getAllAgents()) {
    if (agent.startTime && !agent.endTime) {
      const elapsed = now - agent.startTime;
      
      let progress = agent.progress;
      if (agent.status === "running" || agent.status === "waiting") {
        // Calculate based on activity, not time
        const activityScore = agent.turnsCompleted * 10 + agent.toolsUsed * 5 + agent.messagesExchanged * 2;
        const maxScore = agent.expectedMaxTurns ? agent.expectedMaxTurns * 10 : 100;
        progress = Math.min(95, Math.floor((activityScore / maxScore) * 100));
      } else if (agent.status === "complete") {
        progress = 100;
      }

      this.state.upsertAgent({
        id: agent.id,
        elapsed,
        progress,
      });
    }
  }
  // Emit agent_view:update event
  this.pi.events?.emit("agent_view:update", {
    agents: this.state.getFilteredAgents(this.filters),
    timestamp: Date.now()
  });
}
```

### 2. extractAgentInfo() Fallbacks (index.ts:262-301)
**Issue:** Only handles `prompt-{name}.md` format
**Fix:** Add 4 fallback methods

```typescript
function extractAgentInfo(args: string[]): { name: string; task: string; source: string } | null {
  const hasJSONMode = args.includes("--mode") && args.includes("json");
  const hasPrintFlag = args.includes("-p") || args.includes("--print");
  if (!hasJSONMode || !hasPrintFlag) return null;

  let agentName: string | null = null;
  let task = "Running...";
  let source = "unknown";

  // Method 1: --append-system-prompt with prompt-{name}.md (agent-team)
  const promptIndex = args.indexOf("--append-system-prompt");
  if (promptIndex !== -1 && args[promptIndex + 1]) {
    const promptPath = args[promptIndex + 1];
    let match = promptPath.match(/prompt-([^.]+)\.md$/);
    if (match) { agentName = match[1]; source = "agent-team"; }
  }

  // Method 2: --append-system-prompt with {name}.md (agent-chain, direct)
  if (!agentName && promptIndex !== -1 && args[promptIndex + 1]) {
    const match = args[promptIndex + 1].match(/([^.\/]+)\.md$/);
    if (match) { agentName = match[1]; source = "agent-chain"; }
  }

  // Method 3: -c/--config {name}.md (subagent extension)
  if (!agentName) {
    const configIndex = Math.max(args.indexOf("-c"), args.indexOf("--config"));
    if (configIndex !== -1 && args[configIndex + 1]) {
      const match = args[configIndex + 1].match(/([^.\/]+)\.md$/);
      if (match) { agentName = match[1]; source = "subagent"; }
    }
  }

  // Method 4: Last .md argument (fallback)
  if (!agentName) {
    for (let i = args.length - 1; i >= 0; i--) {
      if (!args[i].startsWith("-") && args[i].endsWith(".md")) {
        const match = args[i].match(/([^.\/]+)\.md$/);
        if (match) { agentName = match[1]; source = "unknown"; break; }
      }
    }
  }

  if (!agentName) return null;

  // Extract task (last non-flag arg)
  const taskIndex = args.findLastIndex((arg, i) => 
    !arg.startsWith("-") && i !== promptIndex - 1 && i !== promptIndex && !arg.endsWith(".md")
  );
  if (taskIndex !== -1) task = args[taskIndex];

  // Detect source with enhanced detection
  if (args.includes("--agent-team")) source = "agent-team";
  else if (args.includes("--agent-chain")) source = "agent-chain";
  else if (args.includes("--pi-pi")) source = "pi-pi";
  else if (args.includes("--subagent") || args.includes("-c")) source = "subagent";
  else if (source === "unknown") {
    // Pattern matching fallback
    if (args.some(a => a.includes("team"))) source = "agent-team";
    else if (args.some(a => a.includes("chain"))) source = "agent-chain";
    else if (args.some(a => a.includes("pi-pi"))) source = "pi-pi";
  }

  return { name: agentName, task, source };
}
```

### 3. Agent View Events (monitor.ts)
**Issue:** Doesn't emit `agent_view:*` events
**Fix:** Add event emissions

```typescript
// In AgentMonitor class:
// After starting monitoring:
start(): void {
  if (this.isRunning) return;
  this.isRunning = true;
  if (this.config.autoRefresh) this.startRefreshTimer();
  this.startCleanupTimer();
  this.emit("agents:changed");
  
  // Emit agent_view:update for other extensions
  this.pi.events?.emit("agent_view:update", {
    agents: this.getAgents(),
    timestamp: Date.now()
  });
}

// In updateElapsedTimes() (called on refresh):
refresh(): void {
  this.updateElapsedTimes();
  this.emit("agents:changed");
  
  // Emit agent_view:update
  this.pi.events?.emit("agent_view:update", {
    agents: this.getAgents(),
    timestamp: Date.now()
  });
}
```

### 4. Agent Filters (SPEC 9.1)
**Issue:** Filter system missing
**Fix:** Add filter interface and commands

```typescript
// In monitor.ts, add:
export interface AgentFilters {
  status?: AgentStatus;
  name?: string;  // wildcard supported (*)
  source?: AgentSource;
}

// Wildcard matching helper:
function matchWildcard(pattern: string, text: string): boolean {
  if (!pattern) return true;
  if (pattern === "*") return true;
  const regex = new RegExp("^" + pattern.replace(/\*/g, ".*") + "$");
  return regex.test(text);
}

// In StateManager class:
getFilteredAgents(filters: AgentFilters): AgentState[] {
  let agents = this.getAllAgents();
  
  if (filters.status) {
    agents = agents.filter(a => a.status === filters.status);
  }
  if (filters.name) {
    agents = agents.filter(a => matchWildcard(filters.name!, a.name));
  }
  if (filters.source) {
    agents = agents.filter(a => a.source === filters.source);
  }
  
  return agents;
}

// In AgentMonitor class:
private filters: AgentFilters = {};

setFilters(filters: AgentFilters): void {
  this.filters = filters;
  this.emit("agents:changed");
  
  // Emit agent_view:update with filtered agents
  this.pi.events?.emit("agent_view:update", {
    agents: this.state.getFilteredAgents(filters),
    timestamp: Date.now()
  });
}

getAgents(): AgentState[] {
  return this.filters && (this.filters.status || this.filters.name || this.filters.source)
    ? this.state.getFilteredAgents(this.filters)
    : this.state.sortAgents(this.config.sortMode);
}
```

```typescript
// In index.ts, add filter commands:
pi.registerCommand({
  name: "agent-view-filter",
  description: "Filter agents by status, name, or source"
}, async (args: { status?: string; name?: string; source?: string; clear?: boolean }) => {
  if (args.clear === true || args.clear === "true") {
    extensionState.monitor?.setFilters({});
    await pi.notify("Filters cleared");
    return;
  }

  const filters: AgentFilters = {};
  let applied = false;

  if (args.status) {
    const validStatuses = ["idle", "starting", "running", "waiting", "complete", "error", "aborted"];
    if (validStatuses.includes(args.status)) {
      filters.status = args.status as AgentStatus;
      applied = true;
    } else {
      await pi.notify(`Invalid status. Valid: ${validStatuses.join(", ")}`);
      return;
    }
  }

  if (args.name) {
    filters.name = args.name;
    applied = true;
  }

  if (args.source) {
    const validSources = ["agent-team", "agent-chain", "pi-pi", "subagent", "unknown"];
    if (validSources.includes(args.source)) {
      filters.source = args.source as AgentSource;
