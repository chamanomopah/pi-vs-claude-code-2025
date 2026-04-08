# Agent Teams - Visual Troubleshooting Guide

## The Problem at a Glance

```
┌─────────────────────────────────────────────────────────────┐
│  AGENT TEAMS EXTENSION                                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  .pi/agents/                                                 │
│  ├── scout.md          ────┐                                 │
│  ├── builder.md        ────┤                                 │
│  ├── reviewer.md       ────┤                                 │
│  └── tester.md         ────┤                                 │
│                             │                                │
│                             ▼                                │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ teams.yaml                                           │    │
│  │ all:                                                 │    │
│  │   - scout       ✓ HAS SKILLS?  NO  ─────────┐       │    │
│  │   - builder     ✓ HAS SKILLS?  YES ──────────┤       │    │
│  │   - reviewer    ✓ HAS SKILLS?  NO  ─────────┤       │    │
│  │   - tester      ✓ HAS SKILLS?  NO  ─────────┤       │    │
│  └──────────────────────────────────────────────┼───────┘    │
│                                                 │           │
│                                                 ▼           │
│                              ┌─────────────────────────┐   │
│                              │ SKILLS FILTER (Line 461)│   │
│                              │ .filter(s =>            │   │
│                              │   s.def.skills.length>0)│   │
│                              └──────────┬──────────────┘   │
│                                         │                  │
│                         ┌───────────────┴───────────────┐ │
│                         ▼                               ▼ │
│                   ┌─────────────┐               ┌──────────────┐
│                   │   VISIBLE   │               │   HIDDEN     │
│                   │   (1 agent) │               │  (3 agents)  │
│                   └─────────────┘               └──────────────┘
│                         │                              │
│                         ▼                              ▼
│              ✓ dispatch_agent works          ✗ "Agent not found"
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

## The 3 Solutions Visualized

```
┌──────────────────────────────────────────────────────────────────┐
│ SOLUTION COMPARISON                                              │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  Solution A: Remove Filter                    Solution B: Add    │
│  ───────────────────────                    Skills to Agents    │
│                                                                   │
│  scout.md    ──┐                           scout.md:            │
│  builder.md   ├──┐  FILTER REMOVED         skills: []           │
│  reviewer.md  ──┼──┼───────────────────►  builder.md:          │
│  tester.md    ──┘  │  ALL AGENTS VISIBLE   skills: [5-min]      │
│                  │  │                       reviewer.md:         │
│                  └──┼──► 4/4 agents          skills: []          │
│                     │                        tester.md:          │
│                     ▼                        skills: []          │
│              ┌─────────────┐                                    │
│              │   VISIBLE   │                                    │
│              │  (4 agents) │                                    │
│              └─────────────┘                                    │
│                                                                   │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  Solution C: Environment Variable (RECOMMENDED)                  │
│  ─────────────────────────────────                               │
│                                                                   │
│  PI_REQUIRE_SKILLS=false    │    PI_REQUIRE_SKILLS=true          │
│  ────────────────────────   │    ────────────────────────       │
│  Filter DISABLED            │    Filter ENABLED (default)        │
│  │                          │    │                               │
│  ▼                          │    ▼                               │
│  ALL AGENTS VISIBLE         │    ONLY SKILLED AGENTS VISIBLE     │
│  (4/4 agents)              │    (1/4 agents)                    │
│                             │                                     │
└──────────────────────────────────────────────────────────────────┘
```

---

## Code Change Visualization

### Current Code (Has the Problem)

```typescript
// Line 461 in agent-team.ts
const agentCatalog = Array.from(agentStates.values())
    .filter(s => s.def.skills.length > 0)  // ⚠️ PROBLEM HERE
    .map(s => `### ${displayName(s.def.name)}...
               **Skills:** ${s.def.skills.join(", ")}`)
    .join("\n\n");

// Result: Only "builder" shows (has skills)
// scout, reviewer, tester: HIDDEN ❌
```

### Solution A: Remove Filter

```typescript
const agentCatalog = Array.from(agentStates.values())
    // .filter(s => s.def.skills.length > 0)  // ✅ REMOVED
    .map(s => {
        const skills = s.def.skills.length > 0
            ? `\n**Skills:** ${s.def.skills.join(", ")}`
            : "";  // ✅ Empty for no-skill agents
        return `### ${displayName(s.def.name)}...${skills}`;
    })
    .join("\n\n");

// Result: All agents show ✓
```

### Solution C: Make Configurable

```typescript
// Add at top (line 23)
const REQUIRE_SKILLS_FOR_DISPATCH = process.env.PI_REQUIRE_SKILLS !== "false";

// In before_agent_start
const agentCatalog = Array.from(agentStates.values())
    .filter(s => !REQUIRE_SKILLS_FOR_DISPATCH || s.def.skills.length > 0)  // ✅ CONFIGURABLE
    .map(s => { /* ... */ })
    .join("\n\n");

// PI_REQUIRE_SKILLS=false → All agents show ✓
// PI_REQUIRE_SKILLS=true  → Only skilled agents show ✓
```

---

## Agent File Examples

### Without Skills (Hidden by default)

```markdown
---
name: scout
description: Reconhecimento rápido
tools: read,grep,find,ls
---
```

### With Empty Skills Array

```markdown
---
name: scout
description: Reconhecimento rápido
tools: read,grep,find,ls
skills: []     ← Shows when filter disabled
---
```

### With Real Skills

```markdown
---
name: builder
description: Constrói código
tools: read,write,edit
skills:        ← Always visible
  - 5-min-scripts
  - code-gen
---
```

---

## Decision Tree

```
                    Need to fix agent visibility?
                             │
                    ┌────────┴────────┐
                    │                 │
              Want to modify       Want to keep
              code?               code minimal?
                    │                 │
                    │            ┌────┴────┐
                    │            │         │
              ┌────┴────┐   Can modify   Use
          Quick fix    Full    agent      environment
    (remove filter)  control  files?    variable?
          │            │       │         │
          │            │    ┌───┴───┐    │
    Solution A    Solution C  Yes   No  Solution C
 (2 min fix)   (flexible)  │     │  (best)
                  │        │     │
                  │        ▼     ▼
                  │    Solution B  Solution C/A
                  │  (add skills)
                  │
            RECOMMENDED
```

---

## Quick Reference Card

```
┌─────────────────────────────────────────────────────────────┐
│  AGENT TEAMS QUICK FIX                                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  SYMPTOM:  Agent "not found" when dispatching              │
│  CAUSE:   Missing skills field → filtered by extension     │
│                                                             │
│  FASTEST FIX (2 min):                                       │
│  1. Edit extensions/agent-team.ts line 461                 │
│  2. Remove .filter() line                                   │
│  3. Add conditional skills display                          │
│  4. Restart pi                                              │
│                                                             │
│  BEST FIX (5 min):                                          │
│  1. Add config constant (line 23)                           │
│  2. Modify filter to be conditional                        │
│  3. Use: PI_REQUIRE_SKILLS=false pi -e agent-team.ts       │
│                                                             │
│  ALTERNATIVE (no code):                                     │
│  Add "skills: []" to every agent file                       │
│                                                             │
│  VERIFY:                                                    │
│  /agents-list → Shows all team members                     │
│  dispatch_agent → Works for all agents                     │
│                                                             │
│  📚 Full docs: docs/AGENT_TEAMS_INDEX.md                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## File Location Map

```
project-root/
│
├── extensions/
│   └── agent-team.ts          ← EDIT THIS for solutions A/C
│                              Lines 23 (add config)
│                              Lines 461-475 (fix filter)
│
├── .pi/
│   ├── agents/
│   │   ├── teams.yaml         ← Check agent names here
│   │   │
│   │   ├── scout.md           ← Add skills: [] for solution B
│   │   ├── builder.md         ← Already has skills
│   │   ├── reviewer.md        ← Add skills: [] for solution B
│   │   └── tester.md          ← Add skills: [] for solution B
│   │
│   └── skills/                ← Skills referenced by agents
│       └── 5-min-scripts/
│
└── docs/
    ├── AGENT_TEAMS_INDEX.md              ← Start here
    ├── agent-teams-quick-fix.md          ← 2-minute fix
    ├── agent-teams-troubleshooting.md    ← Full guide
    ├── agent-teams-solution-examples.md  ← Code examples
    └── agent-teams-visual-guide.md       ← This file
```

---

## Verification Checklist

```
After applying any solution, verify:

☐ Start pi: pi -e extensions/agent-team.ts
☐ Check notification shows all team members
☐ Run: /agents-list
☐ See all agents in list
☐ Test: Use dispatch_agent to send "test" to <agent>
☐ Agent executes successfully
☐ No "Agent not found" errors
☐ Check system prompt: Show me your system prompt
☐ All team members in "## Agents" section
```

---

For complete implementation details, see:
- **[Quick Fix Guide](./agent-teams-quick-fix.md)** - Fastest path to solution
- **[Troubleshooting Guide](./agent-teams-troubleshooting.md)** - In-depth explanation
- **[Solution Examples](./agent-teams-solution-examples.md)** - Copy-paste code
