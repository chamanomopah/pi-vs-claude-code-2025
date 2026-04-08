import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

console.log('🧪 Validando setup LiveKit + Pi...\n');

const checks = [
  {
    name: 'Extensão TypeScript',
    path: 'extensions/livekit.ts',
    validate: (content) => {
      if (content.includes('livekit_basic_agent.py')) {
        return { pass: false, msg: '❌ BUG: Ainda referencia livekit_basic_agent.py' };
      }
      if (content.includes('pi_agent.py')) {
        return { pass: true, msg: '✓ Referencia pi_agent.py corretamente' };
      }
      return { pass: false, msg: '⚠ Não encontra referencia a pi_agent.py' };
    }
  },
  {
    name: 'Agente Python',
    path: 'scripts/livekit-pi-extension/pi_agent.py',
    validate: (content) => {
      if (content.includes('deepgram') && content.includes('cartesia')) {
        return { pass: true, msg: '✓ Plugins configurados' };
      }
      return { pass: false, msg: '⚠ Plugins podem estar faltando' };
    }
  },
  {
    name: 'Arquivo .env',
    path: 'scripts/livekit-pi-extension/.env',
    validate: (content) => {
      const required = ['LIVEKIT_URL', 'LIVEKIT_API_KEY', 'LIVEKIT_API_SECRET', 'DEEPGRAM_API_KEY', 'CARTESIA_API_KEY'];
      const missing = required.filter(key => !content.includes(key));
      if (missing.length === 0) {
        return { pass: true, msg: `✓ Todas as ${required.length} variáveis presentes` };
      }
      return { pass: false, msg: `❌ Faltando: ${missing.join(', ')}` };
    }
  },
  {
    name: 'requirements.txt',
    path: 'scripts/livekit-pi-extension/requirements.txt',
    validate: (content) => {
      const required = ['livekit-agents', 'livekit-plugins-deepgram', 'livekit-plugins-cartesia', 'livekit-plugins-google'];
      const missing = required.filter(pkg => !content.includes(pkg));
      if (missing.length === 0) {
        return { pass: true, msg: '✓ Todas dependências presentes' };
      }
      return { pass: false, msg: `❌ Faltando: ${missing.join(', ')}` };
    }
  }
];

let passCount = 0;
let failCount = 0;

checks.forEach(check => {
  const fullPath = path.resolve(__dirname, '..', '..', check.path);
  console.log(`\n📁 ${check.name}`);
  console.log(`   Caminho: ${check.path}`);

  if (!fs.existsSync(fullPath)) {
    console.log(`   ❌ ARQUIVO NÃO ENCONTRADO`);
    failCount++;
    return;
  }

  const content = fs.readFileSync(fullPath, 'utf-8');
  const result = check.validate(content);
  console.log(`   ${result.msg}`);

  if (result.pass) {
    passCount++;
  } else {
    failCount++;
  }
});

console.log(`\n${'='.repeat(50)}`);
console.log(`✓ Passou: ${passCount}/${checks.length}`);
console.log(`❌ Falhou: ${failCount}/${checks.length}`);
console.log(`${'='.repeat(50)}`);

process.exit(failCount > 0 ? 1 : 0);
