/**
 * Shortcut Diagnostic — Test and validate keyboard shortcuts
 * 
 * Usage: pi -e extensions/shortcut-diagnostic.ts
 * Command: /test-shortcuts
 */

import type { ExtensionAPI } from "@mariozechner/pi-coding-agent";
import { isKittyProtocolActive } from "@mariozechner/pi-tui";

export default function (pi: ExtensionAPI) {
	pi.on("session_start", async (_event, ctx) => {
		pi.registerCommand("test-shortcuts", {
			description: "Diagnose keyboard shortcuts and terminal capabilities",
			handler: async (_args, ctx) => {
				const kittyActive = isKittyProtocolActive();
				
				console.log("\n" + "=".repeat(60));
				console.log("      KEYBOARD SHORTCUTS DIAGNOSTIC REPORT");
				console.log("=".repeat(60));
				console.log(`\nKitty Keyboard Protocol: ${kittyActive ? "ACTIVE" : "INACTIVE"}`);
				
				if (!kittyActive) {
					console.log("\n⚠️  WARNING: Kitty protocol is inactive.");
					console.log("    Some key combinations (like alt+shift+i) may not work.");
					console.log("\n    To enable Kitty protocol, use a terminal that supports it:");
					console.log("    • Kitty Terminal: Built-in support");
					console.log("    • WezTerm: enable_kitty_keyboard = true");
					console.log("    • Ghostty: Default enabled");
					console.log("    • VS Code: terminal.integrated.enableKittyKeyboard = true");
				}
				
				console.log("\n" + "-".repeat(60));
				console.log("Loaded shortcuts from .pi/agents/shortcuts.yaml:");
				console.log("-".repeat(60));
				
				// Import getAllShortcuts dynamically
				const { getAllShortcuts, getShortcutInfo } = await import("./shortcutLoader.ts");
				const allShortcuts = getAllShortcuts(ctx.cwd);
				
				if (allShortcuts.size === 0) {
					console.log("No shortcuts found.");
				} else {
					for (const [extName, shortcuts] of allShortcuts) {
						console.log(`\n[${extName}] (${shortcuts.size} shortcut(s))`);
						for (const [keyId, actionOrDesc] of shortcuts) {
							const info = getShortcutInfo(keyId);
							let status = "✓";
							if (info.kittyInfo.required && !kittyActive) status = "⚠️ ";
							
							console.log(`  ${status} ${keyId} -> ${actionOrDesc || "(no action)"}`);
							if (info.kittyInfo.required && !kittyActive) {
								console.log(`      Needs Kitty: ${info.kittyInfo.reason}`);
							}
						}
					}
				}
				
				console.log("\n" + "=".repeat(60) + "\n");
				
				if (ctx.hasUI) {
					ctx.ui.notify("Diagnostic complete - see console", "info");
				}
				return;
			},
		});

		ctx.ui.notify("Shortcut Diagnostic loaded! Run /test-shortcuts", "info");
	});
}
