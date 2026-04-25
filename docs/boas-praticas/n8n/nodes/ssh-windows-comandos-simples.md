# SSH Node no Windows - SOLUÇÃO RÁPIDA

**Problema:** "O sistema não pode encontrar o caminho especificado"  
**Causa:** Campo `cwd` com caminho Linux (`/.local/`) em servidor Windows

---

## 1. SOLUÇÃO IMEDIATA ✅

### O Que Mudar no Nó SSH

**Campo `cwd` (Current Working Directory):**

```
❌ ERRADO: "/.local/"
✅ CORRETO: "" (vazio)
✅ CORRETO: null
✅ CORRETO: "C:\Users\SeuUsuario"
✅ CORRETO: "C:/n8n-scripts"
```

### Localização no Nó SSH

```
Nó SSH → Aba "Additional Fields" → Campo "Working Directory" (cwd)

┌─────────────────────────────────────────┐
│ Additional Fields                       │
├─────────────────────────────────────────┤
│ ☑ Working Directory (cwd)              │
│                                          │
│ [ C:\n8n-scripts                    ]   │
│                                          │
│ Ou deixe vazio para usar o default      │
└─────────────────────────────────────────┘
```

---

## 2. 10 COMANDOS SIMPLES PARA TESTAR 🧪

**Use estes comandos para testar se o SSH está funcionando:**

| Comando | O Que Faz | Windows |
|---------|-----------|---------|
| `hostname` | Nome do servidor | ✅ |
| `whoami` | Usuário atual | ✅ |
| `date` | Data atual | ✅ |
| `time` | Hora atual | ✅ |
| `ver` | Versão do Windows | ✅ |
| `dir` | Listar arquivos | ✅ |
| `cd` | Diretório atual | ✅ |
| `echo test` | Teste de saída | ✅ |
| `set` | Variáveis de ambiente | ✅ |
| `ipconfig` | Configuração de IP | ✅ |

**Teste rápido no nó SSH:**
```
whoami
```

---

## 3. EXEMPLO DE CONFIGURAÇÃO CORRETA 📋

### JSON do Nó SSH para Windows

```json
{
  "parameters": {
    "host": "192.168.1.100",
    "port": 22,
    "username": "admin",
    "password": "senha_ssh",
    "command": "dir C:\\",
    "cwd": "C:\n8n-scripts",
    "additionalFields": {}
  },
  "name": "SSH - Windows",
  "type": "n8n-nodes-base.ssh",
  "typeVersion": 1,
  "position": [500, 300]
}
```

### Exemplo com `cwd` VAZIO (recomendado)

```json
{
  "parameters": {
    "host": "192.168.1.100",
    "port": 22,
    "username": "admin",
    "command": "whoami",
    "cwd": ""
  },
  "name": "SSH - Windows Test",
  "type": "n8n-nodes-base.ssh"
}
```

---

## 4. COMANDOS PRÁTICOS DO WINDOWS 💡

### Gerenciamento de Arquivos

| Ação | Comando CMD | Comando PowerShell |
|------|-------------|-------------------|
| **Listar arquivos** | `dir` | `ls` ou `Get-ChildItem` |
| **Mudar diretório** | `cd pasta` | `cd pasta` |
| **Criar pasta** | `mkdir pasta` | `New-Item -ItemType Directory pasta` |
| **Deletar arquivo** | `del arquivo.txt` | `Remove-Item arquivo.txt` |
| **Copiar arquivo** | `copy orig.txt dest.txt` | `Copy-Item orig.txt dest.txt` |
| **Mover arquivo** | `move orig.txt dest.txt` | `Move-Item orig.txt dest.txt` |
| **Ver conteúdo** | `type arquivo.txt` | `Get-Content arquivo.txt` |

### Informações do Sistema

| Ação | Comando |
|------|---------|
| **Versão Windows** | `ver` |
| **Variáveis de ambiente** | `set` |
| **Configuração IP** | `ipconfig` |
| **Processos rodando** | `tasklist` |
| **Uso de disco** | `fsutil volume diskfree C:` |
| **Data e hora** | `date /t & time /t` |

### Scripts e Arquivos Batch

**Executar script batch:**
```
cmd.exe /c C:\scripts\meu-script.bat
```

**Executar comando PowerShell:**
```
powershell.exe -Command "Get-Process"
```

**Executar arquivo Python:**
```
python C:\scripts\script.py
```

**Executar arquivo Node.js:**
```
node C:\scripts\app.js
```

---

## 5. DICAS IMPORTANTES ⚠️

### CMD vs PowerShell no SSH Node

**Como saber qual shell está sendo usado:**

```bash
# Teste este comando:
echo %0

# Se retornar: cmd.exe  → Você está no CMD
# Se retornar: powershell → Você está no PowerShell
```

**Forçar uso do CMD:**
```
cmd.exe /c seu-comando
```

**Forçar uso do PowerShell:**
```
powershell.exe -Command "seu-comando"
```

### Comandos que Funcionam em AMBOS

| Comando | Funciona em CMD | Funciona em PowerShell |
|---------|-----------------|------------------------|
| `dir` | ✅ | ✅ |
| `cd` | ✅ | ✅ |
| `mkdir` | ✅ | ✅ |
| `hostname` | ✅ | ✅ |
| `whoami` | ✅ | ✅ |
| `date` | ✅ | ✅ |
| `time` | ✅ | ✅ |
| `echo` | ✅ | ✅ |
| `ipconfig` | ✅ | ✅ |
| `ping` | ✅ | ✅ |
| `exit` | ✅ | ✅ |

### Caminhos no Windows

**Use sempre barras invertidas ou barra normal:**

```
✅ C:\Users\Nome\pasta
✅ C:/Users/Nome/pasta
✅ \servidor\compartilhamento

❌ /c/users/nome/pasta (formato Linux)
```

### Caracteres Especiais

**Escape de aspas e caracteres especiais:**

```
# Com variáveis:
echo "Valor: %VARIAVEL%"          # CMD
echo "Valor: $env:VARIAVEL"       # PowerShell

# Com aspas:
powershell.exe -Command "Write-Host 'Texto com aspas'"
```

---

## 6. SOLUÇÃO DE PROBLEMAS 🔧

### Erro: "O sistema não pode encontrar o caminho especificado"

**Causa 1: `cwd` com formato Linux**
```json
// ❌ ERRADO
"cwd": "/.local/"

// ✅ CORRETO
"cwd": "C:\n8n-scripts"
// ou
"cwd": ""
```

**Causa 2: Caminho com barras erradas**
```
❌ C:/Users/Nome/arquivo.txt
✅ C:\Users\Nome\arquivo.txt
```

**Causa 3: Comando que não existe no Windows**
```
❌ ls -la         (comando Linux)
✅ dir            (equivalente Windows)

❌ pwd            (comando Linux)
✅ cd             (equivalente Windows)
```

### Teste Passo a Passo

**1. Teste se o SSH conecta:**
```
whoami
```

**2. Teste se pode executar comandos:**
```
hostname
```

**3. Teste se pode navegar diretórios:**
```
dir C:\
```

**4. Teste se pode executar scripts:**
```
cmd.exe /c echo "Teste"
```

---

## 7. CHECKLIST RÁPIDO ✅

- [ ] Campo `cwd` está vazio ou em formato Windows (`C:\pasta`)
- [ ] Comando existe no Windows (não use comandos Linux)
- [ ] Caminhos usam `\` ou `/` (mas não formato `/c/`)
- [ ] Se usar barras invertidas, escape-as: `C:\n8n\scripts`
- [ ] Testou primeiro com comandos simples (`whoami`, `hostname`)
- [ ] Verificou se o usuário SSH tem permissão no diretório

---

## 8. CÓPIA E COLAGEM 📋

### Configuração Teste Simples

```
Comando: whoami
cwd: (vazio)
```

### Configuração Script Batch

```
Comando: cmd.exe /c C:\scripts\script.bat
cwd: C:\scripts
```

### Configuração PowerShell

```
Comando: powershell.exe -Command "Get-Process | Select-Object -First 5"
cwd: (vazio)
```

### Configuração Listar Arquivos

```
Comando: dir C:\n8n-scripts
cwd: C:\
```

---

## RESUMO EM 1 LINHA

> **Campo `cwd` VAZIO ou `C:\caminho\windows` (NUNCA `/.local/`) + comandos Windows (`dir`, `whoami`, `hostname`)**
