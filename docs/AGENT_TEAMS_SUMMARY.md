# Agent Teams Issue - Executive Summary

## TL;DR

**Problem:** Agent Teams extension hides agents without `skills:` field from the dispatch list.
**Fix:** Remove the filter or add `skills: []` to agent files.
**Time:** 2-5 minutes.
**Impact:** All team members become available for dispatch.

---

## The Issue in One Paragraph

The `agent-team.ts` extension filters the agent catalog at line 461 to only show agents with a `skills:` field in their YAML frontmatter. This means agents like `scout`, `reviewer`, or `tester` that don't have specialized skills won't appear in the dispatcher's system prompt, causing "Agent not found" errors when you try to use them—even though they're visible in the grid dashboard and listed in `teams.yaml`.

---

## The Numbers

| Metric | Value |
|--------|-------|
| **Code to change** | 1 file (agent-team.ts) |
| **Lines to edit** | ~15 lines |
| **Time to fix** | 2-5 minutes |
| **Affected agents** | Those without `skills:` field |
| **Difficulty level** | Easy |
| **Risk** | None (backwards compatible) |

---

## Recommended Solution

**Solution C: Configurable Filter** (5 minutes)

Add an environment variable toggle that lets you choose whether to filter by skills:

```typescript
// Add after imports (line ~23)
const REQUIRE_SKILLS_FOR_DISPATCH = process.env.PI_REQUIRE_SKILLS !== "false";
```

```typescript
// Update filter (line ~461)
const agentCatalog = Array.from(agentStates.values())
    .filter(s => !REQUIRE_SKILLS_FOR_DISPATCH || s.def.skills.length > 0)
    // ... rest of code
```

**Usage:**
```bash
# Show all agents
PI_REQUIRE_SKILLS=false pi -e extensions/agent-team.ts

# Show only skilled agents (default)
pi -e extensions/agent-team.ts
```

**Why this solution:**
- ✅ No breaking changes
- ✅ Toggle per session
- ✅ No agent file modifications
- ✅ Production-ready

---

## Alternative: Quick Fix (2 minutes)

Just remove the filter:

```typescript
// Line 461 - remove this line:
// .filter(s => s.def.skills.length > 0)

// And update the map to handle empty skills:
.map(s => {
    const skills = s.def.skills.length > 0
        ? `\n**Skills:** ${s.def.skills.join(", ")}`
        : "";
    return `### ${displayName(s.def.name)}...${skills}`;
})
```

---

## What Gets Fixed

### Before
```
Available agents: builder (has skills)
Hidden agents: scout, reviewer, tester (no skills)

User: "Use dispatch_agent to send task to scout"
Result: ❌ Agent "scout" not found
```

### After
```
Available agents: scout, builder, reviewer, tester (all team members)

User: "Use dispatch_agent to send task to scout"
Result: ✓ Scout executes the task
```

---

## Documentation Created

| File | Purpose |
|------|---------|
| **[AGENT_TEAMS_INDEX.md](./AGENT_TEAMS_INDEX.md)** | Start here - navigation hub |
| **[agent-teams-quick-fix.md](./agent-teams-quick-fix.md)** | 2-minute fix guide |
| **[agent-teams-troubleshooting.md](./agent-teams-troubleshooting.md)** | Complete troubleshooting guide |
| **[agent-teams-solution-examples.md](./agent-teams-solution-examples.md)** | Copy-paste code examples |
| **[agent-teams-visual-guide.md](./agent-teams-visual-guide.md)** | Diagrams and visual aids |
| **[AGENT_TEAMS_SUMMARY.md](./AGENT_TEAMS_SUMMARY.md)** | This file - executive summary |

---

## Quick Start

1. **Choose your solution:**
   - Solution A: Remove filter (2 min, simple)
   - Solution B: Add skills to agents (5-10 min, no code change)
   - Solution C: Environment variable (5 min, recommended)

2. **Follow the guide:**
   ```bash
   # Read the quick fix guide
   cat docs/agent-teams-quick-fix.md

   # Or see all options
   cat docs/AGENT_TEAMS_INDEX.md
   ```

3. **Apply the fix:**
   ```bash
   # Edit extensions/agent-team.ts
   # Then restart pi
   pi -e extensions/agent-team.ts
   ```

4. **Verify:**
   ```
   /agents-list
   Use dispatch_agent to send "test" to scout
   ```

---

## FAQ - Quick Answers

**Q: Is this a bug or a feature?**
A: It's a design choice that assumes all agents should have specialized skills. For many users, this is too restrictive.

**Q: Will this break my existing setup?**
A: No. All solutions are backwards compatible. Agents with skills still show them.

**Q: Which solution should I use?**
A: Solution C (environment variable) offers the most flexibility. Solution A (remove filter) is fastest.

**Q: Do I need to restart pi?**
A: Yes, or run `/agent-team-reload` after making changes.

**Q: Can I see which agents have skills?**
A: Run `/agents-list` - it shows agent status and info. The system prompt also shows skills for agents that have them.

---

## Related Context

This issue affects the **Agent Teams extension** which implements a dispatcher pattern where a primary coordinator agent delegates work to specialist agents. Each specialist maintains its own Pi session and can be resumed across invocations.

The extension loads agent definitions from:
- `.pi/agents/*.md`
- `.claude/agents/*.md`
- `agents/*.md`

Teams are defined in `.pi/agents/teams.yaml` where each team is a list of agent names.

---

## Next Steps

1. ✅ Read [agent-teams-quick-fix.md](./agent-teams-quick-fix.md) for immediate solution
2. ✅ Apply your chosen fix
3. ✅ Test with `/agents-list` and `dispatch_agent`
4. ✅ Refer to [agent-teams-troubleshooting.md](./agent-teams-troubleshooting.md) for detailed explanation if needed

---

**Status:** ✅ Documentation complete
**Created:** 2026-04-08
**Applies to:** `extensions/agent-team.ts` (all versions)
**Maintenance:** No ongoing maintenance required once applied
