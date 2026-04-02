/**
 * Agent View Extension v1.2.1
 * 
 * Visualizador em tempo real de agentes Pi executando em paralelo.
 * Suporta layouts responsivos, detecção universal de subprocessos e modo JSON.
 * 
 * CHANGES v1.2.1:
 * - FIXED: Keybinding "q" removido (widget já tem handleInput para "q")
 * - FIXED: Arquivo completo com todas as funções faltantes
 * - FIXED: Keybindings usando formato correto (minúsculas)
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
          await pi.notify(`Layout changed to ${args.value}`);
        }
        break;
      case "font":
        if (args.value && ["small", "medium", "large"].includes(args.value)) {
          extensionState.config.font = args.value as AgentViewConfig["font"];
          extensionState.widget?.updateConfig(extensionState.config);
          await pi.notify(`Font changed to ${args.value}`);
        }
        break;
      case "sort":
        extensionState.config.sortMode = extensionState.config.sortMode === "default" ? "active" : "default";
        extensionState.widget?.updateConfig(extensionState.config);
        await pi.notify(`Sort mode: ${extensionState.config.sortMode}`);
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
        await pi.notify(`Layout: ${args.layout}`);
      }
    });

  pi.registerCommand({ name: "agent-view-font", description: "Change agent view font size" },
    async (args: { size: string }) => {
      if (args.size && ["small", "medium", "large"].includes(args.size)) {
        extensionState.config.font = args.size as AgentViewConfig["font"];
        extensionState.widget?.updateConfig(extensionState.config);
        await pi.notify(`Font: ${args.size}`);
      }
    });

  pi.registerCommand({ name: "agent-view-sort", description: "Toggle agent sort mode" },
    async () => {
      extensionState.config.sortMode = extensionState.config.sortMode === "default" ? "active" : "default";
      extensionState.widget?.updateConfig(extensionState.config);
      await pi.notify(`Sort: ${extensionState.config.sortMode}`);
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
      await pi.notify(`Invalid status: ${args.status}. Valid: ${validStatuses.join(", ")}`);
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
      await pi.notify(`Invalid source: ${args.source}. Valid: ${validSources.join(", ")}`);
      return;
    }
  }

  if (filterApplied) {
    extensionState.monitor?.setFilters(extensionState.filters);
    const filterDesc = Object.entries(extensionState.filters).map(([k, v]) => `${k}=${v}`).join(", ") || "none";
    await pi.notify(`Filters applied: ${filterDesc}`);
  } else {
    const currentFilters = Object.entries(extensionState.filters).map(([k, v]) => `${k}=${v}`).join(", ") || "none";
    await pi.notify(`Current filters: ${currentFilters}`);
  }
}

/**
 * Registra atalhos de teclado globais
 * 
 * NOTA v1.2.1: O keybinding "q" foi REMOVIDO porque:
 * 1. O widget AgentViewWidget ja captura "q" via handleInput() quando esta ativo
 * 2. Um keybinding global para "q" conflitaria com a funcionalidade do Pi
 * 3. A tecla "q" nao deve ser sobrescrita globalmente por uma extensao
 */
function registerKeybindings(pi: any): void {
  // Ctrl+Shift+A: Toggle agent-view
  pi.registerKeybinding?.("ctrl+shift+a", async () => await toggleAgentView(pi));
  
  // Ctrl+Shift+Q: Close agent-view
  pi.registerKeybinding?.("ctrl+shift+q", async () => await closeAgentView(pi));
  
  // NOTA: O keybinding "q" foi intencionalmente removido.
  // O widget ja trata "q" localmente em handleInput() quando esta focado.
}

function installSpawnHook(pi: any): void {
  try {
    const childProcess = require("child_process");
    const originalSpawn = childProcess.spawn;

    childProcess.spawn = function(command: string, args: string[], options: any): any {
      const isPiCommand = command === "pi" || 
        command.endsWith("/pi") || 
        command.endsWith("\pi.exe") ||
        command.endsWith("/pi.cmd") ||
        command.endsWith("\pi.cmd");

      if (isPiCommand) {
        const agentInfo = extractAgentInfo(args);
        if (agentInfo) {
          pi.events?.emit("subagent:spawn", {
            agentId: agentInfo.name,
            agentName: agentInfo.name,
            task: agentInfo.task,
            pid: null,
            source: agentInfo.source
          });

          const proc = originalSpawn.call(this, command, args, options);
          
          pi.events?.emit("subagent:spawn", {
            ...agentInfo,
            pid: proc.pid
          });

          if (proc.stdout) {
            proc.stdout.on("data", (data: Buffer) => {
              const output = data.toString();
              parseAgentOutput(pi, agentInfo.name, output);
            });
          }

          proc.on("close", (code: number | null) => {
            pi.events?.emit("subagent:complete", {
              agentId: agentInfo.name,
              exitCode: code || 0,
              duration: 0
            });
          });

          return proc;
        }
      }

      return originalSpawn.call(this, command, args, options);
    };
  } catch (error) {
    console.debug("[agent-view] Could not install spawn hook:", error);
  }
}

function extractAgentInfo(args: string[]): { name: string; task: string; source: string } | null {
  const hasJSONMode = args.includes("--mode") && args.includes("json");
  const hasPrintFlag = args.includes("-p") || args.includes("--print");
  const hasNoExtensions = args.includes("--no-extensions");
  
  if (!hasJSONMode || !hasPrintFlag || !hasNoExtensions) {
    const promptIndex = args.indexOf("--append-system-prompt");
    if (promptIndex === -1) return null;
  }
  
  const promptIndex = args.indexOf("--append-system-prompt");
  if (promptIndex !== -1 && args[promptIndex + 1]) {
    const promptPath = args[promptIndex + 1];
    
    const patterns = [
      /prompt-([^.]+)\.md$/,
      /prompt[-_]([^-._]+)[._]/,
      /agent[-_]([^-._]+)[._]/,
      /\/([^\/]+)\/prompt\.md$/
    ];
    
    let agentName: string | null = null;
    for (const pattern of patterns) {
      const match = promptPath.match(pattern);
      if (match && match[1]) {
        agentName = match[1];
        break;
      }
    }
    
    if (agentName) {
      const taskIndex = args.findLastIndex((arg, i) => !arg.startsWith("-") && i > promptIndex);
      const task = taskIndex !== -1 ? args[taskIndex] : "Running...";
      
      let source = "unknown";
      if (args.includes("--agent-team")) source = "agent-team";
      else if (args.includes("--agent-chain")) source = "agent-chain";
      else if (args.includes("--pi-pi")) source = "pi-pi";
      else if (args.includes("--subagent")) source = "subagent";
      
      return { name: agentName, task, source };
    }
  }
  
  return null;
}

function parseAgentOutput(pi: any, agentId: string, output: string): void {
  const lines = output.split("\n").filter(line => line.trim().startsWith("{"));
  
  for (const line of lines) {
    try {
      const event = JSON.parse(line);
      
      if (event.type === "agent_start" || event.type === "process_start") {
        pi.events?.emit("subagent:start", { agentId, event });
      } else if (event.type === "agent_end") {
        pi.events?.emit("subagent:end", { 
          agentId, 
          exitCode: event.exitCode || 0,
          duration: event.duration || 0
        });
      } else if (event.type === "turn_start") {
        pi.events?.emit("subagent:output", { 
          agentId, 
          output: event.content || "",
          timestamp: Date.now()
        });
      }
    } catch {
      // Ignorar linhas que nao sao JSON valido
    }
  }
}

async function openAgentView(pi: any): Promise<void> {
  if (extensionState.isEnabled) {
    return;
  }

  extensionState.isEnabled = true;

  extensionState.widget = new AgentViewWidget(
    extensionState.monitor!,
    extensionState.config
  );

  // Configurar listener para o evento "close" do widget
  extensionState.widget.on("close", () => {
    // Quando o widget emite "close" (via tecla 'q' local), fechar agent-view
    setTimeout(() => closeAgentView(pi), 0);
  });

  if (pi.ui?.registerComponent) {
    pi.ui.registerComponent("agent-view", extensionState.widget);
  }

  extensionState.monitor?.start();

  await pi.notify("Agent View opened (press 'q' to close)");
}

async function closeAgentView(pi: any): Promise<void> {
  if (!extensionState.isEnabled) {
    return;
  }

  extensionState.isEnabled = false;

  extensionState.monitor?.stop();

  if (pi.ui?.unregisterComponent) {
    pi.ui.unregisterComponent("agent-view");
  }

  extensionState.widget = undefined;

  await pi.notify("Agent View closed");
}

async function toggleAgentView(pi: any): Promise<void> {
  if (extensionState.isEnabled) {
    await closeAgentView(pi);
  } else {
    await openAgentView(pi);
  }
}

export { extensionState };
