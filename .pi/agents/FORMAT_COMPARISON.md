# Format Comparison: teams.yaml vs shortcuts.yaml

## Similarities

Both files use the same simple, list-based YAML format:

### teams.yaml
```yaml
team-name:
  - member1
  - member2
  - member3
```

### shortcuts.yaml
```yaml
extension-name:
  - keyId    # Optional description
  - keyId    # Another shortcut
```

## Key Differences

| Aspect | teams.yaml | shortcuts.yaml |
|--------|-----------|----------------|
| **Purpose** | Group agents into teams | Define keyboard shortcuts |
| **List items** | Agent names | Key IDs |
| **Descriptions** | Via team name/comments | Inline comments after key |
| **Multiple per group** | Yes (many agents) | Yes (many shortcuts) |

## Visual Example

```
teams.yaml                    shortcuts.yaml
─────────────────────────────────────────────────────────────────
plan-build:                   agent-team:
  - planner                     - f6   # Next team
  - builder                     - f7   # Previous team
  - reviewer
                              
research:                     theme-cycler:
  - scout                       - ctrl+x   # Forward
  - researcher                 - ctrl+q   # Backward
```

## Structure Pattern

Both follow this pattern:
1. **Category name** as key (team/extension name)
2. **Hyphen-prefixed list** of items
3. **Optional comments** for documentation

This consistency makes both files easy to:
- ✅ Edit manually
- ✅ Parse programmatically
- ✅ Extend with new entries
- ✅ Understand at a glance

## Parser Functions

The parse functions are nearly identical:

### parseTeamsYaml()
```typescript
function parseTeamsYaml(raw: string): Record<string, string[]> {
  // Returns: { "team-name": ["agent1", "agent2"] }
}
```

### parseShortcutsYaml()
```typescript
function parseShortcutsYaml(raw: string): Map<string, Map<string, string>> {
  // Returns: Map { "ext-name" => Map { "keyId" => "description" } }
}
```

## Usage Pattern

Both are loaded during `session_start`:

```typescript
// Load teams
const teamsPath = join(cwd, ".pi", "agents", "teams.yaml");
const teams = parseTeamsYaml(readFileSync(teamsPath, "utf-8"));

// Load shortcuts
const shortcutsPath = join(cwd, ".pi", "agents", "shortcuts.yaml");
const shortcuts = parseShortcutsYaml(readFileSync(shortcutsPath, "utf-8"));
```
