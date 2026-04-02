/**
 * Shortcut Loader — Action-based shortcut registration from .pi/agents/shortcuts.yaml
 *
 * NEW APPROACH: YAML defines which keys, code defines what to do.
 *
 * shortcuts.yaml format:
 *   extension-name:
 *     - keyId    # action-name (description as comment)
 *
 * The comment after keyId is parsed as "action-name" if it matches a known action.
 * This allows mapping YAML shortcuts to handler functions by action name.
 *
 * FEATURES:
 * - Normalizes modifier order (alt+shift+i -> alt+shift+i)
 * - Validates key IDs and warns about potential issues
 * - Detects Kitty protocol support requirements
 * - Supports any modifier combination
 *
 * Usage:
 *   import { registerActionShortcuts } from "./shortcutLoader.ts";
 *
 *   registerActionShortcuts(pi, "agent-team", {
 *     "next-team": {
 *       description: "Cycle to next team",
 *       handler: async (ctx) => cycleTeam(1)
 *     },
 *     "prev-team": {
 *       description: "Cycle to previous team", 
 *       handler: async (ctx) => cycleTeam(-1)
 *     },
 *   }, ctx.cwd);
 *
 * YAML example:
 *   agent-team:
 *     - f6   # next-team
 *     - alt+shift+i   # prev-team (any modifier order works!)
 */

import { isKittyProtocolActive } from "@mariozechner/pi-tui";

export interface ShortcutMap extends Map<string, string> {
	// keyId -> description (can be action name)
}

// Valid base keys
const VALID_LETTERS = new Set(["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]);
const VALID_NUMBERS = new Set(["0","1","2","3","4","5","6","7","8","9"]);
const VALID_SPECIAL = new Set(["escape","esc","enter","return","tab","space","backspace","delete","insert","clear","home","end","pageup","pagedown","up","down","left","right","f1","f2","f3","f4","f5","f6","f7","f8","f9","f10","f11","f12"]);
const VALID_SYMBOLS = new Set(["`","-","=","[","]","\\",";","'",",",".","/","!","@","#","$","%","^","&","*","(",")","_","+","|","~","{","}",":","<",">","?"]);

// Valid modifiers
const VALID_MODIFIERS = new Set(["ctrl", "shift", "alt"]);

/**
 * Normalize a keyId to canonical form
 * - Sorts modifiers alphabetically: alt+shift+i -> alt+shift+i
 * - Converts to lowercase
 * - Handles special cases
 */
export function normalizeKeyId(keyId: string): string {
	const parts = keyId.toLowerCase().split("+").map(p => p.trim());
	
	// Separate modifiers from the base key
	const modifiers: string[] = [];
	const baseKeys: string[] = [];
	
	for (const part of parts) {
		if (VALID_MODIFIERS.has(part)) {
			modifiers.push(part);
		} else {
			baseKeys.push(part);
		}
	}
	
	if (baseKeys.length === 0) {
		return keyId; // Invalid, but return as-is
	}
	
	// Sort modifiers alphabetically for consistency
	modifiers.sort();
	
	// Join back together
	return [...modifiers, ...baseKeys].join("+");
}

/**
 * Check if a keyId requires Kitty protocol to work reliably
 */
export function requiresKittyProtocol(keyId: string): { required: boolean; reason: string } {
	const normalized = normalizeKeyId(keyId);
	const parts = normalized.split("+");
	const modifiers = parts.slice(0, -1);
	const baseKey = parts[parts.length - 1];
	
	const hasShift = modifiers.includes("shift");
	const hasAlt = modifiers.includes("alt");
	const hasCtrl = modifiers.includes("ctrl");
	const modCount = modifiers.length;
	
	// Single modifiers or special keys usually work
	if (modCount === 0) {
		return { required: false, reason: "base key" };
	}
	
	// Letters with multiple modifiers need Kitty
	if (VALID_LETTERS.has(baseKey)) {
		if (modCount >= 2) {
			return { required: true, reason: `${baseKey} with ${modCount} modifiers needs Kitty` };
		}
	}
	
	// Arrows with multiple modifiers need Kitty
	if (["up", "down", "left", "right"].includes(baseKey)) {
		if (modCount >= 2) {
			return { required: true, reason: `arrow with ${modCount} modifiers needs Kitty` };
		}
	}
	
	return { required: false, reason: "has legacy fallback" };
}

/**
 * Validate a keyId and return validation result
 */
export function validateKeyId(keyId: string): { valid: boolean; error?: string; warning?: string } {
	const normalized = normalizeKeyId(keyId);
	const parts = normalized.split("+");
	const modifiers = parts.slice(0, -1);
	const baseKey = parts[parts.length - 1];
	
	// Check for empty parts
	if (parts.some(p => p === "")) {
		return { valid: false, error: "Empty part in keyId" };
	}
	
	// Check for duplicate modifiers
	const seenMods = new Set<string>();
	for (const mod of modifiers) {
		if (seenMods.has(mod)) {
			return { valid: false, error: `Duplicate modifier: ${mod}` };
		}
		seenMods.add(mod);
	}
	
	// Validate base key
	const baseLower = baseKey.toLowerCase();
	if (!VALID_LETTERS.has(baseLower) && 
	    !VALID_NUMBERS.has(baseLower) && 
	    !VALID_SPECIAL.has(baseLower) && 
	    !VALID_SYMBOLS.has(baseLower)) {
		return { valid: false, error: `Invalid base key: ${baseKey}` };
	}
	
	// Check for Kitty requirement
	const kittyCheck = requiresKittyProtocol(normalized);
	if (kittyCheck.required) {
		const kittyActive = isKittyProtocolActive();
		if (!kittyActive) {
			return { 
				valid: true, 
				warning: `Requires Kitty protocol (${kittyCheck.reason})` 
			};
		}
	}
	
	return { valid: true };
}

/**
 * Parse shortcuts.yaml file with normalization and validation
 */
export function parseShortcutsYaml(raw: string): Map<string, ShortcutMap> {
	const normalized = raw.replace(/\r\n/g, "\n").replace(/\r/g, "\n");
	const shortcuts = new Map<string, ShortcutMap>();
	let currentExtension: string | null = null;
	let lineNumber = 0;

	for (const line of normalized.split("\n")) {
		lineNumber++;
		const trimmed = line.trim();
		if (!trimmed || trimmed.startsWith("#")) continue;

		const extMatch = line.match(/^(\S[^:]*):$/);
		if (extMatch) {
			currentExtension = extMatch[1].trim();
			if (!shortcuts.has(currentExtension)) {
				shortcuts.set(currentExtension, new Map());
			}
			continue;
		}

		const itemMatch = line.match(/^\s+-\s+(\S+?)(\s+#\s*(.+))?$/);
		if (itemMatch && currentExtension) {
			const rawKeyId = itemMatch[1].trim();
			let actionOrDesc = itemMatch[3]?.trim() || "";
			// Extract action name from "action-name (Description)" format
			const parenIndex = actionOrDesc.indexOf("(");
			if (parenIndex > 0) {
			  actionOrDesc = actionOrDesc.substring(0, parenIndex).trim();
			}
			const normalizedKeyId = normalizeKeyId(rawKeyId);
			const validation = validateKeyId(normalizedKeyId);
			
			if (!validation.valid) {
				console.error(`[shortcutLoader] Line ${lineNumber}: ${validation.error} - "${rawKeyId}"`);
				continue;
			}
			
			if (validation.warning) {
				console.warn(`[shortcutLoader] Line ${lineNumber}: ${normalizedKeyId} - ${validation.warning}`);
			}
			
			if (rawKeyId !== normalizedKeyId) {
				console.log(`[shortcutLoader] Normalized: "${rawKeyId}" -> "${normalizedKeyId}"`);
			}
			
			const extMap = shortcuts.get(currentExtension);
			if (extMap) {
				extMap.set(normalizedKeyId, actionOrDesc);
			}
		}
	}

	return shortcuts;
}

/**
 * Load shortcuts from .pi/agents/shortcuts.yaml for a specific extension
 */
export function loadShortcuts(extensionName: string, cwd: string): ShortcutMap {
	try {
		const { readFileSync, existsSync } = require("fs");
		const { join } = require("path");
		const shortcutsPath = join(cwd, ".pi", "agents", "shortcuts.yaml");
		if (!existsSync(shortcutsPath)) return new Map();
		const raw = readFileSync(shortcutsPath, "utf-8");
		const allShortcuts = parseShortcutsYaml(raw);
		return allShortcuts.get(extensionName) || new Map();
	} catch {
		return new Map();
	}
}

/**
 * Register shortcuts from YAML using action-based handlers
 */
export function registerActionShortcuts(
	pi: any,
	extensionName: string,
	actions: Record<string, { description: string; handler: (ctx: any) => void | Promise<void> }>,
	cwd: string,
): void {
	const yamlShortcuts = loadShortcuts(extensionName, cwd);
	if (yamlShortcuts.size === 0) return;

	console.log(`[shortcutLoader] Registering ${yamlShortcuts.size} shortcut(s) for ${extensionName}`);

	for (const [keyId, actionOrDesc] of yamlShortcuts) {
		const action = actions[actionOrDesc];
		if (action) {
			try {
				pi.registerShortcut(keyId, {
					description: action.description,
					handler: action.handler,
				});
				console.log(`[shortcutLoader] ✓ ${keyId} -> ${actionOrDesc}`);
			} catch (err) {
				console.error(`[shortcutLoader] ✗ Failed to register ${keyId}: ${err}`);
			}
		} else {
			console.warn(`[shortcutLoader] ⚠ No handler for "${actionOrDesc}" on key "${keyId}"`);
		}
	}
}

/**
 * Get all shortcuts from .pi/agents/shortcuts.yaml
 */
export function getAllShortcuts(cwd: string): Map<string, ShortcutMap> {
	try {
		const { readFileSync, existsSync } = require("fs");
		const { join } = require("path");
		const shortcutsPath = join(cwd, ".pi", "agents", "shortcuts.yaml");
		if (!existsSync(shortcutsPath)) return new Map();
		const raw = readFileSync(shortcutsPath, "utf-8");
		return parseShortcutsYaml(raw);
	} catch {
		return new Map();
	}
}

/**
 * Get detailed information about a shortcut key
 */
export function getShortcutInfo(keyId: string): {
	normalized: string;
	parts: { modifiers: string[]; baseKey: string };
	validation: ReturnType<typeof validateKeyId>;
	kittyInfo: ReturnType<typeof requiresKittyProtocol>;
} {
	const normalized = normalizeKeyId(keyId);
	const parts = normalized.split("+");
	const modifiers = parts.slice(0, -1);
	const baseKey = parts[parts.length - 1];
	
	return {
		normalized,
		parts: { modifiers, baseKey },
		validation: validateKeyId(normalized),
		kittyInfo: requiresKittyProtocol(normalized),
	};
}
