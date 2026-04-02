# Shortcuts.yaml Format Documentation

## Overview

The `.pi/agents/shortcuts.yaml` file provides a centralized way to define keyboard shortcuts for all Pi extensions in your project. This makes it easy to customize shortcuts without editing extension code.

## Format

```yaml
# Comment describing the extension group
extension-name:
  - keyId    # Description (optional inline comment)
  - keyId    # Another shortcut for same action

another-extension:
  - f1       # Primary action
  - ctrl+x   # Alternative shortcut
```

### Components

1. **Extension Name** - The key used to identify the extension (must match what's used in `registerShortcuts()`)
2. **Key ID** - Keyboard shortcut identifier (format: `modifier+key`)
3. **Description** (optional) - Inline comment describing what the shortcut does

## Key ID Format

`modifier+key` where:
- **Modifiers**: `ctrl`, `shift`, `alt` (combinable)
- **Keys**: 
  - Letters: `a-z`
  - Digits: `0-9`
  - Function: `f1-f12`
  - Special: `escape`, `enter`, `tab`, `space`, `backspace`, `delete`, `home`, `end`, `pageUp`, `pageDown`, `up`, `down`, `left`, `right`
  - Symbols: `` ` ``, `-`, `=`, `[`, `]`, `\`, `;`, `'`, `,`, `.`, `/`, `!`, `@`, `#`, `$`, `%`, `^`, `&`, `*`, `(`, `)`, `_`, `+`, `|`, `~`, `{`, `}`, `:`, `<`, `>`, `?`

### Examples

- `ctrl+x` - Ctrl+X
- `f6` - F6 function key
- `ctrl+shift+p` - Ctrl+Shift+P
- `alt+enter` - Alt+Enter

## Reserved Keys (Cannot Use)

These keys are reserved by Pi and **cannot be overridden**:

| Key | Action |
|-----|--------|
| `escape` | Cancel/abort |
| `ctrl+c` | Clear/copy |
| `ctrl+d` | Exit |
| `ctrl+z` | Suspend |
| `shift+tab` | Cycle thinking level |
| `ctrl+p` | Cycle model forward |
| `ctrl+shift+p` | Cycle model backward |
| `ctrl+l` | Select model |
| `ctrl+o` | Expand tools |
| `ctrl+t` | Toggle thinking |
| `ctrl+g` | External editor |
| `alt+enter` | Follow-up message |
| `enter` | Submit |
| `ctrl+k` | Delete to line end |

## Safe Keys (Recommended)

- **Function keys**: `f1-f12` (all unbound by default)
- **ctrl+letter**: Most are free except reserved ones above
  - `ctrl+x`, `ctrl+q` work well
  - `ctrl+h` may be intercepted by some terminals

## Current Shortcuts

### Agent Team Extension

```yaml
agent-team:
  - f6   # Cycle to next team
  - f7   # Cycle to previous team
```

### Theme Cycler Extension

```yaml
theme-cycler:
  - ctrl+x   # Cycle theme forward
  - ctrl+q   # Cycle theme backward
```

## Usage in Extensions

### Option 1: Using the Helper (Recommended)

```typescript
import { registerShortcuts } from "./shortcutLoader.ts";

// In session_start event
pi.on("session_start", async (_event, _ctx) => {
  registerShortcuts(pi, "my-extension", {
    "f1": {
      handler: async (ctx) => {
        if (!ctx.hasUI) return;
        // Do something
      }
    },
    "ctrl+x": {
      description: "Custom description", // Optional: override YAML
      handler: async (ctx) => {
        if (!ctx.hasUI) return;
        // Do something else
      }
    },
  }, _ctx.cwd);
});
```

### Option 2: Manual Registration

```typescript
import { loadShortcuts } from "./shortcutLoader.ts";

pi.on("session_start", async (_event, _ctx) => {
  const shortcuts = loadShortcuts("my-extension", _ctx.cwd);
  
  for (const [keyId, description] of shortcuts) {
    pi.registerShortcut(keyId, {
      description,
      handler: async (ctx) => {
        if (!ctx.hasUI) return;
        // Handle the shortcut
      }
    });
  }
});
```

## Reloading Changes

After editing `shortcuts.yaml`, reload the extension:

```
/reload
```

Or restart Pi completely:

```
pi -e extensions/your-extension.ts
```

## Examples

### Single Action, Multiple Shortcuts

```yaml
my-app:
  - f1         # Quick action via function key
  - ctrl+a     # Alternative via keyboard
  - alt+f1     # Another option
```

### Grouped by Category

```yaml
# Navigation shortcuts
navigator:
  - f1   # Go back
  - f2   # Go forward
  - f3   # Go home

# Editing shortcuts
editor:
  - ctrl+s   # Save
  - ctrl+z   # Undo
  - ctrl+y   # Redo
```

### With Descriptions

```yaml
# Window management
window-mgr:
  - ctrl+shift+n   # New window
  - ctrl+shift+w   # Close window
  - ctrl+tab       # Cycle windows
```

## Best Practices

1. **Use function keys (F1-F12)** for extension-specific actions — they're universally available
2. **Prefer `ctrl+letter`** over `alt+letter` for better terminal compatibility (especially on macOS)
3. **Document shortcuts** with inline comments in the YAML
4. **Keep it consistent** — use similar patterns across related extensions
5. **Test on different terminals** — especially if using `alt` or `shift` modifiers
6. **Avoid reserved keys** — they will be silently ignored

## Troubleshooting

### Shortcuts Not Working

1. Check if the key is reserved (see list above)
2. Run Pi with `--verbose` to see shortcut conflicts
3. Ensure `registerShortcuts()` is called in `session_start` (not after)
4. Use `/reload` after editing `shortcuts.yaml`

### macOS Terminal Issues

On macOS, `alt+letter` combinations may type special characters instead of registering as shortcuts. Use:
- `ctrl+letter` combinations (works everywhere)
- Function keys `f1-f12` (universal compatibility)
- Kitty-protocol terminals (Ghostty, WezTerm, Kitty) for full `alt` support

## See Also

- `extensions/shortcutLoader.ts` - Helper module for loading shortcuts
- `extensions/agent-team.ts` - Example usage
- `extensions/theme-cycler.ts` - Another example
- Pi docs: `pi-docs/keybindings.md` - Complete keybinding reference
