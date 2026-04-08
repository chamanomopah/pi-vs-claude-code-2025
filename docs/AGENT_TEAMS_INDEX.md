# Agent Teams Documentation Index

Complete guide for the Agent Teams extension (`pi -e extensions/agent-team.ts`).

## 🚨 Issue Fix: Agents Not Appearing in Dispatch List

**If agents don't appear when dispatching, start here:**

1. **[Quick Fix Guide](./agent-teams-quick-fix.md)** ⚡
   - Fastest path to resolution
   - 3 solution options at a glance
   - Verification steps

2. **[Complete Troubleshooting Guide](./agent-teams-troubleshooting.md)** 📖
   - Detailed problem analysis
   - Root cause explanation
   - Pros/cons of each solution
   - How to add skills to agents
   - Best practices and recommendations

3. **[Solution Implementation Examples](./agent-teams-solution-examples.md)** 💻
   - Copy-paste ready code changes
   - Batch update scripts
   - Testing procedures
   - Common issues and fixes

---

## Overview

### The Problem
The Agent Teams extension filters agents to only show those with a `skills:` field in their frontmatter. This means:
- ✅ Agents **with** `skills:` field appear in dispatch list
- ❌ Agents **without** `skills:` field are hidden from dispatcher
- 🤔 They still show in the grid dashboard but can't be dispatched

### Root Cause
```typescript
// Line 461 in agent-team.ts
const agentCatalog = Array.from(agentStates.values())
    .filter(s => s.def.skills.length > 0)  // ← This hides agents without skills
    .map(s => ...);
```

### The 3 Solutions

| Solution | What It Does | When to Use |
|----------|--------------|-------------|
| **A. Remove filter** | Show all agents regardless of skills | Small teams, quick fix |
| **B. Add skills** | Add `skills: []` to every agent | Want explicit tracking |
| **C. Env variable** | `PI_REQUIRE_SKILLS=false` to toggle | Production, flexibility |

**Recommendation:** Use Solution C (environment variable) for maximum flexibility.

---

## Quick Start

### Fastest Fix (2 minutes)

**1. Edit `extensions/agent-team.ts`** (line ~461):

```typescript
// Remove the .filter() line:
const agentCatalog = Array.from(agentStates.values())
    // .filter(s => s.def.skills.length > 0)  // ← REMOVE
    .map(s => {
        const skills = s.def.skills.length > 0
            ? `\n**Skills:** ${s.def.skills.join(", ")}`
            : "";
        return `### ${displayName(s.def.name)}\n**Dispatch as:** \`${s.def.name}\`\n${s.def.description}${skills}`;
    })
    .join("\n\n");
```

```typescript
// Also update line ~469:
const teamMembers = Array.from(agentStates.values()).map(s => displayName(s.def.name)).join(", ");
```

**2. Restart pi:**
```bash
pi -e extensions/agent-team.ts
```

✅ **Done!** See [Quick Fix Guide](./agent-teams-quick-fix.md) for details.

---

## How to Add Skills to Agents

If you want to assign skills to an agent, add the `skills:` field to frontmatter:

```yaml
---
name: my-agent
description: Does cool stuff
tools: read,grep,find,ls
skills:
  - skill-name
  - another-skill
---
```

**Formats supported:**
- Array: `skills:\n  - skill1\n  - skill2`
- Comma-separated: `skills: skill1, skill2`
- Single: `skills: skill1`
- Empty: `skills: []`

See [Solution Examples](./agent-teams-solution-examples.md) for complete examples.

---

## File Locations

```
project-root/
├── extensions/
│   └── agent-team.ts          # Extension code (edit for solutions A/C)
├── .pi/
│   └── agents/
│       ├── teams.yaml         # Team definitions
│       ├── scout.md           # Agent definitions
│       ├── builder.md
│       └── ...
└── docs/
    ├── agent-teams-quick-fix.md           # Start here
    ├── agent-teams-troubleshooting.md     # Full guide
    └── agent-teams-solution-examples.md   # Code examples
```

---

## Verification Commands

```bash
# List all loaded agents
/agents-list

# Switch active team
/agents-team

# Set grid columns
/agents-grid 3

# Reload agents after changes
/agent-team-reload

# Check which agents dispatcher sees
Show me your system prompt
# Look for "## Agents" section
```

---

## Related Documentation

### Agent Teams
- **[Quick Fix Guide](./agent-teams-quick-fix.md)** - Start here for fast resolution
- **[Complete Troubleshooting](./agent-teams-troubleshooting.md)** - In-depth analysis
- **[Solution Examples](./agent-teams-solution-examples.md)** - Copy-paste code

### General
- **[Quick Reference](./QUICK_REFERENCE.md)** - Common commands
- **[Best Practices](./BEST_PRACTICES.md)** - Usage guidelines
- **[Skills Guide](./HOW_TO_USE_SKILLS.md)** - How skills work

---

## FAQ

**Q: Why does this filter exist?**
A: To maintain a "specialist agent" paradigm where only agents with specific loaded skills are available.

**Q: Which solution should I use?**
A: Solution C (environment variable) offers the most flexibility without modifying agent files.

**Q: Will this break my existing setup?**
A: No. All solutions are backwards compatible. Agents with skills still show them.

**Q: Can I toggle the filter at runtime?**
A: Only with Solution C. Set `PI_REQUIRE_SKILLS=false` before starting pi.

**Q: Do I need to restart pi after changes?**
A: Yes. Agent definitions are loaded at session start. Use `/agent-team-reload` to reload without full restart.

---

## Support

If issues persist after trying these solutions:

1. Verify agent file format: `head -10 .pi/agents/your-agent.md`
2. Check teams.yaml: `cat .pi/agents/teams.yaml`
3. Look for syntax errors: `pi -e extensions/agent-team.ts 2>&1 | head -20`
4. Try minimal test: Create simple agent with `skills: []`

---

**Last Updated:** 2026-04-08
**Extension Version:** agent-team.ts (current)
**Pi Version:** Latest from pi-mono/main
