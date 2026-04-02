/**
 * Prompt Timer — Measure response time for user prompts
 *
 * Displays the elapsed time between user input and assistant response
 * in a small widget. Format: ⏱️ <elapsed>s
 *
 * Events tracked:
 *   - input: Captures when user submits input
 *   - agent_end: Captures when agent finishes responding
 *
 * Usage: pi -e extensions/prompt-timer.ts
 */

import type { ExtensionAPI, TUI } from "@mariozechner/pi-coding-agent";
import { Text } from "@mariozechner/pi-tui";
import { applyExtensionDefaults } from "./themeMap.ts";

export default function (pi: ExtensionAPI) {
	// Use a mutable object so the widget always reads the current value
	const state = {
		startTime: null as number | null,
		pending: false,
		timerText: "⏱️ ready",
	};

	let tui: TUI | null = null;
	let textComponent: Text | null = null;

	// Start timer when user submits input
	pi.on("input", async (_event) => {
		state.startTime = Date.now();
		state.pending = true;
		state.timerText = "⏱️ calculating...";
		if (tui) tui.requestRender();
	});

	// Calculate and display elapsed time when agent finishes
	pi.on("agent_end", async (_event) => {
		if (!state.pending || state.startTime === null) {
			return;
		}

		const elapsedMs = Date.now() - state.startTime;
		const elapsedSec = (elapsedMs / 1000).toFixed(1);
		state.timerText = `⏱️ ${elapsedSec}s`;

		// Reset for next prompt
		state.startTime = null;
		state.pending = false;

		if (tui) tui.requestRender();
	});

	// Initialize extension on session start
	pi.on("session_start", async (_event, ctx) => {
		applyExtensionDefaults(import.meta.url, ctx);

		// Set up a small widget for the timer using Text component
		ctx.ui.setWidget("prompt-timer", (__tui, theme) => {
			tui = __tui;
			textComponent = new Text("", 0, 0);

			return {
				render(width: number): string[] {
					// Update text content with current state
					if (textComponent) {
						textComponent.setText(theme.fg("muted", state.timerText));
						return textComponent.render(width);
					}
					return [`  ${theme.fg("muted", state.timerText)}`];
				},
				invalidate() {
					if (textComponent) textComponent.invalidate();
				},
			};
		}, { placement: "belowEditor" });
	});

	// Clean up on session shutdown
	pi.on("session_shutdown", async () => {
		state.startTime = null;
		state.pending = false;
		tui = null;
		textComponent = null;
	});
}
