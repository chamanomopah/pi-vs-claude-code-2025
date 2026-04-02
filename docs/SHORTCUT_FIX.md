# Shortcut System Fix - F7 → F8 Issue Resolved

## Problem
The F7 key was hardcoded in `agent-team.ts` even though `shortcuts.yaml` specified F8 for "prev-team" action. The `registerShortcuts()` function was accepting hardcoded key IDs in handlers, completely ignoring the YAML configuration.

## Root Cause
In `extensions/agent-team.ts` line 773-788:
```typescript
registerShortcuts(pi, "agent-team", {
  "f6": { ... },  // ❌ Hardcoded key ID
  "f7": { ... },  // ❌ Hardcoded - overrides YAML!
}, _ctx.cwd);
```

This meant:
1. `shortcuts.yaml` defined F8 for prev-team
2. But TypeScript code registered F7 directly
3. Direct registration **overrode** YAML settings

## Solution: Action-Based Shortcut System

### New Approach
**YAML defines which keys** → **Code defines what to do**

The comment after each key ID in YAML is now an **action name** that must match a handler in the code.

### Format Changes

#### shortcuts.yaml (OLD)
```yaml
agent-team:
  - f6   # Cycle to next team
  - f8   # Cycle to previous team
```

#### shortcuts.yaml (NEW)
```yaml
agent-team:
  - f6   # next-team
  - f8   # prev-team
```

The comment is now an action identifier, not just a description.

#### Extension Code (OLD)
```typescript
registerShortcuts(pi, "agent-team", {
  "f6": {        // ❌ Hardcoded key ID
    description: "Cycle to next team",
    handler: async (ctx) => cycleTeam(1)
  },
  "f7": {        // ❌ Ignores YAML
    description: "Cycle to previous team",
    handler: async (ctx) => cycleTeam(-1)
  },
}, _ctx.cwd);
```

#### Extension Code (NEW)
```typescript
registerActionShortcuts(pi, "agent-team", {
  "next-team": {  // ✅ Action name
    description: "Cycle to next team",
    handler: async (ctx) => cycleTeam(1)
  },
  "prev-team": {  // ✅ Action name
    description: "Cycle to previous team", 
    handler: async (ctx) => cycleTeam(-1)
  },
}, _ctx.cwd);
```

### Testing
To verify F8 now works for prev-team:
1. Press F8 in Pi
2. Should cycle to **previous** team (not next)
3. F6 still cycles to **next** team
