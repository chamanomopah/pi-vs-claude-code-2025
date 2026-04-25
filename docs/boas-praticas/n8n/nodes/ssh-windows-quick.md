# SSH Node n8n no Windows - Guia Rápido

> **Resumo Executivo** - Soluções imediatas para começar a usar SSH no Windows
> 
> **Última atualização**: Abril 2026

---

## ⚡ SOLUÇÕES IMEDIATAS (Copy & Paste)

### Solução 1: Configurar PowerShell como Shell Padrão (RECOMENDADO)

Execute no servidor Windows como Administrador:

```powershell
Set-ItemProperty -Path "HKLM:\SOFTWARE\OpenSSH" -Name DefaultShell -Value "C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe"
Restart-Service sshd
```

### Solução 2: Working Directory como Expressão Vazia

1. Clique no ícone `fx` ao lado do campo "Working Directory"
2. Deixe o campo **VAZIO**

### Solução 3: Usar `.` como Working Directory

```json
{
  "workingDirectory": ".",
  "command": "hostname"
}
```

---

## 🎯 CONFIGURAÇÃO MÍNIMA FUNCIONAL

### Nó SSH - Teste Básico

```json
{
  "operation": "executeCommand",
  "credential": {
    "host": "IP_DO_SERVIDOR",
    "port": 22,
    "username": "administrator",
    "password": "SUA_SENHA"
  },
  "workingDirectory": ".",
  "command": "hostname"
}
```

---

## 📋 VALORES DE WORKING DIRECTORY

| Valor | Funciona? | Quando Usar |
|-------|-----------|-------------|
| `.` | ✅ | **Padrão - Use sempre** |
| `%USERPROFILE%` | ✅ | Home do usuário |
| `%TEMP%` | ✅ | Arquivos temporários |
| `C:\Users\Public` | ✅ | Arquivos públicos |
| `C:\` | ⚠️ | Requer permissão |
| `/` | ❌ | **NUNCA use** |
| `null` | ❌ | **NUNCA use** |

---

## 🧪 COMANDOS DE TESTE (EM ORDEM)

### Teste 1: Conexão
```
hostname
```

### Teste 2: Usuário
```
whoami
```

### Teste 3: Lista
```
dir
```

### Teste 4: Info
```
ver
```

---

## 🔥 EXEMPLOS PRONTOS (Copy & Paste)

### Listar Arquivos
```json
{
  "workingDirectory": "C:\Users\Public",
  "command": "dir"
}
```

### Executar Script PowerShell
```json
{
  "workingDirectory": "C:\Scripts",
  "command": "powershell.exe -ExecutionPolicy Bypass -File \"script.ps1\""
}
```

### Executar Script Batch
```json
{
  "workingDirectory": "C:\Scripts",
  "command": "cmd.exe /c \"script.bat\""
}
```

### Informações do Sistema
```json
{
  "workingDirectory": ".",
  "command": "systeminfo"
}
```

---

## ❌ ERROS COMUNS - SOLUÇÕES RÁPIDAS

### "The system cannot find the path specified"
**Solução:** Use `.` como Working Directory

### "Working Directory is required"
**Solução:** Use expressão vazia (clique em fx e deixe vazio)

### "Command not found"
**Solução:** Use comando Windows (`dir` em vez de `ls`)

### "The filename... syntax is incorrect"
**Solução:** Use aspas para caminhos com espaços: `"C:\Program Files"`

---

## 💡 DICAS ESSENCIAIS

1. **SEMPRE** teste com `hostname` primeiro
2. **NUNCA** use `/` como Working Directory no Windows
3. **SEMPRE** use `\` no JSON para caminhos (`C:\Windows`)
4. **USE** aspas para caminhos com espaços
5. **CONFIGURE** PowerShell como shell padrão para melhor compatibilidade

---

## 🚀 WORKFLOW RÁPIDO DE MONITORAMENTO

```json
{
  "nodes": [
    {
      "name": "SSH - CPU",
      "type": "n8n-nodes-base.ssh",
      "parameters": {
        "operation": "executeCommand",
        "workingDirectory": ".",
        "command": "wmic cpu get loadpercentage /value"
      }
    },
    {
      "name": "SSH - Memory",
      "type": "n8n-nodes-base.ssh",
      "parameters": {
        "operation": "executeCommand",
        "workingDirectory": ".",
        "command": "wmic OS get FreePhysicalMemory /value"
      }
    },
    {
      "name": "SSH - Disk",
      "type": "n8n-nodes-base.ssh",
      "parameters": {
        "operation": "executeCommand",
        "workingDirectory": ".",
        "command": "wmic logicaldisk get freespace,size"
      }
    }
  ]
}
```

---

## 📚 DOCUMENTOS RELACIONADOS

- `ssh-windows-completo.md` - Guia completo
- `ssh-windows-exemplos.md` - Mais exemplos
- `ssh-windows-erros.md` - Troubleshooting detalhado
- `ssh-windows-comandos.md` - Lista completa de comandos

---

**Lembrete:** Para suporte detalhado, consulte o documento principal `ssh-windows-completo.md`
