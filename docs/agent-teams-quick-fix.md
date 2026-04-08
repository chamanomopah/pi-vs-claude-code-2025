# Agent Teams - Quick Fix Guide

## 🚨 Problem: Agents Missing from Dispatch List

**Symptom:** You run `/agents-list` and see agents in the grid, but the dispatcher says "Agent not found" when you try to use them.

**Cause:** Agent Teams extension only shows agents with `skills:` field in their frontmatter.

---

## ⚡ Quick Fixes

### Option A: Disable Skills Filter (Recommended - Fastest)

**1. Edit `extensions/agent-team.ts`:**

```typescript
// Around line 461, find this:
const agentCatalog = Array.from(agentStates.values())
    .filter(s => s.def.skills.length > 0)  // ← REMOVE THIS LINE
    .map(s => ...);

// Change to:
const agentCatalog = Array.from(agentStates.values())
    .map(s => {
        const skills = s.def.skills.length > 0
            ? `\n**Skills:** ${s.def.skills.join(", ")}`
            : "";
        return `### ${displayName(s.def.name)}\n**Dispatch as:** \`${s.def.name}\`\n${s.def.description}${skills}`;
    })
    .join("\n\n");
```

```typescript
// Around line 469, find this:
const agentsWithSkills = Array.from(agentStates.values()).filter(s => s.def.skills.length > 0);
const teamMembers = agentsWithSkills.map(s => displayName(s.def.name)).join(", ");

// Change to:
const teamMembers = Array.from(agentStates.values()).map(s => displayName(s.def.name)).join(", ");
```

**2. Restart pi:**
```bash
pi -e extensions/agent-team.ts
```

✅ **Done!** All agents now available.

---

### Option B: Add Skills to Agents (No Code Changes)

Add `skills: []` to each agent that's missing:

**Example for `.pi/agents/scout.md`:**
```yaml
---
name: scout
description: Reconhecimento rápido
tools: read,grep,find,ls
skills: []      # ← ADD THIS
---
```

**Or give them actual skills:**
```yaml
---
name: builder
description: Build stuff
tools: read,write,edit
skills:        # ← ADD THIS
  - 5-min-scripts
  - code-gen
---
```

---

### Option C: Use Environment Variable (Flexible)

**1. Edit `extensions/agent-team.ts`** (after imports, ~line 23):

```typescript
// Add this constant
const REQUIRE_SKILLS_FOR_DISPATCH = process.env.PI_REQUIRE_SKILLS !== "false";
```

**2. Update filter** (around line 461):

```typescript
const agentCatalog = Array.from(agentStates.values())
    .filter(s => !REQUIRE_SKILLS_FOR_DISPATCH || s.def.skills.length > 0)
    .map(s => {
        const skills = s.def.skills.length > 0
            ? `\n**Skills:** ${s.def.skills.join(", ")}`
            : "";
        return `### ${displayName(s.def.name)}\n**Dispatch as:** \`${s.def.name}\`\n${s.def.description}${skills}`;
    })
    .join("\n\n");

const agentsWithSkills = Array.from(agentStates.values())
    .filter(s => !REQUIRE_SKILLS_FOR_DISPATCH || s.def.skills.length > 0);
const teamMembers = agentsWithSkills.map(s => displayName(s.def.name)).join(", ");
```

**3. Use it:**
```bash
# All agents available
PI_REQUIRE_SKILLS=false pi -e extensions/agent-team.ts

# Only skilled agents (default)
pi -e extensions/agent-team.ts
```

---

## 📊 Comparison Table

| Solution | Time to Fix | Code Changes | Agent Changes | Flexibility |
|----------|-------------|--------------|---------------|-------------|
| **A. Remove filter** | 2 min | Yes | No | ⭐⭐⭐ |
| **B. Add skills** | 5-10 min | No | Yes (all agents) | ⭐ |
| **C. Env variable** | 5 min | Yes | No | ⭐⭐⭐⭐⭐ |

---

## ✅ Verification

After applying any fix:

```bash
# 1. Start pi
pi -e extensions/agent-team.ts

# 2. Check notification shows all team members

# 3. Run command
/agents-list

# 4. Test dispatch
Use dispatch_agent to send "hello" to scout
```

**Expected:** Agent executes successfully without "not found" error.

---

## 🔍 Debug

If agents still don't appear:

```bash
# Check agent files exist
ls .pi/agents/*.md

# Check teams.yaml includes them
cat .pi/agents/teams.yaml

# Verify frontmatter format
head -5 .pi/agents/scout.md
```

Common issues:
- Agent not listed in `.pi/agents/teams.yaml`
- Name mismatch (teams.yaml is case-sensitive)
- Invalid YAML frontmatter
- Agent file in wrong directory

---

## 📚 Full Documentation

- [Complete Troubleshooting Guide](./agent-teams-troubleshooting.md)
- [Solution Examples](./agent-teams-solution-examples.md)
