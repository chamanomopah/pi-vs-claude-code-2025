/**
 * Agent View Extension - Test Script
 * 
 * Exemplo de uso da extensão agent-view para testes.
 */

import { AgentMonitor } from "./monitor.js";
import type { AgentViewConfig } from "./monitor.js";

// Configuração de exemplo
const config: AgentViewConfig = {
  layout: "1x4",
  font: "medium",
  sortMode: "active",
  headerStyle: "detailed",
  showBorders: true,
  showColors: true,
  showProgress: true,
  autoRefresh: true,
  refreshInterval: 500,
};

// Mock da API do Pi para testes
const mockPi = {
  events: {
    on: (event: string, handler: (...args: any[]) => void) => {
      console.log(`[Mock] Registered listener for: ${event}`);
    },
    off: (event: string, handler: (...args: any[]) => void) => {
      console.log(`[Mock] Removed listener for: ${event}`);
    },
    emit: (event: string, data?: any) => {
      console.log(`[Mock] Emitted: ${event}`, data?.slice?.(0, 50) || data);
    },
  },
  notify: async (message: string) => {
    console.log(`[Mock] Notification: ${message}`);
  },
  registerCommand: (cmd: any, handler: any) => {
    console.log(`[Mock] Registered command: ${cmd.name}`);
  },
  registerKeybinding: (key: string, handler: any) => {
    console.log(`[Mock] Registered keybinding: ${key}`);
  },
  ui: {
    registerComponent: (name: string, component: any) => {
      console.log(`[Mock] Registered UI component: ${name}`);
    },
    unregisterComponent: (name: string) => {
      console.log(`[Mock] Unregistered UI component: ${name}`);
    },
  },
};

// Teste do AgentMonitor
function testAgentMonitor() {
  console.log("\n=== Testing AgentMonitor ===\n");

  const monitor = new AgentMonitor(mockPi, config);

  // Simular eventos de agentes
  mockPi.events.emit("subagent:spawn", {
    agentId: "scout-1",
    agentName: "scout",
    task: "Explore codebase structure",
    source: "agent-team",
  });

  mockPi.events.emit("subagent:spawn", {
    agentId: "analyst-1",
    agentName: "analyst",
    task: "Analyze dependencies",
    source: "agent-team",
  });

  mockPi.events.emit("subagent:spawn", {
    agentId: "builder-1",
    agentName: "builder",
    task: "Build project",
    source: "agent-chain",
  });

  mockPi.events.emit("subagent:start", {
    agentId: "scout-1",
  });

  mockPi.events.emit("subagent:output", {
    agentId: "scout-1",
    output: "Found 15 TypeScript files",
    timestamp: Date.now(),
  });

  // Ver agentes
  console.log("\n--- Agents after spawn/start/output ---");
  const agents = monitor.getAgents();
  for (const agent of agents) {
    console.log(`[${agent.status}] ${agent.name}: ${agent.task}`);
    console.log(`  Output: ${agent.lastOutput}`);
  }

  // Simular conclusão
  mockPi.events.emit("subagent:complete", {
    agentId: "scout-1",
    exitCode: 0,
    duration: 1500,
  });

  console.log("\n--- Agents after completion ---");
  const agents2 = monitor.getAgents();
  for (const agent of agents2) {
    console.log(`[${agent.status}] ${agent.name}`);
  }

  // Status counts
  console.log("\n--- Status Counts ---");
  const counts = monitor.getStatusCounts();
  console.log(counts);

  // Cleanup
  monitor.dispose();
  console.log("\n--- Monitor disposed ---");
}

// Teste de parse de argumentos
function testArgumentParsing() {
  console.log("\n=== Testing Argument Parsing ===\n");

  const testCases = [
    {
      args: ["pi", "--mode", "json", "-p", "--no-extensions", "--append-system-prompt", "/tmp/prompt-scout.md", "Explore codebase"],
      expected: { name: "scout", task: "Explore codebase" },
    },
    {
      args: ["pi", "--mode", "json", "-p", "--no-extensions", "--append-system-prompt", "/tmp/prompt-analyst.md", "Analyze code"],
      expected: { name: "analyst", task: "Analyze code" },
    },
    {
      args: ["pi", "run", "script.ts"], // Não é um agente
      expected: null,
    },
  ];

  for (const testCase of testCases) {
    const result = extractAgentInfo(testCase.args);
    const match = result?.name === testCase.expected?.name;
    console.log(`Args: ${testCase.args.slice(0, 3).join(" ")}...`);
    console.log(`  Expected: ${testCase.expected?.name || "null"}`);
    console.log(`  Got: ${result?.name || "null"}`);
    console.log(`  ✓ ${match ? "PASS" : "FAIL"}\n`);
  }
}

// Função auxiliar (copiada do index.ts para teste)
function extractAgentInfo(args: string[]): { name: string; task: string; source: string } | null {
  const hasJSONMode = args.includes("--mode") && args.includes("json");
  const hasPrintFlag = args.includes("-p") || args.includes("--print");
  const hasNoExtensions = args.includes("--no-extensions");

  if (!hasJSONMode || !hasPrintFlag || !hasNoExtensions) {
    return null;
  }

  const promptIndex = args.indexOf("--append-system-prompt");
  if (promptIndex !== -1 && args[promptIndex + 1]) {
    const promptPath = args[promptIndex + 1];
    const match = promptPath.match(/prompt-([^.]+)\.md$/);
    if (match) {
      const agentName = match[1];
      const taskIndex = args.findLastIndex((arg, i) => !arg.startsWith("-") && i > promptIndex);
      const task = taskIndex !== -1 ? args[taskIndex] : "Running...";
      return { name: agentName, task, source: "unknown" };
    }
  }

  return null;
}

// Teste de layout responsiveness
function testLayoutResponsiveness() {
  console.log("\n=== Testing Layout Responsiveness ===\n");

  const testCases = [
    { layout: "1x8" as const, width: 120, expected: "1x8" },
    { layout: "1x8" as const, width: 100, expected: "list" }, // Fallback
    { layout: "1x4" as const, width: 80, expected: "1x4" },
    { layout: "1x4" as const, width: 60, expected: "list" }, // Fallback
    { layout: "list" as const, width: 40, expected: "list" },
  ];

  for (const tc of testCases) {
    // Simular getEffectiveLayout
    let result: AgentViewConfig["layout"] = tc.layout;
    if (tc.layout === "1x8" && tc.width < 120) result = "list";
    else if (tc.layout === "1x4" && tc.width < 80) result = "list";
    else if (tc.layout === "1x2" && tc.width < 60) result = "list";

    const match = result === tc.expected;
    console.log(`Layout: ${tc.layout}, Width: ${tc.width}`);
    console.log(`  Expected: ${tc.expected}`);
    console.log(`  Got: ${result}`);
    console.log(`  ✓ ${match ? "PASS" : "FAIL"}\n`);
  }
}

// Executar testes
console.log("╔════════════════════════════════════════════════════════╗");
console.log("║  Agent View Extension - Test Suite                    ║");
console.log("╚════════════════════════════════════════════════════════╝");

testAgentMonitor();
testArgumentParsing();
testLayoutResponsiveness();

console.log("\n=== All tests completed ===\n");
