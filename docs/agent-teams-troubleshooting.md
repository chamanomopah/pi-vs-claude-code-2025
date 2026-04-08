# Agent Teams - Troubleshooting Guide

## Problem: Agents Not Appearing in Dispatch List

### Symptoms
When using the Agent Teams extension (`pi -e extensions/agent-team.ts`), some agents may not appear in the dispatcher's available agents list, even though they are:
- Defined in `.pi/agents/*.md` files
- Listed in `.pi/agents/teams.yaml`
- Visible in the grid dashboard

### Root Cause
The `before_agent_start` event handler filters the agent catalog to **only show agents with skills**:

```typescript
// Line 461-465 in agent-team.ts
const agentCatalog = Array.from(agentStates.values())
    .filter(s => s.def.skills.length > 0)  // ⚠️ This filters out agents without skills
    .map(s => `### ${displayName(s.def.name)}\n**Dispatch as:** \`${s.def.name}\`\n${s.def.description}\n**Skills:** ${s.def.skills.join(", ")}`)
    .join("\n\n");
```

This means agents without a `skills:` field in their frontmatter won't appear in the system prompt, making them unavailable for dispatch.

---

## Solution Options

### Solution 1: Remove the Skills Filter (Easiest)

**Description:** Remove the `.filter()` call so all team members appear in the catalog, regardless of whether they have skills.

**Implementation:**
```typescript
// In before_agent_start event handler (line 461-465)
const agentCatalog = Array.from(agentStates.values())
    // .filter(s => s.def.skills.length > 0)  // ← Remove this line
    .map(s => {
        const skills = s.def.skills.length > 0
            ? `\n**Skills:** ${s.def.skills.join(", ")}`
            : "";
        return `### ${displayName(s.def.name)}\n**Dispatch as:** \`${s.def.name}\`\n${s.def.description}${skills}`;
    })
    .join("\n\n");
```

**Pros:**
- ✅ Simplest change (single line removal + minor logic update)
- ✅ All agents immediately available
- ✅ No need to modify agent files
- ✅ Backwards compatible - agents with skills still show them

**Cons:**
- ❌ Loses the "specialist" semantic (agents without skills can still be dispatched)
- ❌ May clutter the catalog if you have many generic agents

---

### Solution 2: Add Empty Skills Field to All Agents

**Description:** Add a `skills: []` or `skills: generic` field to every agent's frontmatter.

**Implementation:**

For agents without specific skills:
```yaml
---
name: scout
description: Reconhecimento rápido e exploração de codebase
tools: read,grep,find,ls
skills: []
---
```

Or give them a generic skill:
```yaml
---
name: scout
description: Reconhecimento rápido e exploração de codebase
tools: read,grep,find,ls
skills:
  - generic
---
```

**Pros:**
- ✅ No code changes required
- ✅ Maintains the specialist-only semantic
- ✅ Explicit about which agents have specialized capabilities

**Cons:**
- ❌ Requires editing every agent file (tedious for many agents)
- ❌ `skills: []` feels redundant when agents don't need skills
- ❌ Ongoing maintenance burden for new agents

---

### Solution 3: Make Skills Filter Optional (Recommended)

**Description:** Add a configuration option to control whether the skills filter is applied. This gives you flexibility via environment or config.

**Implementation:**

1. Add a config variable at the top of the extension:
```typescript
// After imports (line ~23)
const REQUIRE_SKILLS_FOR_DISPATCH = process.env.PI_REQUIRE_SKILLS !== "false";
```

2. Modify the filter logic:
```typescript
// In before_agent_start event handler
const agentCatalog = Array.from(agentStates.values())
    .filter(s => !REQUIRE_SKILLS_FOR_DISPATCH || s.def.skills.length > 0)
    .map(s => {
        const skills = s.def.skills.length > 0
            ? `\n**Skills:** ${s.def.skills.join(", ")}`
            : "";
        return `### ${displayName(s.def.name)}\n**Dispatch as:** \`${s.def.name}\`\n${s.def.description}${skills}`;
    })
    .join("\n\n");
```

3. Update the team members display:
```typescript
const agentsWithSkills = Array.from(agentStates.values())
    .filter(s => !REQUIRE_SKILLS_FOR_DISPATCH || s.def.skills.length > 0);
const teamMembers = agentsWithSkills.map(s => displayName(s.def.name)).join(", ");
```

**Usage:**
```bash
# Require skills (default - only specialists shown)
pi -e extensions/agent-team.ts

# Allow all agents (regardless of skills)
PI_REQUIRE_SKILLS=false pi -e extensions/agent-team.ts
```

**Pros:**
- ✅ Best of both worlds - configurable behavior
- ✅ Can switch modes per session
- ✅ No need to modify agent files
- ✅ Clear intent via environment variable

**Cons:**
- ❌ Slightly more complex code
- ❌ Requires setting environment variable to change behavior

---

## How to Add Skills to Agent Files

If you want to assign skills to an agent, add a `skills:` field to the YAML frontmatter:

### Format Options

**1. YAML Array (Recommended for multiple skills):**
```yaml
---
name: builder
description: Implementação e geração de código
tools: read,write,edit,gash,grep,find,ls
skills:
  - 5-min-scripts
  - code-generation
---
```

**2. Comma-separated string:**
```yaml
---
name: builder
description: Implementação e geração de código
tools: read,write,edit,bash,grep,find,ls
skills: 5-min-scripts, code-generation
---
```

**3. Single skill:**
```yaml
---
name: tester
description: Testes e validação
tools: read,grep,find,ls,bash
skills: testing
---
```

**4. Empty array (agent has no special skills):**
```yaml
---
name: scout
description: Reconhecimento rápido
tools: read,grep,find,ls
skills: []
---
```

### Complete Example

```markdown
---
name: n8n-builder
description: Especialista em criar workflows N8N automatizados
tools: read,grep,find,ls,write,edit
skills:
  - n8n-claude-workflow-builder
  - workflow-design
---

Você é um especialista em criar workflows N8N usando Claude Code CLI. 
Crie workflows complexos com múltiplos agentes e automação.
```

---

## Recommendation

**Use Solution 3 (Configurable Filter)** for the following reasons:

1. **Flexibility:** Different projects may have different needs
2. **No Breaking Changes:** Existing behavior preserved by default
3. **Future-Proof:** Easy to adapt as your agent ecosystem evolves
4. **Clean Code:** Minimal code complexity for maximum flexibility

For most users, the environment variable `PI_REQUIRE_SKILLS=false` provides a quick way to include all agents without modifying any files.

---

## Quick Fix Commands

### Apply Solution 1 (Remove Filter)
```bash
# Edit agent-team.ts and remove the .filter() line
# Then restart pi
pi -e extensions/agent-team.ts
```

### Apply Solution 3 (Configurable)
```bash
# Add the config constant and modify filter as shown above
# Run with all agents visible:
PI_REQUIRE_SKILLS=false pi -e extensions/agent-team.ts

# Run with only skilled agents:
pi -e extensions/agent-team.ts
```

### Apply Solution 2 (Add Skills to Agents)
```bash
# Add skills field to each agent file
# Example for scout:
cat > .pi/agents/scout.md << 'EOF'
---
name: scout
description: Reconhecimento rápido e exploração de codebase
tools: read,grep,find,ls
skills: []
---
Você é um agente de reconhecimento...
EOF
```

---

## Verification

After applying any solution, verify it works:

1. **Start the extension:**
   ```bash
   pi -e extensions/agent-team.ts
   ```

2. **Check the notification** - it should show all team members

3. **List agents:**
   ```
   /agents-list
   ```

4. **Test dispatch:**
   ```
   Use dispatch_agent to send "hello" to scout
   ```

5. **Check system prompt** (if using Solution 1 or 3 with filter disabled):
   - All team members should appear in the "## Agents" section
   - Agents with skills show `**Skills:** ...` field
   - Agents without skills don't show the skills field

---

## Related Files

- **Extension:** `extensions/agent-team.ts` (lines 461-475)
- **Teams config:** `.pi/agents/teams.yaml`
- **Agent definitions:** `.pi/agents/*.md`
- **Skills directory:** `.pi/skills/*/`

---

## Additional Notes

### Why the Filter Exists
The skills filter was added to maintain a "specialist agent" paradigm where only agents with specific, loaded skills should be available for dispatch. This prevents cluttering the dispatcher with generic utility agents.

### When to Use Each Solution

- **Solution 1 (Remove filter):** Small teams, few agents, or when all agents are truly specialists
- **Solution 2 (Add skills):** When you want to explicitly track which agents have capabilities
- **Solution 3 (Configurable):** Production environments, varying team sizes, or when you want flexibility

### Future Improvements
Consider these enhancements for the Agent Teams extension:
1. Add a `/agents-filter` command to toggle the filter at runtime
2. Support skill inheritance (base skills + agent-specific skills)
3. Show agent status (idle/running/error) in the system prompt catalog
4. Add skill discovery from `.pi/skills/` directory automatically
