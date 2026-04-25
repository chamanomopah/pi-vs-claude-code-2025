# SSH Node do n8n - Resumo Executivo

## 📋 Visão Geral

O **SSH node** do n8n é um componente essencial para automação de servidores, permitindo executar comandos remotos, transferir arquivos e gerenciar sistemas de forma segura via protocolo SSH.

## 🎯 Principais Capacidades

| Operação | Descrição | Caso de Uso |
|----------|-----------|-------------|
| **Execute Command** | Roda comandos em servidores remotos | Manutenção, monitoramento, deploy |
| **Download File** | Baixa arquivos do servidor remoto | Backup de logs, configs |
| **Upload File** | Envia arquivos para servidor remoto | Deploy de código, configs |

## 🔧 Configuração Windows - Checklist Rápido

### ✅ Pré-requisitos Servidor Windows

```powershell
# 1. Instalar OpenSSH Server
Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0

# 2. Iniciar serviço
Start-Service sshd
Set-Service -Name sshd -StartupType 'Automatic'

# 3. Configurar PowerShell como shell padrão (CRUCIAL!)
Set-ItemProperty -Path "HKLM:\SOFTWARE\OpenSSH" `
  -Name DefaultShell `
  -Value "C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe"
Restart-Service sshd

# 4. Firewall
New-NetFirewallRule -Name sshd -DisplayName 'OpenSSH Server' `
  -Enabled True -Direction Inbound -Protocol TCP -LocalPort 22
```

### ✅ Configurar Credencial n8n

**Autenticação Recomendada:** Chave Privata (Private Key)

1. Cole a chave privada **COMPLETA** no campo:
   ```
   -----BEGIN OPENSSH PRIVATE KEY-----
   ... conteúdo da chave ...
   -----END OPENSSH PRIVATE KEY-----
   ```

2. Adicione passphrase se a chave tiver

### ✅ Configurar Node

- **Working Directory** (Windows): Use `{{null}}` ou deixe vazio
- **Command**: Use comandos PowerShell completos com caminhos

## 🚨 Erros Comuns e Soluções Rápidas

| Erro | Solução |
|------|---------|
| "Cannot parse privateKey" | Inclua linhas BEGIN/END da chave |
| "The filename... syntax is incorrect" | Use `{{null}}` em Working Directory ou configure PowerShell como shell padrão |
| "All configured authentication methods failed" | Teste conexão manual com `ssh usuario@host` |
| "ECONNREFUSED" | Verifique se `sshd` está rodando e firewall liberado |
| "Permission denied" | Verifique permissões do diretório/arquivo |

## 🔐 Boas Práticas de Segurança

### Chave de Criptografia n8n (CRUCIAL!)

```bash
# Gerar chave
openssl rand -hex 32

# Adicionar ao .env
N8N_ENCRYPTION_KEY=sua_chave_hex_64_caracteres
```

⚠️ **Sempre backup desta chave - perdê-la = perder todas credenciais!**

### Princípios de Segurança

- ✅ Usar autenticação por chave em produção
- ✅ Criar usuário dedicado para automação (evite Administrador)
- ✅ Aplicar princípio do menor privilégio
- ✅ Rotacionar chaves periodicamente
- ✅ Monitorar logs de autenticação

## 💻 Comandos Úteis

### Windows (PowerShell)

```powershell
# Informações do sistema
hostname
systeminfo | Select-String "OS Name","OS Version"

# Espaço em disco
Get-PSDrive C | Select-Object Used,Free

# Serviços
Get-Service -Name "nginx" | Select-Object Name,Status
Restart-Service -Name "nginx" -Force

# Processos
Get-Process
Stop-Process -Name "notepad" -Force

# Limpeza de logs
Get-ChildItem "C:\Logs" -File | 
  Where-Object {$_.LastWriteTime -lt (Get-Date).AddDays(-30)} | 
  Remove-Item -Force
```

### Linux

```bash
# Informações do sistema
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

## 📊 Exemplos de Workflows Práticos

### 1. Monitoramento de VPS
```
Schedule (15 min) → SSH (df -h) → Code (parse) → IF (>80%) → Slack Alert
```

### 2. Auto-Update Windows
```
Schedule (semanal) → SSH (Windows Update) → Wait (30 min) → SSH (check) → Email Report
```

### 3. Limpeza de Logs
```
Schedule (diário) → SSH (deletar antigos) → Code (contar) → IF (>0) → Email Report
```

### 4. Deploy Docker
```
Webhook → SSH (docker pull) → SSH (stop) → SSH (rm) → SSH (run) → SSH (health) → Slack
```

### 5. Health Check
```
Schedule (hora) → SSH (CPU) → SSH (RAM) → SSH (Disk) → Merge → Code → IF (fail) → Slack
```

## 📚 Referências Principais

- **Docs Oficiais**: https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.ssh/
- **Comunidade**: https://community.n8n.io/
- **Security Guide**: https://vps.us/blog/secure-n8n/
- **Workflows**: https://n8n.io/workflows/

## ⚡ Dicas de Performance

- Use comandos específicos em vez de genéricos
- Evite comandos que retornam muito output
- Implemente timeouts em workflows
- Considere execução paralela para múltiplos servidores

## 🎓 Aprendizado Recomendado

1. Comece com comandos simples (hostname, uptime)
2. Teste comandos manualmente antes de automatizar
3. Implemente error handling gradualmente
4. Documente seus workflows
5. Use sub-workflows para operações complexas

---

**Documento Completo**: Veja `ssh-node-research.md` para detalhes extensivos

**Data**: 25 de Abril de 2026  
**Versão n8n**: 1.x+
