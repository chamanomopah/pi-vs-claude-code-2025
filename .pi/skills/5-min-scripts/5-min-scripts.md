---
name: 5-min-scripts
description: fazer um script rápido em python para resolver um problema específico 
allowed-tools: read,write,edit,bash,grep,find,ls
---

# ativação

- so deve ser ativado quando o usuario pedir pra criar um script em 5 minutos ou quando pedir pra um scripts simples pra resolver um problema especifico

# 5-Minute Scripts

- a ideia é criar scripts rápidos para resolver problemas específicos
- o foco é na simplicidade e rapidez, não na robustez ou escalabilidade
- o script deve ser testado como um humano testaria, é inaceitável que o script seja criado e não seja testado em condições reais, não py test e sim rodando o script com bash pra ver como ele se comporta que o usuario usaria pra garantir que o usuario não se fruste quando fazer funcionar
- os scripts devem ser escritos em Python, mas podem usar outras linguagens se necessário
- deve ter o minimo de arquivos possiveis pra resolver o problema, idealmente um unico arquivo 
- caso o script pedido ter variaveis de uso, scripts em py devem ter variaveis e flags pra ficar dinamico e ter variados resultados ex: py script "variavel" --flag

- precisa ser validado no minimo em 5 use cases pra garantir bom funcionamento

# resultado

- crie o script em scripts/ pra manter organizado
