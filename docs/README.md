# Documentation Index

Complete guide for the pi-vs-claude-code project.

## 🚨 Quick Start: Agent Teams Issue

**If agents aren't appearing in your dispatch list:**

1. **[Executive Summary](./AGENT_TEAMS_SUMMARY.md)** ⏱️ 2 min read
   - Problem overview and recommended solution
   - Quick decision matrix

2. **[Quick Fix Guide](./agent-teams-quick-fix.md)** ⚡ Fastest solution
   - 3 solution options
   - Step-by-step fixes

3. **[Agent Teams Index](./AGENT_TEAMS_INDEX.md)** 📚 Complete hub
   - Links to all Agent Teams documentation
   - Verification steps

---

## Agent Teams Documentation

Complete troubleshooting and solutions for the Agent Teams extension.

| Document | Description | Time to Read |
|----------|-------------|--------------|
| **[AGENT_TEAMS_SUMMARY.md](./AGENT_TEAMS_SUMMARY.md)** | Executive summary - TL;DR of the issue | 2 min |
| **[agent-teams-quick-fix.md](./agent-teams-quick-fix.md)** | Fast path to resolution - 3 solutions | 3 min |
| **[AGENT_TEAMS_INDEX.md](./AGENT_TEAMS_INDEX.md)** | Navigation hub for all Agent Teams docs | 2 min |
| **[agent-teams-troubleshooting.md](./agent-teams-troubleshooting.md)** | Complete troubleshooting guide | 10 min |
| **[agent-teams-solution-examples.md](./agent-teams-solution-examples.md)** | Copy-paste code examples | 5 min |
| **[agent-teams-visual-guide.md](./agent-teams-visual-guide.md)** | Diagrams and visual explanations | 5 min |

### Agent Teams Quick Reference

**Problem:** Agents without `skills:` field hidden from dispatcher
**Solution:** Remove filter or add `skills: []` to agents
**Files:** `extensions/agent-team.ts` (line 461)
**Time:** 2-5 minutes

---

## Skills Documentation

Guides for implementing and using skills in Pi agents.

| Document | Description |
|----------|-------------|
| **[HOW_TO_USE_SKILLS.md](./HOW_TO_USE_SKILLS.md)** | Complete guide to using skills |
| **[INDEX_SKILLS.md](./INDEX_SKILLS.md)** | Skills reference index |
| **[AGENT_SKILLS_IMPLEMENTATION.md](./AGENT_SKILLS_IMPLEMENTATION.md)** | Implementation details |
| **[SKILLS_IMPLEMENTATION_SUMMARY.md](./SKILLS_IMPLEMENTATION_SUMMARY.md)** | Summary of skills implementation |

---

## Extensions & Best Practices

| Document | Description |
|----------|-------------|
| **[BEST_PRACTICES.md](./BEST_PRACTICES.md)** | Extension authoring best practices |
| **[QUICK_REFERENCE.md](./QUICK_REFERENCE.md)** | Common commands and patterns |
| **[COMPARISON.md](./COMPARISON.md)** | Claude Code vs Pi comparison |

---

## Shortcuts Documentation

| Document | Description |
|----------|-------------|
| **[SHORTCUTS_GUIDE.md](./SHORTCUTS_GUIDE.md)** | Complete shortcuts guide |
| **[QUICKSTART_SHORTCUTS.md](./QUICKSTART_SHORTCUTS.md)** | Quick start for shortcuts |
| **[SHORTCUT_FIX.md](./SHORTCUT_FIX.md)** | Shortcut troubleshooting |

---

## LiveKit Integration

| Document | Description |
|----------|-------------|
| **[LIVEKIT_SUMMARY.md](./LIVEKIT_SUMMARY.md)** | LiveKit integration summary |
| **[LIVEKIT_IMPLEMENTATION_GUIDE.md](./LIVEKIT_IMPLEMENTATION_GUIDE.md)** | Implementation guide |

---

## Testing & Verification

| Document | Description |
|----------|-------------|
| **[TEST_CHECKLIST.md](./TEST_CHECKLIST.md)** | Testing checklist |
| **[TEST_RESULTS.md](./TEST_RESULTS.md)** | Test results documentation |

---

## By Use Case

### I want to...

**Fix Agent Teams issue:**
1. [AGENT_TEAMS_SUMMARY.md](./AGENT_TEAMS_SUMMARY.md) - Start here
2. [agent-teams-quick-fix.md](./agent-teams-quick-fix.md) - Apply fix
3. [agent-teams-solution-examples.md](./agent-teams-solution-examples.md) - Get code

**Understand the problem:**
1. [agent-teams-troubleshooting.md](./agent-teams-troubleshooting.md) - Full explanation
2. [agent-teams-visual-guide.md](./agent-teams-visual-guide.md) - See diagrams

**Use skills in agents:**
1. [HOW_TO_USE_SKILLS.md](./HOW_TO_USE_SKILLS.md) - Complete guide
2. [INDEX_SKILLS.md](./INDEX_SKILLS.md) - Reference

**Write extensions:**
1. [BEST_PRACTICES.md](./BEST_PRACTICES.md) - Guidelines
2. [QUICK_REFERENCE.md](./QUICK_REFERENCE.md) - Commands

**Set up shortcuts:**
1. [QUICKSTART_SHORTCUTS.md](./QUICKSTART_SHORTCUTS.md) - Quick start
2. [SHORTCUTS_GUIDE.md](./SHORTCUTS_GUIDE.md) - Full guide

---

## By Skill Level

### Beginner
- [AGENT_TEAMS_SUMMARY.md](./AGENT_TEAMS_SUMMARY.md) - Issue overview
- [agent-teams-quick-fix.md](./agent-teams-quick-fix.md) - Quick fixes
- [QUICK_REFERENCE.md](./QUICK_REFERENCE.md) - Common commands

### Intermediate
- [AGENT_TEAMS_INDEX.md](./AGENT_TEAMS_INDEX.md) - Agent Teams hub
- [HOW_TO_USE_SKILLS.md](./HOW_TO_USE_SKILLS.md) - Skills guide
- [BEST_PRACTICES.md](./BEST_PRACTICES.md) - Extension practices

### Advanced
- [agent-teams-troubleshooting.md](./agent-teams-troubleshooting.md) - Deep dive
- [agent-teams-solution-examples.md](./agent-teams-solution-examples.md) - Code examples
- [COMPARISON.md](./COMPARISON.md) - Feature comparison

---

## Document Statistics

| Category | Documents |
|----------|-----------|
| Agent Teams | 6 docs |
| Skills | 4 docs |
| Best Practices | 3 docs |
| Shortcuts | 3 docs |
| LiveKit | 2 docs |
| Testing | 2 docs |
| **Total** | **20 docs** |

---

## Contributing

When adding new documentation:

1. Use descriptive filenames with kebab-case
2. Add a title and description
3. Update this index
4. Cross-reference related documents
5. Include examples where applicable

---

## Project Links

- **Main README:** [../README.md](../README.md)
- **Extensions:** [../extensions/](../extensions/)
- **Agent Definitions:** [../.pi/agents/](../.pi/agents/)
- **Skills:** [../.pi/skills/](../.pi/skills/)

---

**Last Updated:** 2026-04-08
**Documentation Version:** 1.0
