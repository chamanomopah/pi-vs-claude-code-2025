# Shortcuts.yaml Quick Reference

## Format (One-Line Summary)

```yaml
extension-name:
  - keyId    # Optional description
```

## Valid Key IDs

- **Letters**: `a-z`
- **Function**: `f1-f12`
- **With modifiers**: `ctrl+x`, `shift+x`, `alt+x`, `ctrl+shift+x`

## Reserved Keys (Don't Use)

`escape`, `ctrl+c`, `ctrl+d`, `ctrl+z`, `shift+tab`, `ctrl+p`, `ctrl+shift+p`, `ctrl+l`, `ctrl+o`, `ctrl+t`, `ctrl+g`, `alt+enter`, `enter`, `ctrl+k`

## Safe Keys (Recommended)

- Function keys: `f1-f12`
- `ctrl+x`, `ctrl+q`

## Current Shortcuts

| Extension | Key | Action |
|-----------|-----|--------|
| agent-team | f6 | Next team |
| agent-team | f7 | Previous team |
| theme-cycler | ctrl+x | Next theme |
| theme-cycler | ctrl+q | Previous theme |
| test-shortcuts | f8 | Test notification |
| test-shortcuts | f9 | Test log |
| test-shortcuts | f10 | List all shortcuts |

## Use in Extension Code

```typescript
import { registerShortcuts } from "./shortcutLoader.ts";

pi.on("session_start", async (_event, _ctx) => {
  registerShortcuts(pi, "my-extension", {
    "f1": {
      handler: async (ctx) => {
        if (!ctx.hasUI) return;
        // Your code
      }
    },
  }, _ctx.cwd);
});
```

## Reload After Editing

```
/reload
```

## Full Docs

See `.pi/agents/SHORTCUTS.md` for complete documentation.
