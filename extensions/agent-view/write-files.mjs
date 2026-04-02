#!/usr/bin/env bun

import { writeFileSync } from 'fs';

const indexContent = `/**
 * Agent View Extension v1.2.0
 * Visualizador em tempo real de agentes Pi executando em paralelo.
 * 
 * CHANGES v1.2.0:
 * - Fixed: extractAgentInfo() with multiple fallback formats
 * - Added: Agent filter support (status, name with wildcards, source)
 * - Added: /agent-view filter commands
 * - Fixed: Agent view events now emitted properly
 * - Improved: Source detection for all orchestrator types
 */

import { AgentMonitor, AgentStatus, AgentSource, AgentFilters } from "./monitor.js";
import { AgentViewWidget, AgentViewConfig } from "./widget.js";

interface AgentViewExtension {
  monitor?: AgentMonitor;
  widget?: AgentViewWidget;
  config: AgentViewConfig;
  isEnabled: boolean;
  jsonMode: boolean;
  filters: AgentFilters;
}

const extensionState: AgentViewExtension = {
  config: {
    layout: "1x4",
    font: "medium",
    sortMode: "default",
    headerStyle: "detailed",
    showBorders: true,
    showColors: true,
    showProgress: true,
    autoRefresh: true,
    refreshInterval: 500
  },
  isEnabled: false,
  jsonMode: false,
  filters: {}
};

export default function agentViewExtension(pi: any): void {
  extensionState.jsonMode = isJSONMode();
  registerCLIFlags(pi);
  registerCommands(pi);
  extensionState.monitor = new AgentMonitor(pi, extensionState.config);
  
  pi.on("session_start", async () => {
    const mode = pi.getFlag?.("--agent-view-mode") || "auto";
    if (mode === "auto" && extensionState.jsonMode === false) {
      await openAgentView(pi);
    }
  });

  pi.on("session_shutdown", async () => {
    await closeAgentView(pi);
    extensionState.monitor?.dispose();
  });

  installSpawnHook(pi);
}

function isJSONMode(): boolean {
  const args = process.argv || [];
  return args.includes("--mode") && args[args.indexOf("--mode") + 1] === "json";
}

function registerCLIFlags(pi: any): void {
  if (pi.getFlag) {
    const layoutFlag = pi.getFlag("--agent-view-layout");
    if (layoutFlag && ["1x1", "1x2", "1x4", "1x8", "list"].includes(layoutFlag)) {
      extensionState.config.layout = layoutFlag as AgentViewConfig["layout"];
    }
    const fontFlag = pi.getFlag("--agent-view-font");
    if (fontFlag && ["small", "medium", "large"].includes(fontFlag)) {
      extensionState.config.font = fontFlag as AgentViewConfig["font"];
    }
  }
}

function registerCommands(pi: any): void {
  pi.registerCommand({
    name: "agent-view",
    description: "Open/close agent view widget",
    aliases: ["av"]
  }, async (args: { action?: string; value?: string } = {}) => {
    const action = args.action || "toggle";
    switch (action) {
      case "open": case "toggle": await openAgentView(pi); break;
      case "close": await closeAgentView(pi); break;
      case "layout":
        if (args.value && ["1x1", "1x2", "1x4", "1x8", "list"].includes(args.value)) {
          extensionState.config.layout = args.value as AgentViewConfig["layout"];
          extensionState.widget?.updateConfig(extensionState.config);
          await pi.notify(\`Layout changed to \${args.value}\`);
        }
        break;
      case "font":
        if (args.value && ["small", "medium", "large"].includes(args.value)) {
          extensionState.config.font = args.value as AgentViewConfig["font"];
          extensionState.widget?.updateConfig(extensionState.config);
          await pi.notify(\`Font changed to \${args.value}\`);
        }
        break;
      case "sort":
        extensionState.config.sortMode = extensionState.config.sortMode === "default" ? "active" : "default";
        extensionState.widget?.updateConfig(extensionState.config);
        await pi.notify(\`Sort mode: \${extensionState.config.sortMode}\`);
        break;
      case "filter": await handleFilterCommand(pi, args); break;
      default: await openAgentView(pi);
    }
  });

  pi.registerCommand({
    name: "agent-view-filter",
    description: "Filter agents by status, name, or source"
  }, async (args: { status?: string; name?: string; source?: string; clear?: boolean }) => {
    await handleFilterCommand(pi, args);
  });

  pi.registerCommand({ name: "agent-view-layout", description: "Change agent view layout" },
    async (args: { layout: string }) => {
      if (args.layout && ["1x1", "1x2", "1x4", "1x8", "list"].includes(args.layout)) {
        extensionState.config.layout = args.layout as AgentViewConfig["layout"];
        extensionState.widget?.updateConfig(extensionState.config);
        await pi.notify(\`Layout: \${args.layout}\`);
      }
    });

  pi.registerCommand({ name: "agent-view-font", description: "Change agent view font size" },
    async (args: { size: string }) => {
      if (args.size && ["small", "medium", "large"].includes(args.size)) {
        extensionState.config.font = args.size as AgentViewConfig["font"];
        extensionState.widget?.updateConfig(extensionState.config);
        await pi.notify(\`Font: \${args.size}\`);
      }
    });

  pi.registerCommand({ name: "agent-view-sort", description: "Toggle agent sort mode" },
    async () => {
      extensionState.config.sortMode = extensionState.config.sortMode === "default" ? "active" : "default";
      extensionState.widget?.updateConfig(extensionState.config);
      await pi.notify(\`Sort: \${extensionState.config.sortMode}\`);
    });

  pi.registerCommand({ name: "agent-view-close", description: "Close agent view widget" },
    async () => await closeAgentView(pi));

  registerKeybindings(pi);
}

async function handleFilterCommand(pi: any, args: any): Promise<void> {
  if (args.clear === true || args.clear === "true") {
    extensionState.filters = {};
    extensionState.monitor?.setFilters({});
    await pi.notify("Filters cleared");
    return;
  }

  let filterApplied = false;

  if (args.status) {
    const validStatuses: AgentStatus[] = ["idle", "starting", "running", "waiting", "complete", "error", "aborted"];
    if (validStatuses.includes(args.status as AgentStatus)) {
      extensionState.filters.status = args.status as AgentStatus;
      filterApplied = true;
    } else {
      await pi.notify(\`Invalid status: \${args.status}. Valid: \${validStatuses.join(", ")}\`);
      return;
    }
  }

  if (args.name) {
    extensionState.filters.name = args.name;
    filterApplied = true;
  }

  if (args.source) {
    const validSources: AgentSource[] = ["agent-team", "agent-chain", "pi-pi", "subagent", "unknown"];
    if (validSources.includes(args.source as AgentSource)) {
      extensionState.filters.source = args.source as AgentSource;
      filterApplied = true;
    } else {
      await pi.notify(\`Invalid source: \${args.source}. Valid: \${validSources.join(", ")}\`);
      return;
    }
  }

  if (filterApplied) {
    extensionState.monitor?.setFilters(extensionState.filters);
    const filterDesc = Object.entries(extensionState.filters).map(([k, v]) => \`\${k}=\${v}\`).join(", ") || "none";
    await pi.notify(\`Filters applied: \${filterDesc}\`);
  } else {
    const currentFilters = Object.entries(extensionState.filters).map(([k, v]) => \`\${k}=\${v}\`).join(", ") || "none";
    await pi.notify(\`Current filters: \${currentFilters}\`);
  }
}

function registerKeybindings(pi: any): void {
  pi.registerKeybinding?.("ctrl+shift+a", async () => await toggleAgentView(pi));
  pi.registerKeybinding?.("ctrl+shift+q", async () => await closeAgentView(pi));
}

async function installSpawnHook(pi: any): Promise<void> {
  try {
    const childProcess = await import("child_process");
    const originalSpawn = childProcess.spawn;

    childProcess.spawn = function(command: string, args: string[], options: any): any {
      if (command === "pi" || command.endsWith("/pi") || command.endsWith("\\pi.exe")) {
        const agentInfo = extractAgentInfo(args);
        if (agentInfo) {
          pi.events?.emit("subagent:spawn", { agentId: agentInfo.name, agentName: agentInfo.name, task: agentInfo.task, pid: null, source: agentInfo.source });
          cons
