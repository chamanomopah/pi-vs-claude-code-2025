#!/usr/bin/env tsx
/**
 * Fix Agent Teams List - Script Interativo
 *
 * Resolve o problema de agentes não aparecerem na lista "Members with skills"
 * da extensão Agent Teams.
 *
 * Opções:
 *   A) Adicionar campo `skills` padrão aos agentes que não têm
 *   B) Modificar agent-team.ts para remover o filtro de skills
 *   C) Gerar relatório de agentes com/sem skills
 *
 * Uso: bun run scripts/fix-agent-teams-list.ts
 */

import { readFileSync, writeFileSync, existsSync, mkdirSync, readdirSync, statSync } from "fs";
import { join, resolve, dirname } from "path";
import { spawnSync } from "child_process";

// ── Tipos ─────────────────────────────────────────────────────

interface AgentInfo {
	name: string;
	file: string;
	hasSkills: boolean;
	skills: string[];
	frontmatter: Record<string, any>;
}

interface BackupInfo {
	originalPath: string;
	backupPath: string;
	timestamp: string;
}

// ── Utilitários de UI ──────────────────────────────────────────

const colors = {
	reset: "\x1b[0m",
	bright: "\x1b[1m",
	dim: "\x1b[2m",
	red: "\x1b[31m",
	green: "\x1b[32m",
	yellow: "\x1b[33m",
	blue: "\x1b[34m",
	magenta: "\x1b[35m",
	cyan: "\x1b[36m",
};

function style(color: keyof typeof colors, text: string): string {
	return `${colors[color]}${text}${colors.reset}`;
}

function printHeader(title: string) {
	console.log("\n" + style("cyan", "═".repeat(60)));
	console.log(style("bright", `  ${title}`));
	console.log(style("cyan", "═".repeat(60)) + "\n");
}

function printSuccess(message: string) {
	console.log(style("green", `✓ ${message}`));
}

function printError(message: string) {
	console.log(style("red", `✗ ${message}`));
}

function printWarning(message: string) {
	console.log(style("yellow", `⚠ ${message}`));
}

function printInfo(message: string) {
	console.log(style("blue", `ℹ ${message}`));
}

// ── Utilitários de File System ──────────────────────────────────

function ensureDir(path: string): void {
	if (!existsSync(path)) {
		mkdirSync(path, { recursive: true });
	}
}

function createBackup(filePath: string): string {
	const backupDir = join(process.cwd(), ".pi", "backups");
	ensureDir(backupDir);

	const timestamp = new Date().toISOString().replace(/[:.]/g, "-").slice(0, -5);
	const filename = `${basename(filePath)}_${timestamp}.bak`;
	const backupPath = join(backupDir, filename);

	const content = readFileSync(filePath, "utf-8");
	writeFileSync(backupPath, content, "utf-8");

	return backupPath;
}

function basename(path: string): string {
	return path.split(/[\\/]/).pop() || "";
}

// ── Parser de Frontmatter ───────────────────────────────────────

function parseFrontmatter(filePath: string): { frontmatter: Record<string, any>; content: string; raw: string } | null {
	try {
		const raw = readFileSync(filePath, "utf-8");
		const match = raw.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n([\s\S]*)$/);
		if (!match) return null;

		const frontmatter: Record<string, any> = {};
		const lines = match[1].split(/\r?\n/);
		let currentArray: string[] | null = null;
		let currentKey: string | null = null;

		for (const line of lines) {
			const idx = line.indexOf(":");
			if (idx > 0) {
				const key = line.slice(0, idx).trim();
				const value = line.slice(idx + 1).trim();
				currentKey = key;
				currentArray = null;

				if (value === "") {
					currentArray = [];
					frontmatter[key] = currentArray;
				} else {
					frontmatter[key] = value;
				}
			} else if (currentArray && currentKey) {
				const itemMatch = line.match(/^\s+-\s+(.+)$/);
				if (itemMatch) {
					currentArray.push(itemMatch[1].trim());
				}
			}
		}

		return { frontmatter, content: match[2], raw };
	} catch {
		return null;
	}
}

// ── Scanner de Agentes ─────────────────────────────────────────

function scanAgentFiles(cwd: string): AgentInfo[] {
	const agentDirs = [
		join(cwd, "agents"),
		join(cwd, ".claude", "agents"),
		join(cwd, ".pi", "agents"),
	];

	const agents: AgentInfo[] = [];
	const seen = new Set<string>();

	function scanDirectory(dir: string, pathPrefix: string = ""): void {
		if (!existsSync(dir)) return;

		try {
			const entries = readdirSync(dir, { withFileTypes: true });
			for (const entry of entries) {
				const fullPath = resolve(dir, entry.name);

				if (entry.isDirectory()) {
					const newPrefix = pathPrefix ? `${pathPrefix}/${entry.name}` : entry.name;
					scanDirectory(fullPath, newPrefix);
				} else if (entry.isFile() && entry.name.endsWith(".md")) {
					const parsed = parseFrontmatter(fullPath);
					if (!parsed || !parsed.frontmatter.name) continue;

					const agentName = pathPrefix
						? `${pathPrefix}/${parsed.frontmatter.name}`
						: parsed.frontmatter.name;

					const key = agentName.toLowerCase();
					if (seen.has(key)) continue;
					seen.add(key);

					const skills = parsed.frontmatter.skills || parsed.frontmatter.skill || [];
					const hasSkills = Array.isArray(skills) ? skills.length > 0 : !!skills;

					agents.push({
						name: agentName,
						file: fullPath,
						hasSkills,
						skills: Array.isArray(skills) ? skills : (skills ? [skills] : []),
						frontmatter: parsed.frontmatter,
					});
				}
			}
		} catch (err) {
			// Silently skip unreadable directories
		}
	}

	for (const dir of agentDirs) {
		scanDirectory(dir);
	}

	return agents.sort((a, b) => a.name.localeCompare(b.name));
}

// ── Opção A: Adicionar Skills ───────────────────────────────────

function optionA_AddSkills(agents: AgentInfo[]): boolean {
	printHeader("Opção A: Adicionar Campo skills");

	const agentsWithoutSkills = agents.filter(a => !a.hasSkills);

	if (agentsWithoutSkills.length === 0) {
		printSuccess("Todos os agentes já têm o campo skills!");
		return false;
	}

	console.log(`Found ${style("yellow", agentsWithoutSkills.length.toString())} agents without skills:\n`);

	agentsWithoutSkills.forEach((agent, i) => {
		console.log(`  ${style("dim", `${(i + 1).toString().padStart(2)}.`)} ${style("bright", agent.name)}`);
		console.log(`      ${style("dim", agent.file)}`);
	});

	console.log("\n" + style("cyan", "─".repeat(60)));
	console.log(style("bright", "Default skills to add:"));
	console.log(`  ${style("green", "1")} - generic (default agent)`);
	console.log(`  ${style("green", "2")} - ${style("yellow", "[custom name]")} - specify custom skill`);
	console.log(`  ${style("red", "0")} - Cancel\n`);

	// For simplicity, we'll use "generic" as default
	const defaultSkill = "generic";

	console.log(`Will add skill: ${style("green", `"${defaultSkill}"`)} to all agents\n`);

	const backupDir = join(process.cwd(), ".pi", "backups");
	ensureDir(backupDir);

	const backups: BackupInfo[] = [];
	let modified = 0;

	for (const agent of agentsWithoutSkills) {
		try {
			// Create backup
			const backupPath = createBackup(agent.file);
			backups.push({ originalPath: agent.file, backupPath, timestamp: new Date().toISOString() });

			// Read file
			const content = readFileSync(agent.file, "utf-8");

			// Find position to insert skills (after "tools:" or before "---")
			let newContent: string;

			if (content.includes("tools:")) {
				// Insert after tools line
				newContent = content.replace(
					/^(tools:\s*[^\n]*\n)/m,
					`$1skills:\n - ${defaultSkill}\n`
				);
			} else {
				// Insert before closing "---"
				newContent = content.replace(
					/^---\r?\n/m,
					`---\nskills:\n - ${defaultSkill}\n`
				);
			}

			writeFileSync(agent.file, newContent, "utf-8");
			modified++;

			printSuccess(`Updated: ${agent.name}`);
		} catch (err) {
			printError(`Failed to update ${agent.name}: ${err}`);
		}
	}

	console.log("\n" + style("cyan", "─".repeat(60)));
	printSuccess(`Modified ${modified} agent files`);
	printInfo(`Backups saved to: ${backupDir}`);

	// Save backup manifest
	const manifestPath = join(backupDir, "backup-manifest.json");
	const manifest = {
		timestamp: new Date().toISOString(),
		action: "add-skills",
		backups,
	};
	writeFileSync(manifestPath, JSON.stringify(manifest, null, 2), "utf-8");
	printInfo(`Backup manifest: ${manifestPath}`);

	return true;
}

// ── Opção B: Modificar agent-team.ts ────────────────────────────

function optionB_ModifyAgentTeam(): boolean {
	printHeader("Opção B: Modificar agent-team.ts");

	const agentTeamPath = join(process.cwd(), "extensions", "agent-team.ts");

	if (!existsSync(agentTeamPath)) {
		printError(`File not found: ${agentTeamPath}`);
		return false;
	}

	printInfo(`Target file: ${agentTeamPath}\n`);

	// Create backup
	const backupPath = createBackup(agentTeamPath);
	printInfo(`Backup created: ${backupPath}\n`);

	let content = readFileSync(agentTeamPath, "utf-8");

	// Check if already patched
	if (content.includes("// PATCH: Skills filter removed")) {
		printWarning("File appears to already be patched!");
		console.log("Would you like to:");
		console.log(`  ${style("green", "1")} - Revert to original`);
		console.log(`  ${style("red", "0")} - Cancel\n`);
		return false;
	}

	// Apply patches
	const patches = [
		{
			search: /\/\/ Build dynamic agent catalog from active team only\s+\/\/ Include skills for agents that have them\s+const agentCatalog = Array\.from\(agentStates\.values\(\)\)\s+\.filter\(s => s\.def\.skills\.length > 0\)  \/\/ Only show agents with skills\s+\.map\(s => `### \$\{displayName\(s\.def\.name\)\}\\\\n\*\*Dispatch as:\*\* \\\`\$\{s\.def\.name\}\\\`\\\\n\$\{s\.def\.description\}\\\\n\*\*Skills:\*\* \$\{s\.def\.skills\.join\(", "\)\}`\)\s+\.join\("\\n\\n"\);/,
			replace: `// Build dynamic agent catalog from active team only
		// PATCH: Skills filter removed - show ALL agents in catalog
		// Include skills for agents that have them
		const agentCatalog = Array.from(agentStates.values())
			.map(s => {
				const skillInfo = s.def.skills.length > 0
					? \`\\\\n**Skills:** \${s.def.skills.join(", ")}\`
					: "";
				return \`### \${displayName(s.def.name)}\\\\n**Dispatch as:** \\\`\${s.def.name}\\\`\\\\n\${s.def.description}\${skillInfo}\`;
			})
			.join("\\n\\n");`,
		},
		{
			search: /const agentsWithSkills = Array\.from\(agentStates\.values\(\)\)\.filter\(s => s\.def\.skills\.length > 0\);\s+const teamMembers = agentsWithSkills\.map\(s => displayName\(s\.def\.name\)\)\.join\(", "\);/,
			replace: `// PATCH: Show all team members, not just those with skills
		const teamMembers = Array.from(agentStates.values()).map(s => displayName(s.def.name)).join(", ");
		const agentsWithSkills = Array.from(agentStates.values()).filter(s => s.def.skills.length > 0);`,
		},
		{
			search: /Members with skills: \$\{teamMembers \|\| "none"\}/,
			replace: `Members (all): $\{teamMembers}`,
		},
	];

	let applied = 0;
	for (const patch of patches) {
		const before = content;
		content = content.replace(patch.search, patch.replace);
		if (content !== before) applied++;
	}

	if (applied === 0) {
		printError("Could not apply patches - file structure may have changed");
		return false;
	}

	writeFileSync(agentTeamPath, content, "utf-8");

	printSuccess(`Applied ${applied} patches to agent-team.ts`);
	printInfo("\nChanges made:");
	printInfo("  • Removed skills filter from agent catalog");
	printInfo("  • Agent catalog now shows ALL agents");
	printInfo("  • Skills are displayed when available");
	printInfo("  • 'Members (all)' now shows all team members");

	return true;
}

// ── Opção C: Gerar Relatório ────────────────────────────────────

function optionC_GenerateReport(agents: AgentInfo[]): boolean {
	printHeader("Opção C: Relatório de Skills");

	const withSkills = agents.filter(a => a.hasSkills);
	const withoutSkills = agents.filter(a => !a.hasSkills);

	console.log(`Total agents found: ${style("bright", agents.length.toString())}\n`);

	// Agents WITH skills
	console.log(style("green", `✓ Agents WITH skills (${withSkills.length}):`));
	if (withSkills.length === 0) {
		console.log(style("dim", "  (none)"));
	} else {
		withSkills.forEach(agent => {
			const skillsList = agent.skills.map(s => style("cyan", `"${s}"`)).join(", ");
			console.log(`\n  ${style("bright", agent.name)}`);
			console.log(`    ${style("dim", "├─ File:")} ${agent.file}`);
			console.log(`    ${style("dim", "└─ Skills:")} ${skillsList}`);
		});
	}

	console.log("\n" + style("cyan", "─".repeat(60)) + "\n");

	// Agents WITHOUT skills
	console.log(style("yellow", `✗ Agents WITHOUT skills (${withoutSkills.length}):`));
	if (withoutSkills.length === 0) {
		console.log(style("dim", "  (none)"));
	} else {
		withoutSkills.forEach(agent => {
			console.log(`\n  ${style("bright", agent.name)}`);
			console.log(`    ${style("dim", "└─ File:")} ${agent.file}`);
		});
	}

	// Save report to file
	const reportDir = join(process.cwd(), ".pi", "reports");
	ensureDir(reportDir);

	const timestamp = new Date().toISOString().replace(/[:.]/g, "-").slice(0, -5);
	const reportPath = join(reportDir, `agent-skills-report_${timestamp}.txt`);

	const reportLines = [
		`Agent Skills Report`,
		`Generated: ${new Date().toISOString()}`,
		``,
		`SUMMARY`,
		`-------`,
		`Total agents: ${agents.length}`,
		`With skills: ${withSkills.length}`,
		`Without skills: ${withoutSkills.length}`,
		``,
		``,
		`AGENTS WITH SKILLS`,
		`-------------------`,
		...withSkills.map(a => `${a.name}\n  File: ${a.file}\n  Skills: ${a.skills.join(", ")}\n`),
		``,
		``,
		`AGENTS WITHOUT SKILLS`,
		`----------------------`,
		...withoutSkills.map(a => `${a.name}\n  File: ${a.file}\n`),
	];

	writeFileSync(reportPath, reportLines.join("\n"), "utf-8");

	console.log("\n" + style("cyan", "─".repeat(60)));
	printSuccess(`Report saved to: ${reportPath}`);

	return true;
}

// ── Função Rollback ─────────────────────────────────────────────

function rollbackBackup(): boolean {
	printHeader("Rollback from Backup");

	const backupDir = join(process.cwd(), ".pi", "backups");
	const manifestPath = join(backupDir, "backup-manifest.json");

	if (!existsSync(manifestPath)) {
		printError("No backup manifest found");
		return false;
	}

	try {
		const manifest = JSON.parse(readFileSync(manifestPath, "utf-8"));
		const backups = manifest.backups as BackupInfo[];

		console.log(`Found backup from: ${style("dim", manifest.timestamp)}`);
		console.log(`Action: ${style("cyan", manifest.action)}`);
		console.log(`Files: ${backups.length}\n`);

		let restored = 0;
		for (const backup of backups) {
			if (!existsSync(backup.backupPath)) {
				printWarning(`Backup file missing: ${backup.backupPath}`);
				continue;
			}

			try {
				const content = readFileSync(backup.backupPath, "utf-8");
				writeFileSync(backup.originalPath, content, "utf-8");
				restored++;
				printSuccess(`Restored: ${backup.originalPath}`);
			} catch (err) {
				printError(`Failed to restore ${backup.originalPath}: ${err}`);
			}
		}

		console.log("\n" + style("cyan", "─".repeat(60)));
		printSuccess(`Restored ${restored} file(s)`);

		// Archive manifest
		const archivePath = join(backupDir, `backup-manifest-restored-${Date.now()}.json`);
		writeFileSync(archivePath, readFileSync(manifestPath), "utf-8");
		return true;

	} catch (err) {
		printError(`Failed to read backup manifest: ${err}`);
		return false;
	}
}

// ── Menu Principal ──────────────────────────────────────────────

function showMenu(): never {
	printHeader("Agent Teams List - Fix Script");

	console.log(style("bright", "This script fixes the issue where agents don't appear in"));
	console.log(style("bright", "the 'Members with skills' list.\n"));

	console.log(style("cyan", "Choose an option:"));
	console.log(`  ${style("green", "A")} - Add default 'skills' field to agents without it`);
	console.log(`  ${style("green", "B")} - Modify agent-team.ts to show ALL agents (remove filter)`);
	console.log(`  ${style("green", "C")} - Generate report of agents with/without skills`);
	console.log(`  ${style("yellow", "R")} - Rollback from backup`);
	console.log(`  ${style("red", "Q")} - Quit\n`);

	process.exit(0);
}

function main() {
	const args = process.argv.slice(2);
	const option = args[0]?.toUpperCase();

	// Scan agents first
	const cwd = process.cwd();
	const agents = scanAgentFiles(cwd);

	if (agents.length === 0) {
		printError("No agent files found!");
		printInfo("Looked in: agents/, .claude/agents/, .pi/agents/");
		process.exit(1);
	}

	printInfo(`Found ${agents.length} agent(s)\n`);

	switch (option) {
		case "A":
			optionA_AddSkills(agents);
			break;

		case "B":
			optionB_ModifyAgentTeam();
			break;

		case "C":
			optionC_GenerateReport(agents);
			break;

		case "R":
			rollbackBackup();
			break;

		case "Q":
			console.log("Bye!");
			break;

		default:
			showMenu();
			break;
	}

	console.log("\n" + style("cyan", "─".repeat(60)) + "\n");
}

main();
