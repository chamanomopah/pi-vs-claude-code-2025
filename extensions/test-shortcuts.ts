/**
 * Test Shortcuts — Example extension demonstrating YAML shortcut loading
 *
 * This is a minimal example showing how to use the shortcutLoader helper.
 * Usage: pi -e extensions/test-shortcuts.ts
 *
 * Shortcuts defined in .pi/agents/shortcuts.yaml:
 *   test-shortcuts:
 *     - f8   # Show notification
 *     - f9   # Log to console
 *     - f10  # Show current shortcuts
 */

import type { ExtensionAPI } from "@mariozechner/pi-coding-agent";
import { registerShortcuts, loadShortcuts, getAllShortcuts } from "./shortcutLoader.ts";

export default function (pi: ExtensionAPI) {
	let currentCtx: any = undefined;

	// Define the handlers
	const handlers = {
		"f8": {
			description: "Show test notification",
			handler: async (ctx: any) => {
				if (!ctx.hasUI) return;
				ctx.ui.notify("Test shortcut F8 pressed!", "info");
			},
		},
		"f9": {
			description: "Log test message",
			handler: async (ctx: any) => {
				console.log("[test-shortcuts] F9 pressed - handler executed!");
			},
		},
		"f10": {
			description: "List all loaded shortcuts",
			handler: async (ctx: any) => {
				if (!ctx.hasUI) return;
				
				const allShortcuts = getAllShortcuts(ctx.cwd);
				let message = `Loaded ${allShortcuts.size} extension(s):\n`;
				
				for (const [extName, shortcuts] of allShortcuts) {
					message += `\n[${extName}] (${shortcuts.size} shortcut(s))\n`;
					for (const [keyId, desc] of shortcuts) {
						message += `  ${keyId}${desc ? ": " + desc : ""}\n`;
					}
				}
				
				console.log(message);
				ctx.ui.notify("See console for all shortcuts", "info");
			},
		},
	};

	pi.on("session_start", async (_event, _ctx) => {
		currentCtx = _ctx;

		// Register shortcuts from YAML
		registerShortcuts(pi, "test-shortcuts", handlers, _ctx.cwd);

		// Log what we loaded
		const loaded = loadShortcuts("test-shortcuts", _ctx.cwd);
		console.log(`[test-shortcuts] Loaded ${loaded.size} shortcut(s):`);
		for (const [keyId, desc] of loaded) {
			console.log(`  ${keyId}: ${desc || "(no description in YAML)"}`);
		}

		_ctx.ui.notify(
			`Test Shortcuts loaded!\n` +
			`Press F8 for notification, F9 to log, F10 to list all`,
			"info"
		);
	});

	pi.on("session_shutdown", async () => {
		console.log("[test-shortcuts] Session ended");
	});
}
