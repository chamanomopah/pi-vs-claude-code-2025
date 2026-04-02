/**
 * Agent View Extension v1.2.0
 * 
 * Visualizador em tempo real de agentes Pi executando em paralelo.
 * Suporta layouts responsivos, detecção universal de subprocessos,
 * modo JSON e persistência de presets.
 */

import { Type } from "@sinclair/typebox";
import { AgentMonitor } from "./monitor.js";
import { AgentViewWidget, AgentViewConfig } from "./widget.js";
import { ConfigManager, DEFAULT_CONFIG, AgentViewPreset } from "./config.js";
import { PresetStorage } from "./storage.js";
import { logger } from "./logger.js";
import { errorHandler, createError, ErrorSeverity } from "./error-handler.js";
import { createDefaultHealthMonitor } from "./health-monitor.js";

interface AgentViewExtension {
  monitor?: AgentMonitor;
  widget?: AgentViewWidget;
  configManager: ConfigManager;
  storage: PresetStorage;
  isEnabled: boolean;
  jsonMode: boolean;
}

const extensionState: AgentViewExtension = {
  configManager: new ConfigManager(),
  storage: new PresetStorage(),
  isEnabled: false,
  jsonMode: false,
};

/**
 * Função principal da extensão - chamada pelo Pi ao carregar
 */
export default function agentViewExtension(pi: any): void {
  // Inicializar logger
  logger.info("Agent View Extension v1.2.0 loading...");
  
  // Detectar modo JSON
  extensionState.jsonMode = isJSONMode();
  logger.debug(`JSON mode: ${extensionState.jsonMode}`);

  // Inicializar storage e carregar presets
  extensionState.storage.load().catch((err) => {
    logger.error("Failed to load presets", err);
  });

  // Inicializar health monitor
  const healthMonitor = createDefaultHealthMonitor();
  healthMonitor.start();

  // Detectar problemas
  healthMonitor.on("status-change", (status) => {
    if (status !== "healthy") {
      logger.warn(`Health status: ${status}`);
    }
  });

  // Carregar última configuração
  loadLastConfig();

  // Registrar flags CLI
  registerCLIFlags(pi);

  // Registrar comandos
  registerCommands(pi);

  // Inicializar monitor com configuração completa
  const config = extensionState.configManager.getConfig();
  extensionState.monitor = new AgentMonitor(pi, config, config);

  // Hook de sessão
  pi.on("session_start", async () => {
    const mode = pi.getFlag?.("--agent-view-mode") || "auto";
    if (mode === "auto" && extensionState.jsonMode === false) {
      await openAgentView(pi);
    }
  });

  // Hook de encerramento para cleanup
  pi.on("session_shutdown", async () => {
    await closeAgentView(pi);
    extensionState.monitor?.dispose();
    await extensionState.storage.save(true);
    await logger.flush();
    healthMonitor.dispose();
  });

  // Hook universal em spawn para detecção de subprocessos
  installSpawnHook(pi);

  logger.info("Agent View Extension loaded successfully");
}

/**
 * Carrega última configuração usada
 */
async function loadLastConfig(): Promise<void> {
  try {
    const lastPreset = extensionState.storage.getLastPreset();
    if (lastPreset) {
      const preset = await extensionState.storage.loadPreset(lastPreset);
      if (preset) {
        extensionState.configManager.applyPreset(preset);
        logger.debug(`Loaded last preset: ${lastPreset}`);
      }
    }
  } catch (error) {
    logger.warn("Could not load last config", error);
  }
}

/**
 * Detecta se Pi está rodando em modo JSON
 */
function isJSONMode(): boolean {
  const args = process.argv || [];
  const modeIndex = args.indexOf("--mode");
  return modeIndex !== -1 && args[modeIndex + 1] === "json";
}

/**
 * Registra flags CLI para configuração do agent-view
 */
function registerCLIFlags(pi: any): void {
  if (pi.getFlag) {
    const layoutFlag = pi.getFlag("--agent-view-layout");
    if (layoutFlag && ["1x1", "1x2", "1x4", "1x8", "list"].includes(layoutFlag)) {
      extensionState.configManager.updateConfig({ layout: layoutFlag });
    }

    const fontFlag = pi.getFlag("--agent-view-font");
    if (fontFlag && ["small", "medium", "large"].includes(fontFlag)) {
      extensionState.configManager.updateConfig({ font: fontFlag });
    }
  }
}
