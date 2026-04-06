/**
 * Hands-Free Voice Chat Extension for Pi
 *
 * A TRUE hands-free voice interface that:
 * - Activates immediately with /speak (no confirmation)
 * - Changes prompt to show voice mode is active
 * - Captures microphone automatically
 * - Transcribes speech (Deepgram)
 * - Sends to Pi for processing
 * - Speaks response (Cartesia TTS)
 * - Displays last sentence of response
 *
 * Usage:
 *   pi -e extensions/livekit.ts
 *   /speak
 *
 * Environment variables required in scripts/livekit-pi-extension/.env:
 *   DEEPGRAM_API_KEY=...
 *   CARTESIA_API_KEY=...
 *
 * Author: Pi Extension Framework
 * Created: 2026-04-06
 * Version: 2.0 - True Hands-Free
 */

import type { ExtensionAPI } from "@mariozechner/pi-coding-agent";
import { Type } from "@sinclair/typebox";
import { StringEnum } from "@mariozechner/pi-ai";
import { spawn, ChildProcess } from "child_process";
import { readFileSync, existsSync, writeFileSync, appendFileSync } from "fs";
import { join, resolve } from "path";
import { setTimeout as sleep } from "timers/promises";

// ============================================================================
// Types and State
// ============================================================================

type VoiceState =
	| "inactive"
	| "starting"
	| "listening"
	| "processing"
	| "speaking"
	| "error";

interface VoiceSession {
	state: VoiceState;
	process: ChildProcess | null;
	transcript: string;
	response: string;
	lastSentence: string;
	startTime: number;
}

// ============================================================================
// Configuration
// ============================================================================

const CONFIG = {
	scriptPath: resolve(process.cwd(), "scripts", "livekit-pi-extension", "simple_handsfree.py"),
	pythonCmd: "python",
};

// ============================================================================
// Extension Entry Point
// ============================================================================

export default function (pi: ExtensionAPI) {
	let session: VoiceSession | null = null;
	let statusWidget: any = null;

	// ------------------------------------------------------------------------
	// Voice Chat Tool
	// ------------------------------------------------------------------------

	pi.registerTool({
		name: "voice_chat",
		label: "Voice Chat",
		description: "Control hands-free voice chat. Use /speak to start, /un speak to stop.",
		parameters: Type.Object({
			action: StringEnum(["start", "stop", "status"] as const),
		}),

		async execute(_toolCallId, params, _signal, onUpdate, ctx) {
			const { action } = params as { action: "start" | "stop" | "status" };

			try {
				switch (action) {
					case "start":
						return await handleStart(ctx);
					case "stop":
						return await handleStop(ctx);
					case "status":
						return handleStatus();
				}
			} catch (error: any) {
				return {
					content: [{ type: "text", text: `Error: ${error.message}` }],
					details: { action, error: error.message },
				};
			}
		},

		renderCall(args, theme) {
			const params = args as { action: string };
			return new Text(
				theme.fg("toolTitle", theme.bold("voice_chat ")) +
				theme.fg("accent", params.action),
				0, 0,
			);
		},

		renderResult(result, _options, theme) {
			const details = result.details as { status?: string; error?: string } | undefined;
			if (!details) {
				return new Text(theme.fg("muted", "Voice chat action completed"), 0, 0);
			}

			if (details.error) {
				return new Text(theme.fg("error", `❌ ${details.error}`), 0, 0);
			}

			const statusColor = details.status === "listening" ? "success" : "muted";
			return new Text(
				theme.fg(statusColor, details.status || "Complete"),
				0, 0,
			);
		},
	});

	// ------------------------------------------------------------------------
	// Command Handlers
	// ------------------------------------------------------------------------

	pi.registerCommand("speak", {
		description: "Start hands-free voice mode immediately. No confirmation needed.",
		handler: async (_args, ctx) => {
			// DIRECTLY start voice mode - no confirmation, no message sending
			await startVoiceMode(ctx);
		},
	});

	pi.registerCommand("un speak", {
		description: "Stop hands-free voice mode",
		handler: async (_args, ctx) => {
			await stopVoiceMode(ctx);
		},
	});

	pi.registerCommand("speak-status", {
		description: "Show voice mode status",
		handler: async (_args, ctx) => {
			if (!session) {
				ctx.ui.notify("Voice mode is inactive", "info");
				return;
			}

			const uptime = Math.floor((Date.now() - session.startTime) / 1000);
			ctx.ui.notify(
				`State: ${session.state}\nUptime: ${uptime}s\nLast transcript: "${session.transcript}"`,
				"info",
			);
		},
	});

	// ------------------------------------------------------------------------
	// Core Functions
	// ------------------------------------------------------------------------

	async function startVoiceMode(ctx: any): Promise<void> {
		if (session && session.state !== "inactive") {
			ctx.ui.notify("Voice mode already active", "warning");
			return;
		}

		console.log("\n" + "=".repeat(60));
		console.log("🎤 STARTING HANDS-FREE VOICE MODE");
		console.log("=".repeat(60) + "\n");

		// Create temp file for Pi communication
		const commFile = join(process.cwd(), "scripts", "livekit-pi-extension", ".pi_comm.txt");
		writeFileSync(commFile, "", "utf-8");

		// Start the voice client
		const voiceProcess = spawn(CONFIG.pythonCmd, [CONFIG.scriptPath], {
			cwd: process.cwd(),
			stdio: ["ignore", "pipe", "pipe"],
			env: {
				...process.env,
				PI_MODE: "true",
			},
		});

		// Create session
		session = {
			state: "starting",
			process: voiceProcess,
			transcript: "",
			response: "",
			lastSentence: "",
			startTime: Date.now(),
		};

		// Handle output
		voiceProcess.stdout?.on("data", (data: Buffer) => {
			const output = data.toString().trim();
			console.log("[Voice Client]", output);
		});

		voiceProcess.stderr?.on("data", (data: Buffer) => {
			const error = data.toString().trim();
			console.error("[Voice Client Error]", error);
		});

		// Handle process exit
		voiceProcess.on("exit", (code) => {
			console.log(`[Voice Client] Exited with code ${code}`);
			if (session) {
				session.state = "inactive";
				session.process = null;
				updateStatusWidget(ctx);
			}
		});

		// Wait a bit for startup
		await sleep(1000);

		// Update state
		session.state = "listening";

		// Update UI
		updateStatusWidget(ctx);
		ctx.ui.notify("🎤 Voice mode ACTIVE - Speak now!", "success");

		// Start monitoring for communication
		startCommunicationMonitoring(ctx);
	}

	async function stopVoiceMode(ctx: any): Promise<void> {
		if (!session || session.state === "inactive") {
			ctx.ui.notify("Voice mode is not active", "warning");
			return;
		}

		console.log("\n" + "=".repeat(60));
		console.log("🛑 STOPPING HANDS-FREE VOICE MODE");
		console.log("=".repeat(60) + "\n");

		if (session.process) {
			session.process.kill("SIGTERM");
			session.process = null;
		}

		session.state = "inactive";
		updateStatusWidget(ctx);
		ctx.ui.notify("Voice mode stopped", "info");
	}

	function handleStatus() {
		if (!session || session.state === "inactive") {
			return {
				content: [{ type: "text", text: "Voice mode is inactive. Use /speak to start." }],
				details: { status: "inactive" },
			};
		}

		const uptime = Math.floor((Date.now() - session.startTime) / 1000);

		return {
			content: [{
				type: "text",
				text: `Voice Mode Status:\nState: ${session.state}\nUptime: ${uptime}s\nLast: "${session.lastSentence}"`,
			}],
			details: { status: session.state, uptime },
		};
	}

	async function handleStart(ctx: any) {
		await startVoiceMode(ctx);
		return {
			content: [{ type: "text", text: "🎤 Voice mode ACTIVATED. Speak now!" }],
			details: { status: "listening" },
		};
	}

	async function handleStop(ctx: any) {
		await stopVoiceMode(ctx);
		return {
			content: [{ type: "text", text: "Voice mode deactivated." }],
			details: { status: "inactive" },
		};
	}

	// ------------------------------------------------------------------------
	// Status Widget
	// ------------------------------------------------------------------------

	function updateStatusWidget(ctx: any): void {
		if (!session) return;

		const stateEmojis: Record<VoiceState, string> = {
			inactive: "⚫",
			starting: "🟡",
			listening: "🎤",
			processing: "⚙️",
			speaking: "🔊",
			error: "❌",
		};

		const emoji = stateEmojis[session.state] || "⚫";
		const statusText = session.state === "listening"
			? "Listening..."
			: session.state === "speaking"
			? "Speaking..."
			: session.state;

		// Update Pi's status line
		ctx.ui.setStatus("voice", `${emoji} Voice: ${statusText}`);

		// Update prompt if possible
		if (session.state === "listening") {
			// Try to change prompt (if Pi supports it)
			try {
				ctx.ui.setPrompt?.("🎤 Speak now... ");
			} catch {
				// Ignore if not supported
			}
		}
	}

	// ------------------------------------------------------------------------
	// Communication Monitoring
	// ------------------------------------------------------------------------

	function startCommunicationMonitoring(ctx: any): void {
		const commFile = join(process.cwd(), "scripts", "livekit-pi-extension", ".pi_comm.txt");

		// Monitor file for updates
		const interval = setInterval(async () => {
			if (!session || session.state === "inactive") {
				clearInterval(interval);
				return;
			}

			try {
				if (existsSync(commFile)) {
					const content = readFileSync(commFile, "utf-8").trim();

					if (content && content !== session.transcript) {
						// New transcript received
						session.transcript = content;

						console.log(`\n🎤 You said: "${content}"\n`);

						// Update state
						session.state = "processing";
						updateStatusWidget(ctx);

						// Send to Pi for processing
						pi.sendUserMessage(content, { deliverAs: "steer" });

						// Clear file
						writeFileSync(commFile, "", "utf-8");
					}
				}
			} catch (error) {
				console.error("Communication monitoring error:", error);
			}
		}, 500); // Check every 500ms
	}

	// ------------------------------------------------------------------------
	// Event Handlers
	// ------------------------------------------------------------------------

	pi.on("message_update", async (event, ctx) => {
		// Capture assistant responses for display
		if (!session || session.state === "inactive") return;

		const assistantEvent = event.assistantMessageEvent;
		if (assistantEvent?.type === "text_delta") {
			session.response += assistantEvent.delta;

			// Extract last sentence for display
			const lastSentence = extractLastSentence(session.response);

			if (lastSentence !== session.lastSentence) {
				session.lastSentence = lastSentence;
				console.log(`\n🤖 Assistant: ${lastSentence}\n`);
			}
		}
	});

	pi.on("message_end", async (event, ctx) => {
		if (!session || session.state === "inactive") return;

		const message = event.message;
		if (message?.role === "assistant") {
			// Response complete
			const lastSentence = extractLastSentence(session.response);
			session.lastSentence = lastSentence;

			console.log(`\n🤖 Assistant: ${lastSentence}\n`);

			// Send response to voice client for TTS
			const commFile = join(process.cwd(), "scripts", "livekit-pi-extension", ".pi_response.txt");
			writeFileSync(commFile, session.response, "utf-8");

			// Reset for next message
			session.response = "";

			// Return to listening
			await sleep(500);
			session.state = "listening";
			updateStatusWidget(ctx);
		}
	});

	pi.on("session_shutdown", async () => {
		if (session && session.process) {
			session.process.kill("SIGTERM");
		}
	});

	// ------------------------------------------------------------------------
	// Initialization
	// ------------------------------------------------------------------------

	pi.on("session_start", async (_event, ctx) => {
		ctx.ui.notify("Hands-free voice chat loaded. Use /speak to start.", "info");
	});
}

// ============================================================================
// Helper Functions
// ============================================================================

function extractLastSentence(text: string): string {
	// Remove thinking tags
	let cleaned = text.replace(/<thinking>[\s\S]*?<\/thinking>/gi, "").trim();

	// Remove code blocks
	cleaned = cleaned.replace(/```[\s\S]*?```/g, "").trim();

	// Split on sentence boundaries
	const sentences = cleaned.match(/[^.!?]*[.!?]+|[^.!?]+$/g) || [cleaned];

	// Get last non-empty sentence
	for (let i = sentences.length - 1; i >= 0; i--) {
		const sentence = sentences[i]?.trim();
		if (sentence && sentence.length > 0) {
			return sentence.substring(0, 100);
		}
	}

	return cleaned.substring(0, 100);
}
