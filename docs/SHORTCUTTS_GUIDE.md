# Keyboard Shortcuts Guide for Pi Extensions

## Overview

This guide explains how to configure and use keyboard shortcuts in Pi extensions via the `.pi/agents/shortcuts.yaml` file.

## Quick Start

1. Edit `.pi/agents/shortcuts.yaml`:
```yaml
my-extension:
  - f6            # my-action
  - alt+shift+i   # another-action
```

2. In your extension, register handlers:
```typescript
import { registerActionShortcuts } from "./shortcutLoader.ts";

registerActionShortcuts(pi, "my-extension", {
  "my-action": {
    description: "Do something",
    handler: async (ctx) => { /* your code */ }
  },
  "another-action": {
    description: "Do something else",
    handler: async (ctx) => { /* your code */ }
  }
}, ctx.cwd);
```

3. Reload: `/reload`

## Key ID Format

### Basic Format
```
modifier+key
```

### Modifiers (order doesn't matter!)
- `ctrl` - Control key
- `shift` - Shift key  
- `alt` - Alt/Meta key

**Important:** `alt+shift+i` and `shift+alt+i` are the same! They are normalized to `alt+shift+i`.

### Valid Keys

**Letters:** `a` through `z`

**Numbers:** `0` through `9`

**Function keys:** `f1` through `f12`

**Special keys:**
- `escape` or `esc`
- `enter` or `return`
- `tab`
- `space`
- `backspace`
- `delete`
- `insert`
- `home`
- `end`
- `pageup` or `pageDown`
- `up`, `down`, `left`, `right`

**Symbol keys:**
`` ` - = [ ] \ ; ' , . / ! @ # $ % ^ & * ( ) _ + | ~ { } : < > ? ```

### Examples

```yaml
# Single modifiers
- ctrl+c          # Copy
- alt+x           # Cut
- shift+enter     # New line

# Multiple modifiers (order doesn't matter!)
- ctrl+shift+x    # Same as shift+ctrl+x
- alt+shift+i     # Same as shift+alt+i
- ctrl+alt+delete # Same as alt+ctrl+delete

# Function keys (most reliable!)
- f6              # Always works
- f10             # Always works
```

## Terminal Compatibility

### Kitty Keyboard Protocol

Some key combinations require the **Kitty Keyboard Protocol** to work properly:

- ✅ **Works without Kitty:**
  - Single modifiers (ctrl+x, alt+x, shift+x)
  - Function keys (f1-f12)
  - Most special keys (enter, tab, escape, etc.)

- ⚠️  **Requires Kitty:**
  - Multiple modifiers with letters (ctrl+shift+x, alt+shift+i)
  - Multiple modifiers with arrows
  - Complex combinations (ctrl+alt+shift+x)

### Terminals with Kitty Protocol Support

| Terminal | Support | How to Enable |
|----------|---------|---------------|
| **Kitty** | ✅ Built-in | Default enabled |
| **WezTerm** | ✅ Supported | `enable_kitty_keyboard = true` in config |
| **Ghostty** | ✅ Built-in | Default enabled |
| **iTerm2** | ✅ Supported | Enable in profile settings |
| **VS Code** | ✅ Supported | `"terminal.integrated.enableKittyKeyboard": true` |
| **Windows Terminal** | ⚠️ Partial | May work with latest versions |
| **GNOME Terminal** | ❌ No | Consider alternatives |
| **macOS Terminal** | ❌ No | Use iTerm2 instead |

### Check Your Terminal

Run `/test-shortcuts` to see if your terminal supports Kitty protocol:

```
Kitty Keyboard Protocol: ACTIVE  ✅
```

or

```
Kitty Keyboard Protocol: INACTIVE  ⚠️
```

## Diagnostic Command

Use `/test-shortcuts` to:
- List all loaded shortcuts
- Check terminal capabilities
- Validate shortcut definitions
- See which shortcuts need Kitty protocol

## Best Practices

### 1. Use Function Keys for Maximum Compatibility
```yaml
my-extension:
  - f6   # Works on ALL terminals
  - f7   # Works on ALL terminals
  - f8   # Works on ALL terminals
```

### 2. Avoid Complex Combinations
```yaml
# ⚠️ May not work without Kitty
- ctrl+alt+shift+x

# ✅ Better alternative
- f6
```

### 3. Test Your Shortcuts
Always run `/test-shortcuts` after editing `shortcuts.yaml` to verify:
- Shortcuts are loaded correctly
- Your terminal supports the combinations
- No conflicts with built-in shortcuts

### 4. Use Descriptive Action Names
```yaml
# Good
- f6   # next-team
- f8   # prev-team

# Less clear
- f6   # action1
- f8   # action2
```

## Reserved Keys

These keys are used by Pi and should NOT be overridden:

| Shortcut | Purpose |
|----------|---------|
| `escape` | Cancel/interrupt |
| `ctrl+c` | Clear editor |
| `ctrl+d` | Exit |
| `ctrl+z` | Suspend |
| `shift+tab` | Cycle thinking level |
| `ctrl+p` | Cycle model forward |
| `shift+ctrl+p` | Cycle model backward |
| `ctrl+l` | Select model |
| `ctrl+o` | Expand tools |
| `ctrl+t` | Expand thinking |
| `ctrl+g` | External editor |
| `alt+enter` | Queue follow-up |
| `enter` | Submit input |
| `ctrl+k` | Delete to end of line |

## Troubleshooting

### Shortcut Not Working

1. **Check if loaded:**
   ```
   /test-shortcuts
   ```
   Look for your shortcut in the output.

2. **Check Kitty protocol:**
   If your shortcut uses multiple modifiers (like `alt+shift+i`), verify Kitty protocol is active.

3. **Try a function key:**
   Replace your shortcut with `f6` or `f7` to test if the handler works.

4. **Check for typos:**
   Verify the action name in YAML matches the handler in your code exactly.

### "No handler found" Warning

This means the action name in YAML doesn't match any registered handler:

```yaml
# In shortcuts.yaml
my-extension:
  - f6   # my-action

# In your extension
registerActionShortcuts(pi, "my-extension", {
  "my-action": {  // Must match exactly!
    description: "Do something",
    handler: async (ctx) => { ... }
  }
}, ctx.cwd);
```

### Modifier Order Confusion

Don't worry about modifier order! All these are the same:
- `alt+shift+i`
- `shift+alt+i`
- `ALT+SHIFT+I` (case insensitive)

They all get normalized to `alt+shift+i`.

## Examples

### Simple Extension with Shortcuts

```typescript
// extensions/my-extension.ts
import type { ExtensionAPI } from "@mariozechner/pi-coding-agent";
import { registerActionShortcuts } from "./shortcutLoader.ts";

export default function (pi: ExtensionAPI) {
  pi.on("session_start", async (_event, ctx) => {
    registerActionShortcuts(pi, "my-extension", {
      "do-work": {
        description: "Perform the main work",
        handler: async (ctx) => {
          ctx.ui.notify("Working...", "info");
          // Your code here
        }
      },
      "show-help": {
        description: "Show help information",
        handler: async (ctx) => {
          ctx.ui.notify("Help: Use F6 to work, F7 for help", "info");
        }
      }
    }, ctx.cwd);

    ctx.ui.notify("My Extension loaded! F6=work, F7=help", "info");
  });
}
```

```yaml
# .pi/agents/shortcuts.yaml
my-extension:
  - f6   # do-work
  - f7   # show-help
```

## Advanced Usage

### Dynamic Shortcut Registration

You can register shortcuts at runtime (not just at startup):

```typescript
pi.registerShortcut("f10", {
  description: "Dynamic action",
  handler: async (ctx) => {
    ctx.ui.notify("F10 pressed!", "info");
  }
});
```

### Conditional Shortcuts

Register shortcuts based on conditions:

```typescript
if (someCondition) {
  pi.registerShortcut("f11", {
    description: "Conditional action",
    handler: async (ctx) => { ... }
  });
}
```

## Resources

- [Pi Extensions Documentation](https://github.com/badlogic/pi-mono/blob/main/packages/coding-agent/docs/extensions.md)
- [Keybindings Documentation](https://github.com/badlogic/pi-mono/blob/main/packages/coding-agent/docs/keybindings.md)
- [Kitty Keyboard Protocol](https://sw.kovidgoyal.net/kitty/keyboard-protocol/)
- [Test Shortcuts](shortcut-diagnostic.ts) - Run `/test-shortcuts`

## Quick Reference

```bash
# Test your shortcuts
/test-shortcuts

# Reload after editing shortcuts.yaml
/reload

# View all commands
/          # then type "test" and tab
```

---

**Last updated:** 2025-01-02  
**Pi version:** 0.63.1+
