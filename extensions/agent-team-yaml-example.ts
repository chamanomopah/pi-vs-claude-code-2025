/**
 * Agent Team — YAML Shortcuts Example
 *
 * This demonstrates how to use the shortcutLoader helper to register
 * shortcuts from .pi/agents/shortcuts.yaml instead of hardcoding them.
 */

import type { ExtensionAPI } from "@mariozechner/pi-coding-agent";
import { registerShortcuts, loadShortcuts } from "./shortcutLoader.ts";

export default function (pi: ExtensionAPI) {
	// ... rest of the extension code ...

	// Register shortcuts from YAML in session_start
	pi.on("session_start", async (_event, _ctx) => {
		// ... other initialization code ...

		// Register shortcuts from .pi/agents/shortcuts.yaml
		registerShortcuts(pi, "agent-team", {
			"f6": {
				handler: async (_ctx) => {
					if (!_ctx.hasUI) return;
					cycleTeam(1);
				},
			},
			"f7": {
				handler: async (_ctx) => {
					if (!_ctx.hasUI) return;
					cycleTeam(-1);
				},
			},
		}, _ctx.cwd);

		// Debug: log loaded shortcuts
		const loadedShortcuts = loadShortcuts("agent-team", _ctx.cwd);
		console.log(`[agent-team] Loaded ${loadedShortcuts.size} shortcut(s)`);
	});
}
