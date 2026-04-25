# SSH Node n8n - Quick Reference

> Consulta rápida para o SSH node do n8n com foco em Windows

## 🔧 Configuração Windows - Checklist

```powershell
# 1. Instalar OpenSSH
Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0

# 2. Iniciar serviço
Start-Service sshd
Set-Service -Name sshd -StartupType 'Automatic'

# 3. PowerShell como shell padrão (CRUCIAL!)
Set-ItemProperty -Path "HKLM:\SOFTWARE\OpenSSH" `
  -Name DefaultShell `
  -Value "C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe"
Restart-Service sshd

# 4. Firewall
New-NetFirewallRule -Name sshd -DisplayName 'OpenSSH Server' `
  -Enabled True -Direction Inbound -Protocol TCP -LocalPort 22
```

## 🔐 Chave de Criptografia n8n

```bash
# Gerar chave
openssl rand -hex 32

# Adicionar ao .env
N8N_ENCRYPTION_KEY=sua_chave_hex_64_caracteres
```

⚠️ **Backup desta chave - perdê-la = perder todas credenciais!**

## 🎯 Configuração Node

| Campo | Windows | Linux |
|-------|---------|-------|
| Working Directory | `{{null}}` | `/home/user` |
| Command | `powershell.exe -Command "comando"` | `comando` |
| Credential | SSH Key + Passphrase | SSH Key |

## 🩺 Troubleshooting Rápido

| Erro | Solução |
|------|---------|
| Cannot parse privateKey | Inclua linhas BEGIN/END da chave |
| The filename... syntax | Use `{{null}}` em Working Directory |
| All auth methods failed | Teste `ssh usuario@host` manualmente |
| ECONNREFUSED | Verifique `Get-Service sshd` e firewall |
| Permission denied | Verifique permissões com `icacls` |

## 💻 Comandos Mais Usados

### Windows (PowerShell)

```powershell
# Sistema
hostname
systeminfo | Select-String "OS Name","OS Version"

# Disco
Get-PSDrive C | Select-Object Used,Free

# Serviços
Get-Service | Where-Object {$_.Status -eq 'Running'}
Restart-Service -Name "nginx" -Force

# Processos
Get-Process
Stop-Process -Name "notepad" -Force

# Arquivos
Get-ChildItem "C:\Logs" -File | 
  Where-Object {$_.LastWriteTime -lt (Get-Date).AddDays(-30)} | 
  Remove-Item -Force

# Rede
Test-NetConnection -ComputerName "google.com" -Port 443
```

### Linux

```bash
# Sistema
uptime
df -h
free -h

# Serviços
systemctl status nginx
systemctl restart nginx

# Docker
docker ps
docker restart container-name
```

## 📋 Workflows Template

### 1. Monitoramento Simples

```
Schedule (15 min) → SSH (df -h) → Code (parse) → 
IF (>80%) → Slack Alert
```

### 2. Limpeza de Logs

```
Schedule (diário) → SSH (deletar antigos) → 
Code (contar) → IF (>0) → Email Report
```

### 3. Deploy Docker

```
Webhook → SSH (pull) → SSH (stop) → SSH (rm) → 
SSH (run) → SSH (health) → Slack
```

## 🔒 Segurança - Essentials

- ✅ Usar autenticação por chave em produção
- ✅ Criar usuário dedicado para automação
- ✅ Configurar N8N_ENCRYPTION_KEY
- ✅ Aplicar princípio do menor privilégio
- ✅ Rotacionar chaves periodicamente
- ✅ Monitorar logs de autenticação

## 📚 Referências

- **Docs:** https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.ssh/
- **Comunidade:** https://community.n8n.io/
- **Guia Completo:** `ssh-node-research.md`
- **Resumo:** `ssh-node-resumo.md`

---

**Data:** 25/04/2026  
**Versão n8n:** 1.x+
