/**
 * Image Gallery Extension
 *
 * Features:
 * 1. Widget no terminal mostrando a imagem atual
 * 2. Tool para agentes atualizarem o caminho da imagem
 * 3. Histórico de versões armazenado em session entries
 * 4. Visualização de imagem com renderização (terminal suportado)
 *
 * Usage:
 *   - Agent: "Show image at /path/to/image.png"
 *   - Command: /gallery [next|prev|n|p|view]
 *   - Shortcuts: Ctrl+Alt+Right (next), Ctrl+Alt+Left (prev)
 */

import type { ExtensionAPI, ExtensionContext, Theme } from "@mariozechner/pi-coding-agent";
import { Container, Image, Key, matchesKey, Spacer, Text } from "@mariozechner/pi-tui";
import { Type } from "@sinclair/typebox";
import { readFileSync } from "node:fs";

interface ImageDetails {
	imagePath: string | null;
	history: string[];
	position: number;
	timestamp: number;
}

function imageToBase64(path: string): { data: string; mimeType: string } | null {
	try {
		const buffer = readFileSync(path);
		const base64 = buffer.toString("base64");
		const ext = path.split(".").pop()?.toLowerCase();
		const mimeTypes: Record<string, string> = {
			png: "image/png",
			jpg: "image/jpeg",
			jpeg: "image/jpeg",
			gif: "image/gif",
			webp: "image/webp"
		};
		return { data: base64, mimeType: mimeTypes[ext || "png"] || "image/png" };
	} catch {
		return null;
	}
}

const GalleryParams = Type.Object({
	action: Type.String({ description: "Action: 'show' to display image, 'next'/'prev' for history" }),
	path: Type.Optional(Type.String({ description: "Image path to display" })),
});

export default function imageGalleryExtension(pi: ExtensionAPI) {
	let currentPath: string | null = null;
	let history: string[] = [];
	let position = -1;

	const reconstructState = (ctx: ExtensionContext) => {
		currentPath = null;
		history = [];
		position = -1;

		for (const entry of ctx.sessionManager.getBranch()) {
			if (entry.type === "message" && 
			    entry.message.role === "toolResult" && 
			    entry.message.toolName === "gallery") {
				const details = entry.message.details as ImageDetails | undefined;
				if (details) {
					currentPath = details.imagePath;
					history = details.history;
					position = details.position;
				}
			}
		}
		
		updateWidget(ctx);
	};

	const updateWidget = (ctx: ExtensionContext) => {
		if (!ctx.hasUI) return;

		if (currentPath) {
			const histInfo = history.length > 0 
				? `[${position + 1}/${history.length}]` 
				: "";
			ctx.ui.setWidget("image-gallery", [
				`🖼️  ${currentPath} ${histInfo}`,
				"Use /gallery to navigate history"
			]);
		} else {
			ctx.ui.setWidget("image-gallery", undefined);
		}
	};

	pi.on("session_start", async (_event, ctx) => {
		reconstructState(ctx);
	});

	pi.on("session_switch", async (_event, ctx) => {
		reconstructState(ctx);
	});

	pi.on("session_fork", async (_event, ctx) => {
		reconstructState(ctx);
	});

	pi.on("session_tree", async (_event, ctx) => {
		reconstructState(ctx);
	});

	pi.registerTool({
		name: "gallery",
		label: "Image Gallery",
		description: "Display an image in the terminal widget. Actions: 'show' (with path), 'next', 'prev'. Use to show and navigate through images.",
		parameters: GalleryParams,

		async execute(_toolCallId, params, _signal, _onUpdate, ctx) {
			switch (params.action) {
				case "show": {
					if (!params.path) {
						return {
							content: [{ type: "text", text: "Error: path required for show action" }],
							details: { imagePath: currentPath, history: [...history], position, timestamp: Date.now() } as ImageDetails,
						};
					}

					if (currentPath !== params.path) {
						if (position < history.length - 1) {
							history = history.slice(0, position + 1);
						}
						history.push(params.path);
						position = history.length - 1;
					}

					currentPath = params.path;
					updateWidget(ctx);

					return {
						content: [{ type: "text", text: `Displaying image: ${currentPath}` }],
						details: { imagePath: currentPath, history: [...history], position, timestamp: Date.now() } as ImageDetails,
					};
				}

				case "next": {
					if (history.length === 0 || position >= history.length - 1) {
						return {
							content: [{ type: "text", text: "No more images in history" }],
							details: { imagePath: currentPath, history: [...history], position, timestamp: Date.now() } as ImageDetails,
						};
					}
					position++;
					currentPath = history[position];
					updateWidget(ctx);

					return {
						content: [{ type: "text", text: `Next image: ${currentPath}` }],
						details: { imagePath: currentPath, history: [...history], position, timestamp: Date.now() } as ImageDetails,
					};
				}

				case "prev": {
					if (history.length === 0 || position <= 0) {
						return {
							content: [{ type: "text", text: "No previous images" }],
							details: { imagePath: currentPath, history: [...history], position, timestamp: Date.now() } as ImageDetails,
						};
					}
					position--;
					currentPath = history[position];
					updateWidget(ctx);

					return {
						content: [{ type: "text", text: `Previous image: ${currentPath}` }],
						details: { imagePath: currentPath, history: [...history], position, timestamp: Date.now() } as ImageDetails,
					};
				}

				case "view": {
					if (!currentPath) {
						return {
							content: [{ type: "text", text: "No image to view. Use 'show' action first" }],
							details: { imagePath: currentPath, history: [...history], position, timestamp: Date.now() } as ImageDetails,
						};
					}

					const imageData = imageToBase64(currentPath);
					if (!imageData) {
						return {
							content: [{ type: "text", text: `Error: Could not read image file: ${currentPath}` }],
							details: { imagePath: currentPath, history: [...history], position, timestamp: Date.now() } as ImageDetails,
						};
					}

					return {
						content: [
							{ type: "text", text: `Displaying: ${currentPath}` }
						],
						details: { imagePath: currentPath, history: [...history], position, timestamp: Date.now() } as ImageDetails,
					};
				}

				default:
					return {
						content: [{ type: "text", text: `Unknown action: ${params.action}. Use: show, next, or prev` }],
						details: { imagePath: currentPath, history: [...history], position, timestamp: Date.now() } as ImageDetails,
					};
			}
		},

		renderCall(args, theme) {
			let text = theme.fg("toolTitle", theme.bold("gallery ")) + theme.fg("muted", args.action);
			if (args.path) {
				text += " " + theme.fg("dim", `"${args.path}"`);
			}
			return new Text(text, 0, 0);
		},

		renderResult(result, { expanded }, theme) {
			const details = result.details as ImageDetails;
			if (!details) {
				const text = result.content[0];
				return new Text(text?.type === "text" ? text.text : "", 0, 0);
			}

			let output = theme.fg("success", "🖼️  ");
			if (details.imagePath) {
				output += theme.fg("accent", details.imagePath);
			} else {
				output += theme.fg("dim", "No image");
			}

			if (expanded && details.history.length > 0) {
				output += "\n" + theme.fg("muted", "History:");
				for (let i = 0; i < details.history.length; i++) {
					const prefix = i === details.position ? theme.fg("accent", "→") : " ";
					const item = i === details.position 
						? theme.fg("accent", details.history[i]!)
						: theme.fg("dim", details.history[i]!);
					output += "\n  " + prefix + " " + item;
				}
			}

			return new Text(output, 0, 0);
		},
	});

	pi.registerCommand("gallery", {
		description: "Navigate image gallery history. Usage: /gallery [next|prev|n|p|view]",
		handler: async (args, ctx) => {
			if (!ctx.hasUI) {
				ctx.ui.notify("Gallery requires interactive mode", "error");
				return;
			}

			if (history.length === 0 && args?.toLowerCase() !== "view") {
				ctx.ui.notify("No images in history. Use gallery tool first", "warning");
				return;
			}

			const action = args?.toLowerCase().trim();

			if (action === "next" || action === "n") {
				if (position < history.length - 1) {
					position++;
					currentPath = history[position];
					updateWidget(ctx);
					ctx.ui.notify("Next: " + currentPath + " [" + (position + 1) + "/" + history.length + "]", "info");
				} else {
					ctx.ui.notify("No more images in history", "warning");
				}
			} else if (action === "prev" || action === "p") {
				if (position > 0) {
					position--;
					currentPath = history[position];
					updateWidget(ctx);
					ctx.ui.notify("Previous: " + currentPath + " [" + (position + 1) + "/" + history.length + "]", "info");
				} else {
					ctx.ui.notify("No previous images in history", "warning");
				}
			} else if (action === "view") {
				if (!currentPath) {
					ctx.ui.notify("No image to view. Use gallery tool first", "warning");
					return;
				}
				const imageData = imageToBase64(currentPath);
				if (!imageData) {
					ctx.ui.notify("Could not read image: " + currentPath, "error");
					return;
				}

				// Use ctx.ui.custom with proper callback signature
				ctx.ui.custom((tui, theme, _keybindings, done) => {
					const container = new Container();

					// Title
					container.addChild(new Text(theme.fg("accent", theme.bold("🖼️  Image Viewer")), 1, 0));
					container.addChild(new Spacer(1));

					// Image
					const image = new Image(
						imageData.data,
						imageData.mimeType,
						theme,
						{ maxWidthCells: 80, maxHeightCells: 25 }
					);
					container.addChild(image);

					container.addChild(new Spacer(1));

					// Footer instructions
					container.addChild(new Text(theme.fg("dim", currentPath!), 1, 0));
					container.addChild(new Text(theme.fg("muted", "Press ESC to close"), 1, 0));

					return {
						render: (width) => container.render(width),
						invalidate: () => container.invalidate(),
						handleInput: (data) => {
							if (matchesKey(data, Key.escape)) {
								done(null);
							}
						},
					};
				});
			} else if (action === "" || action === undefined) {
				const info = currentPath
					? "Current: " + currentPath + " [" + (position + 1) + "/" + history.length + "]"
					: "No image";
				ctx.ui.notify(info, "info");
			} else {
				ctx.ui.notify("Usage: /gallery [next|prev|n|p|view]", "warning");
			}
		},
	});

	pi.registerShortcut("ctrl+alt+right", {
		description: "Next image in gallery",
		handler: async (ctx) => {
			if (history.length > 0 && position < history.length - 1) {
				position++;
				currentPath = history[position];
				updateWidget(ctx);
				ctx.ui.notify("→ " + currentPath, "info");
			}
		},
	});

	pi.registerShortcut("ctrl+alt+left", {
		description: "Previous image in gallery",
		handler: async (ctx) => {
			if (history.length > 0 && position > 0) {
				position--;
				currentPath = history[position];
				updateWidget(ctx);
				ctx.ui.notify("← " + currentPath, "info");
			}
		},
	});
}
