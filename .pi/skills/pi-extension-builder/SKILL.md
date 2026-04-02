---
name: pi-extension-builder
description: Complete toolkit for creating Pi extensions. scaffolds TypeScript extension projects with proper structure (tools, events, UI, commands), creates manifest.json, implements tool registration with TypeBox schemas, event interception, custom TUI components, and follows Pi extension best practices.
allowed-tools: Bash,read,write,edit,find,ls
---

# Pi Extension Builder

Complete toolkit for creating TypeScript extensions for the Pi CLI.

## Extension Structure

```
my-extension/
├── package.json           # npm package manifest
├── tsconfig.json          # TypeScript config
├── manifest.json          # Pi extension manifest
├── src/
│   └── index.ts          # Main extension entry point
├── scripts/              # Optional utility scripts
└── README.md             # Extension documentation
```

## Quick Start

### 1. Scaffold New Extension

```bash
# Create extension directory
mkdir my-extension && cd my-extension

# Initialize package.json
npm init -y

# Install dependencies
npm install --save-dev typescript @types/node
npm install @sinclair/typebox
```

### 2. Create manifest.json

```json
{
  "name": "my-extension",
  "version": "1.0.0",
  "description": "My Pi extension",
  "main": "dist/index.js",
  "permissions": [
    "tools",
    "events",
    "ui"
  ]
}
```

### 3. Create tsconfig.json

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true
  },
  "include": ["src/**/*"]
}
```

### 4. Create src/index.ts

```typescript
import { PiExtension } from "@pi/sdk";

export default function(extension: PiExtension) {
  // Register custom tool
  extension.registerTool({
    name: "my_tool",
    description: "Does something useful",
    parameters: {
      type: "object",
      properties: {
        input: { type: "string" }
      },
      required: ["input"]
    }
  }, async (args) => {
    return { result: `Processed: ${args.input}` };
  });

  // Intercept event
  extension.on("session_start", async (ctx) => {
    extension.pi.appendEntry({
      role: "system",
      content: [{ type: "text", text: "Extension loaded!" }]
    });
  });

  // Register command
  extension.registerCommand({
    name: "my-command",
    description: "My custom command"
  }, async () => {
    const ui = extension.pi.ui;
    await ui.notify("Command executed!");
  });
}
```

## Key Patterns

### Register Tool with TypeBox

```typescript
import { Type } from "@sinclair/typebox";

extension.registerTool({
  name: "search_files",
  description: "Search files by pattern",
  parameters: Type.Object({
    pattern: Type.String({ minLength: 1 }),
    path: Type.String({ default: "." }),
    maxResults: Type.Number({ default: 10 })
  })
}, async (args) => {
  // Implementation
  return { files: [...] };
});
```

### Custom UI Components

```typescript
extension.registerCommand({
  name: "show-ui",
  description: "Show custom UI"
}, async () => {
  const result = await extension.pi.ui.custom({
    type: "select",
    title: "Choose option",
    options: [
      { label: "Option 1", value: "1" },
      { label: "Option 2", value: "2" }
    ]
  });
  return result;
});
```

### Event Interception

```typescript
// Available events: session_start, input, before_agent_start, agent_start,
// message_start, turn_start, context, tool_call, tool_result, turn_end,
// message_end, agent_end, session_end

extension.on("tool_call", async (ctx, next) => {
  console.log(`Tool called: ${ctx.toolName}`);
  await next();
});
```

### Session Persistence

```typescript
extension.on("agent_end", async (ctx) => {
  extension.pi.appendEntry({
    role: "system",
    content: [{
      type: "text",
      text: `Agent completed in ${ctx.duration}ms`
    }]
  });
});
```

## Build & Install

```bash
# Build TypeScript
npx tsc

# Install globally
pi install .

# Install locally
pi install . --local
```

## TUI Components Reference

Common components for custom UI:
- **Text** - Formatted text with word wrap
- **Box** - Container with padding/borders
- **Container** - Vertical layout
- **Markdown** - Render markdown with syntax highlighting
- **SelectList** - Interactive selection list
- **SettingsList** - Toggle settings
- **BorderedLoader** - Async operation loader

## Events Reference

Session lifecycle events in order:
1. session_start
2. input
3. before_agent_start
4. agent_start
5. message_start
6. turn_start
7. context
8. tool_call
9. tool_result
10. turn_end
11. message_end
12. agent_end
13. session_end (optional)

## Best Practices

1. **Use TypeBox** for type-safe parameter schemas
2. **Handle errors** gracefully with try/catch
3. **Document tools** with clear descriptions
4. **Limit side effects** in event handlers
5. **Use async/await** for all async operations
6. **Clean up resources** in session_end if needed

## Examples

See `pi-docs/extensions.md` for complete examples and advanced patterns.
