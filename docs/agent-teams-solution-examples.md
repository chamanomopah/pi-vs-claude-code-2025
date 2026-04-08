# Agent Teams - Solution Implementation Examples

This file provides copy-paste ready code changes for each solution described in [agent-teams-troubleshooting.md](./agent-teams-troubleshooting.md).

---

## Solution 1: Remove Skills Filter

**File:** `extensions/agent-team.ts`
**Location:** Lines 461-475 in `before_agent_start` event handler

### Find This Code:
```typescript
// Build dynamic agent catalog from active team only
// Include skills for agents that have them
const agentCatalog = Array.from(agentStates.values())
    .filter(s => s.def.skills.length > 0)  // Only show agents with skills
    .map(s => `### ${displayName(s.def.name)}\n**Dispatch as:** \`${s.def.name}\`\n${s.def.description}\n**Skills:** ${s.def.skills.join(", ")}`)
    .join("\n\n");

const agentsWithSkills = Array.from(agentStates.values()).filter(s => s.def.skills.length > 0);
const teamMembers = agentsWithSkills.map(s => displayName(s.def.name)).join(", ");
```

### Replace With:
```typescript
// Build dynamic agent catalog from active team only
// Include skills for agents that have them
const agentCatalog = Array.from(agentStates.values())
    // .filter(s => s.def.skills.length > 0)  // REMOVED: Show all agents, not just those with skills
    .map(s => {
        const skills = s.def.skills.length > 0
            ? `\n**Skills:** ${s.def.skills.join(", ")}`
            : "";
        return `### ${displayName(s.def.name)}\n**Dispatch as:** \`${s.def.name}\`\n${s.def.description}${skills}`;
    })
    .join("\n\n");

// Show all team members in the list
const teamMembers = Array.from(agentStates.values()).map(s => displayName(s.def.name)).join(", ");
```

---

## Solution 2: Add Skills to Agent Files

### Example 1: Agent with Empty Skills Array

**File:** `.pi/agents/scout.md`

```markdown
---
name: scout
description: Reconhecimento rápido e exploração de codebase
tools: read,grep,find,ls
skills: []
---

Você é um agente de reconhecimento. Investigue o codebase rapidamente e reporte descobertas de forma concisa. NÃO modifique nenhum arquivo. Foque na estrutura, padrões e pontos de entrada chave.
```

### Example 2: Agent with Generic Skill

**File:** `.pi/agents/reviewer.md`

```markdown
---
name: reviewer
description: Revisão de código e boas práticas
tools: read,grep,find,ls
skills:
  - code-review
---

Você é um agente revisor. Analise o código em busca de bugs, problemas de segurança e violações de boas práticas.
```

### Example 3: Agent with Multiple Skills

**File:** `.pi/agents/builder.md`

```markdown
---
name: builder
description: Implementação e geração de código
tools: read,write,edit,bash,grep,find,ls
skills:
  - 5-min-scripts
  - code-generation
  - testing
---

Você é um agente construtor. Implemente as mudanças solicitadas completamente. Escreva código limpo e minimal.
```

### Batch Update Script

To add `skills: []` to all agents that don't have a skills field:

```bash
#!/bin/bash
# add-skills-field.sh

for file in .pi/agents/*.md; do
    # Check if file already has skills field
    if ! grep -q "^skills:" "$file"; then
        # Add skills: [] after the tools: line
        sed -i '/^tools:/a skills: []' "$file"
        echo "Updated: $file"
    else
        echo "Skipped (has skills): $file"
    fi
done
```

---

## Solution 3: Configurable Skills Filter (Recommended)

### Step 1: Add Configuration Constant

**File:** `extensions/agent-team.ts`
**Location:** After imports (around line 23)

**Add this code:**
```typescript
// ── Configuration ───────────────────────────────

// Set PI_REQUIRE_SKILLS=false to allow ALL agents for dispatch (not just those with skills)
// Default: true (only agents with skills appear in dispatcher list)
const REQUIRE_SKILLS_FOR_DISPATCH = process.env.PI_REQUIRE_SKILLS !== "false";
```

### Step 2: Update before_agent_start Handler

**File:** `extensions/agent-team.ts`
**Location:** Lines 461-475 in `before_agent_start` event handler

**Find this code:**
```typescript
// Build dynamic agent catalog from active team only
// Include skills for agents that have them
const agentCatalog = Array.from(agentStates.values())
    .filter(s => s.def.skills.length > 0)  // Only show agents with skills
    .map(s => `### ${displayName(s.def.name)}\n**Dispatch as:** \`${s.def.name}\`\n${s.def.description}\n**Skills:** ${s.def.skills.join(", ")}`)
    .join("\n\n");

const agentsWithSkills = Array.from(agentStates.values()).filter(s => s.def.skills.length > 0);
const teamMembers = agentsWithSkills.map(s => displayName(s.def.name)).join(", ");
```

**Replace with:**
```typescript
// Build dynamic agent catalog from active team only
// Include skills for agents that have them
// Filter behavior controlled by REQUIRE_SKILLS_FOR_DISPATCH
const agentCatalog = Array.from(agentStates.values())
    .filter(s => !REQUIRE_SKILLS_FOR_DISPATCH || s.def.skills.length > 0)
    .map(s => {
        const skills = s.def.skills.length > 0
            ? `\n**Skills:** ${s.def.skills.join(", ")}`
            : "";
        return `### ${displayName(s.def.name)}\n**Dispatch as:** \`${s.def.name}\`\n${s.def.description}${skills}`;
    })
    .join("\n\n");

// Show team members based on filter setting
const agentsWithSkills = Array.from(agentStates.values())
    .filter(s => !REQUIRE_SKILLS_FOR_DISPATCH || s.def.skills.length > 0);
const teamMembers = agentsWithSkills.map(s => displayName(s.def.name)).join(", ");
```

### Step 3: Usage

**Default mode (require skills):**
```bash
pi -e extensions/agent-team.ts
# Only agents with skills field will be available for dispatch
```

**Allow all agents:**
```bash
PI_REQUIRE_SKILLS=false pi -e extensions/agent-team.ts
# All team members available for dispatch
```

**Set as alias (bash/zsh):**
```bash
# Add to ~/.bashrc or ~/.zshrc
alias pi-all='PI_REQUIRE_SKILLS=false pi -e extensions/agent-team.ts'
alias pi-team='pi -e extensions/agent-team.ts'

# Usage:
pi-all    # All agents available
pi-team   # Only skilled agents
```

**Windows PowerShell:**
```powershell
# Add to $PROFILE
Set-Content -Path function:\pi-all -Value { $env:PI_REQUIRE_SKILLS = "false"; pi -e extensions/agent-team.ts }
Set-Content -Path function:\pi-team -Value { Remove-Item Env:PI_REQUIRE_SKILLS -ErrorAction SilentlyContinue; pi -e extensions/agent-team.ts }
```

---

## Testing Your Changes

### Test Script 1: Verify Agent Visibility

```bash
#!/bin/bash
# test-visibility.sh

echo "=== Testing Agent Visibility ==="
echo ""

# Start pi and check which agents appear
pi -e extensions/agent-team.ts << 'EOF' &
PID=$!
sleep 2
kill $PID 2>/dev/null
EOF

echo "Check the notification message - it should show all team members"
echo "Run /agents-list to see all loaded agents"
```

### Test Script 2: Dispatch Test

```
# After starting pi, test dispatch with:

Use dispatch_agent to send "List the files in current directory" to scout

# Expected: scout executes the task
# Error: "Agent scout not found" indicates the filter is still active
```

### Test Script 3: System Prompt Check

```
# In pi, check the system prompt:
Show me your system prompt

# Look for the "## Agents" section
# Verify that all team members are listed
```

---

## Quick Reference

### Filter Behavior Comparison

| Mode | REQUIRE_SKILLS | Agents Shown | Use Case |
|------|----------------|--------------|----------|
| Specialist | `true` or unset | Only agents with `skills:` | Production, expert teams |
| All Agents | `false` | All team members | Development, mixed teams |

### Agent Frontmatter Examples

| Agent Type | Skills Field | Visible When |
|------------|--------------|--------------|
| Specialist | `skills: [skill1, skill2]` | Always |
| Generic | `skills: []` | All-agents mode only |
| No field | (missing) | All-agents mode only |
| Generic single | `skills: generic` | Always |

---

## Troubleshooting Common Issues

### Issue: Changes not taking effect

**Solution:** Restart pi completely
```bash
# Kill any running pi instances
pkill -f pi

# Start fresh
pi -e extensions/agent-team.ts
```

### Issue: Environment variable not working

**Solution:** Check variable is set before starting pi
```bash
# Verify
echo $PI_REQUIRE_SKILLS

# Set explicitly for this session
export PI_REQUIRE_SKILLS=false
pi -e extensions/agent-team.ts

# Or one-shot
PI_REQUIRE_SKILLS=false pi -e extensions/agent-team.ts
```

### Issue: Agent still not showing

**Possible causes:**
1. Agent not in active team (check `.pi/agents/teams.yaml`)
2. Agent name mismatch (case-sensitive in teams.yaml)
3. Syntax error in agent frontmatter
4. Agent file not in `.pi/agents/` directory

**Debug:**
```bash
# List all agent files found
ls -la .pi/agents/*.md

# Check teams.yaml
cat .pi/agents/teams.yaml

# Use /agents-list in pi to see loaded agents
```

---

## Related Documentation

- [Agent Teams Troubleshooting](./agent-teams-troubleshooting.md) - Full problem description
- [Skills Implementation Guide](./HOW_TO_USE_SKILLS.md) - How skills work
- [Quick Reference](./QUICK_REFERENCE.md) - Common commands and patterns
