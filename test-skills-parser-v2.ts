/**
 * Teste do parser v2 de skills com suporte a arrays YAML
 */

interface ParsedFrontmatter {
	[key: string]: string | string[];
}

function parseAgentFileFrontmatter(frontmatterText: string): ParsedFrontmatter {
	const lines = frontmatterText.split(/\r?\n/);
	const frontmatter: ParsedFrontmatter = {};
	let currentArray: string[] | null = null;
	let currentKey: string | null = null;

	for (const line of lines) {
		const idx = line.indexOf(":");
		if (idx > 0) {
			// New key-value pair
			const key = line.slice(0, idx).trim();
			const value = line.slice(idx + 1).trim();
			currentKey = key;
			currentArray = null;

			// Check if this might be the start of an array (next line starts with "-")
			if (value === "") {
				currentArray = [];
				frontmatter[key] = currentArray;
			} else {
				frontmatter[key] = value;
			}
		} else if (currentArray && currentKey) {
			// Array item (starts with "-")
			const itemMatch = line.match(/^\s+-\s+(.+)$/);
			if (itemMatch) {
				currentArray.push(itemMatch[1].trim());
			}
		}
	}

	return frontmatter;
}

function parseSkillsFromFrontmatter(frontmatter: ParsedFrontmatter): string[] {
	const skillsField = frontmatter.skills || frontmatter.skill;
	if (!skillsField) return [];

	if (Array.isArray(skillsField)) {
		// YAML array format
		return skillsField.filter(s => s.length > 0);
	} else if (typeof skillsField === "string") {
		// Handle comma-separated values
		if (skillsField.includes(",")) {
			return skillsField.split(",").map(s => s.trim()).filter(s => s.length > 0);
		} else {
			// Single skill (trim and filter empty)
			return [skillsField.trim()].filter(s => s.length > 0);
		}
	}

	return [];
}

// Test cases
const tests = [
	{
		name: "YAML array format (single item)",
		frontmatter: parseAgentFileFrontmatter("name: test\nskills:\n - 5-min-scripts"),
		expected: ["5-min-scripts"]
	},
	{
		name: "YAML array format (multiple items)",
		frontmatter: parseAgentFileFrontmatter("name: test\nskills:\n - 5-min-scripts\n - bowser\n - playwright-bowser"),
		expected: ["5-min-scripts", "bowser", "playwright-bowser"]
	},
	{
		name: "Comma-separated",
		frontmatter: parseAgentFileFrontmatter("name: test\nskills: 5-min-scripts, bowser, another-skill"),
		expected: ["5-min-scripts", "bowser", "another-skill"]
	},
	{
		name: "Single skill",
		frontmatter: parseAgentFileFrontmatter("name: test\nskills: 5-min-scripts"),
		expected: ["5-min-scripts"]
	},
	{
		name: "Singular 'skill'",
		frontmatter: parseAgentFileFrontmatter("name: test\nskill: 5-min-scripts"),
		expected: ["5-min-scripts"]
	},
	{
		name: "No skills field",
		frontmatter: parseAgentFileFrontmatter("name: test\ntools: read"),
		expected: []
	},
	{
		name: "Empty skills array",
		frontmatter: parseAgentFileFrontmatter("name: test\nskills:\n"),
		expected: [] // Note: empty array would need special handling
	},
	{
		name: "Whitespace handling in arrays",
		frontmatter: parseAgentFileFrontmatter("name: test\nskills:\n -   skill-one  \n - skill-two"),
		expected: ["skill-one", "skill-two"]
	}
];

console.log("=== Testes do Parser v2 de Skills ===\n");

let passed = 0;
let failed = 0;

for (const test of tests) {
	const result = parseSkillsFromFrontmatter(test.frontmatter);
	const success = JSON.stringify(result) === JSON.stringify(test.expected);

	if (success) {
		passed++;
		console.log(`✅ ${test.name}`);
		console.log(`   Resultado: [${result.map(s => `"${s}"`).join(", ")}]`);
	} else {
		failed++;
		console.log(`❌ ${test.name}`);
		console.log(`   Esperado: [${test.expected.map(s => `"${s}"`).join(", ")}]`);
		console.log(`   Obtido:   [${result.map(s => `"${s}"`).join(", ")}]`);
	}
	console.log();
}

console.log(`\n=== Resumo ===`);
console.log(`Total: ${tests.length} testes`);
console.log(`Passou: ${passed}`);
console.log(`Falhou: ${failed}`);
console.log(`Taxa de sucesso: ${((passed / tests.length) * 100).toFixed(1)}%`);

if (failed === 0) {
	console.log("\n✨ Todos os testes passaram!");
	process.exit(0);
} else {
	console.log("\n⚠️ Alguns testes falharam!");
	process.exit(1);
}
