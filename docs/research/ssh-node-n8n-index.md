# Índice de Pesquisa - SSH Node n8n

**Data:** 25 de Abril de 2026  
**Tipo:** Pesquisa Técnica Especializada  
**Foco:** SSH node do n8n com foco em Windows

## 📊 Resumo da Pesquisa

Esta pesquisa abrangente cobre todos os aspectos do uso do SSH node do n8n, com especial atenção para ambiente Windows, segurança e troubleshooting.

### Palavras-chave

- n8n, SSH node, Windows, OpenSSH, PowerShell
- Autenticação SSH, chave privada, passphrase
- Automatização de servidores, DevOps, deploy
- Troubleshooting, erros comuns, soluções
- Workflows, automação, segurança

## 📁 Documentos Gerados

### 1. Guia Completo (ssh-node-research.md)
**Localização:** `docs/boas-praticas/n8n/nodes/ssh-node-research.md`  
**Tamanho:** ~8KB  
**Conteúdo:**
- 7 seções principais
- 40+ comandos PowerShell e Bash
- 6 erros comuns documentados
- 7 exemplos de workflows
- Referências completas

### 2. Resumo Executivo (ssh-node-resumo.md)
**Localização:** `docs/boas-praticas/n8n/nodes/ssh-node-resumo.md`  
**Tamanho:** ~5KB  
**Conteúdo:**
- Visão geral rápida
- Checklist de configuração
- Tabela de erros e soluções
- Comandos mais usados
- 5 exemplos de workflows

## 🔍 Fontes Consultadas

### Documentação Oficial
- n8n Docs - SSH Node
- n8n Docs - SSH Credentials
- n8n Integration Page

### Guias e Artigos
- VPS US Blog - Secure Your n8n Instance
- MassiveGRID - n8n Security Hardening Checklist
- Medium - Locking Down Your Workflows
- Contabo - 10 n8n Best Practices

### Comunidade
- n8n Community Forum (6 threads)
- GitHub Issues (2 issues)
- Reddit discussions

### Workflows de Exemplo
- Send Email if Server has Upgradable Packages
- Check VPS Resource Usage Every 15 Minutes
- Docker Registry Cleanup Workflow

## 💡 Principais Descobertas

### Configuração Windows
1. **PowerShell como shell padrão é crucial**
   ```powershell
   Set-ItemProperty -Path "HKLM:\SOFTWARE\OpenSSH" `
     -Name DefaultShell `
     -Value "C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe"
   ```

2. **Working Directory deve ser `null` para Windows**
   - Usar expressão: `{{null}}`
   - Ou deixar vazio

3. **OpenSSH nativo do Windows tem limitações**
   - Considerar instalar versão mais recente do GitHub

### Segurança
1. **N8N_ENCRYPTION_KEY é crucial**
   - Perder esta chave = perder todas credenciais
   - Usar `openssl rand -hex 32` para gerar

2. **Autenticação por chave é superior**
   - Chave + Passphrase = máxima segurança
   - Nunca usar senhas em produção

3. **Princípio do menor privilégio**
   - Criar usuário dedicado para automação
   - Evitar conta de Administrador

### Troubleshooting
1. **Erro "Cannot parse privateKey"**
   - Incluir linhas BEGIN/END da chave
   - Atualizar para n8n@0.127.0+

2. **Erro de sintaxe no Windows**
   - Configurar PowerShell como shell padrão
   - Usar `{{null}}` em Working Directory

3. **Conexão recusada**
   - Verificar se sshd está rodando
   - Confirmar regra de firewall

## 📈 Casos de Uso Documentados

### 1. Monitoramento
- Verificação de recursos a cada 15 minutos
- Alertas quando thresholds excedidos
- Relatórios por Slack/Email

### 2. Manutenção Automática
- Limpeza de logs antigos
- Atualizações de sistema
- Reinício de serviços

### 3. Deploy
- Deploy de containers Docker
- Deploy de aplicações
- Health checks pós-deploy

### 4. Backup
- Download de arquivos de configuração
- Compactação e upload para storage
- Backups agendados

### 5. Multi-Server
- Executar comando em múltiplos servidores
- Consolidar resultados
- Relatório agregado

## 🎯 Recomendações Práticas

### Para Iniciantes
1. Comece com comandos simples (hostname, uptime)
2. Teste comandos manualmente primeiro
3. Use autenticação por senha apenas para testes
4. Implemente error handling gradualmente

### Para Intermediários
1. Migre para autenticação por chave
2. Configure N8N_ENCRYPTION_KEY
3. Use sub-workflows para operações complexas
4. Implemente monitoramento e alertas

### Para Avançados
1. Implemente logging detalhado
2. Configure execução paralela
3. Use princípio do menor privilégio
4. Automatize rotação de credenciais

## 📚 Referências Rápidas

### Comandos PowerShell Mais Úteis
```powershell
# Sistema
hostname
systeminfo

# Disco
Get-PSDrive C | Select-Object Used,Free

# Serviços
Get-Service | Where-Object {$_.Status -eq 'Running'}
Restart-Service -Name "nginx" -Force

# Processos
Get-Process
Stop-Process -Name "notepad" -Force

# Arquivos
Get-ChildItem "C:\Logs" -File | Where-Object {$_.LastWriteTime -lt (Get-Date).AddDays(-30)} | Remove-Item -Force
```

### Comandos Linux Mais Úteis
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

## 🔗 Links Úteis

- **Docs Oficiais:** https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.ssh/
- **Comunidade:** https://community.n8n.io/
- **Workflows:** https://n8n.io/workflows/
- **GitHub:** https://github.com/n8n-io/n8n

## 📝 Notas de Pesquisa

### Metodologia
- Pesquisa usando Tavily MCP
- Busca por palavras-chave específicas
- Validação de múltiplas fontes
- Compilação de informações práticas

### Limitações
- Foco em Windows pode não se aplicar totalmente a Linux
- Alguns problemas podem estar corrigidos em versões futuras
- Sempre verificar documentação mais recente

### Próximos Passos Sugeridos
1. Testar comandos em ambiente de desenvolvimento
2. Implementar workflows de exemplo
3. Documentar casos de uso específicos do projeto
4. Criar templates reutilizáveis

---

**Pesquisador:** Agente de Pesquisa Tavily MCP  
**Data de Criação:** 25 de Abril de 2026  
**Status:** ✅ Completa
