// Test script to validate shortcuts.yaml structure
const fs = require('fs');
const path = require('path');

const shortcutsPath = path.join('.pi', 'agents', 'shortcuts.yaml');
const content = fs.readFileSync(shortcutsPath, 'utf-8');

console.log('🔍 Validating shortcuts.yaml...\n');

// Check for alt+shift+i
if (content.includes('alt+shift+i')) {
  console.log('✓ alt+shift+i is defined');
  // Find the line
  const lines = content.split('\n');
  const line = lines.find(l => l.includes('alt+shift+i'));
  console.log('  Line:', line.trim());
} else {
  console.log('✗ alt+shift+i is NOT defined');
}

// Check for prev-team action
if (content.includes('prev-team')) {
  console.log('✓ prev-team action is referenced');
} else {
  console.log('✗ prev-team action is NOT referenced');
}

// Check for F6
if (content.includes('f6')) {
  console.log('✓ f6 is defined');
} else {
  console.log('✗ f6 is NOT defined');
}

// Check for next-team action
if (content.includes('next-team')) {
  console.log('✓ next-team action is referenced');
} else {
  console.log('✗ next-team action is NOT referenced');
}

// Check for misleading F7 comment
if (content.includes('F7') || content.includes('f7')) {
  console.log('✗ WARNING: F7 is still referenced (should be removed)');
} else {
  console.log('✓ No F7 references found');
}

// Check for agent-team section
if (content.includes('agent-team:')) {
  console.log('✓ agent-team section exists');
} else {
  console.log('✗ agent-team section is missing');
}

console.log('\n✅ Validation complete!\n');
