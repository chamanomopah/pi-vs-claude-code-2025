/**
 * Teste com agentes reais do projeto
 */
import { readFileSync } from "fs";

interface ParsedFrontmatter {
	[key: string]: string | string[];
}

function parseAgentFileFrontmatter(filePath: string): ParsedFrontmatter | null {
	try {
		const raw = readFileSync(filePath, "utf-8");
		const match = raw.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n([\s\S]*)$/);
		if (!match) return null;

		const lines = match[1].split(/\r?\n/);
		const frontmatter: ParsedFrontmatter = {};
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

		return frontmatter;
	} catch {
		return null;
	}
}

function parseSkillsFromFrontmatter(frontmatter: ParsedFrontmatter | null): string[] {
	if (!frontmatter) return [];

	const skillsField = frontmatter.skills || frontmatter.skill;
	if (!skillsField) return [];

	if (Array.isArray(skillsField)) {
		return skillsField.filter(s => s.length > 0);
	} else if (typeof skillsField === "string") {
		if (skillsField.includes(",")) {
			return skillsField.split(",").map(s => s.trim()).filter(s => s.length > 0);
		} else {
			return [skillsField.trim()].filter(s => s.length > 0);
		}
	}

	return [];
}

// Testar agentes reais
const agents = [
	".pi/agents/builder.md",
	".pi/agents/bowser.md",
	".pi/agents/documenter.md",
	".pi/agents/scout.md",
	".pi/agents/flowchart.md",
];

console.log("=== Teste com Arquivos de Agentes Reais ===\n");

for (const agentPath of agents) {
	const frontmatter = parseAgentFileFrontmatter(agentPath);
	const skills = parseSkillsFromFrontmatter(frontmatter);

	console.log(`📄 ${agentPath}`);
	if (frontmatter) {
		console.log(`   Name: ${frontmatter.name}`);
		console.log(`   Skills: [${skills.length > 0 ? skills.map(s => `"${s}"`).join(", ") : "sem skills"}]`);
	} else {
		console.log(`   ❌ Falha ao parsear`);
	}
	console.log();
}
