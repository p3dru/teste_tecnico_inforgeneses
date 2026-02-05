# 🔧 Solução Definitiva: Problemas de Permissão no Kestra

## 🎯 Problema Resolvido

O erro `java.net.BindException: Permission denied` e problemas de volume foram **completamente resolvidos** através de um script de setup automatizado.

## ✅ Solução Implementada

### Script de Setup Automático (`setup.sh`)

Criamos um script que executa **UMA VEZ** e configura tudo automaticamente:

```bash
cd back
./setup.sh
```

**O que o script faz:**
1. ✅ Cria estrutura de diretórios
2. ✅ Copia `.env.example` para `.env` (se necessário)
3. ✅ Sobe todos os containers
4. ✅ **Fixa permissões do volume compartilhado** (usando Alpine container)
5. ✅ Gera o modelo de IA customizado
6. ✅ Verifica status final

## 🚀 Como Usar

### Primeira Instalação

```bash
cd back
./setup.sh
```

### Reset Completo (quando necessário)

```bash
cd back
docker-compose down -v  # Remove tudo
./setup.sh              # Reconfigura do zero
```

### Restarts Normais (sem perder dados)

```bash
docker-compose restart
# OU
docker-compose down && docker-compose up -d
```

## 🔍 Por Que Funciona?

### Problema Original
- Docker cria volumes com permissões **root:root** (700)
- Kestra roda como usuário **não-root** (UID 1000)
- Conflito de permissões impede acesso

### Nossa Solução
1. **Usamos um container Alpine** (que roda como root) para fixar permissões
2. **Executamos ANTES** de subir o Kestra
3. **Permissões 777** no `/shared-data` permitem acesso de qualquer UID
4. **Automático e reproduzível** - funciona sempre

## 📊 Verificação

### Confirmar que está funcionando:

```bash
# Ver status dos containers
docker-compose ps

# Todos devem estar "Up"
# Kestra deve estar em http://localhost:8080
```

### Se houver problemas:

```bash
# Ver logs do Kestra
docker-compose logs kestra

# Ver logs da API
docker-compose logs api
```

## 🛡️ Troubleshooting

### Erro: "Port 8080 already in use"

```bash
# Verificar o que está usando a porta
sudo lsof -i :8080

# Matar processo (se necessário)
sudo kill -9 <PID>
```

### Erro: "ContainerConfig" no docker-compose

```bash
# Remover container problemático
docker ps -a | grep kestra  # Pegar o ID
docker rm -f <CONTAINER_ID>

# Recriar
docker-compose up -d kestra
```

### Volume corrompido

```bash
# Remover volume específico
docker volume rm back_shared-data

# Rodar setup novamente
./setup.sh
```

## 📝 Arquivos Criados

- `setup.sh` - Script principal de configuração
- `PERMISSIONS_FIX.md` - Esta documentação
- `backend/scripts/init-api.sh` - Script auxiliar (não usado atualmente)
- `kestra/scripts/init-permissions.sh` - Script auxiliar (não usado atualmente)

## 🎓 Lições Aprendidas

1. **Volumes Docker** precisam de permissões corretas ANTES do uso
2. **Containers não-root** são mais seguros mas exigem planejamento
3. **Scripts de setup** são essenciais para reprodutibilidade
4. **Alpine containers** são perfeitos para tarefas de manutenção

## ✨ Benefícios da Solução

✅ **100% Automático** - Um comando resolve tudo  
✅ **Reproduzível** - Funciona em qualquer máquina  
✅ **Seguro** - Não requer sudo no host  
✅ **Resiliente** - Funciona após `down -v`  
✅ **Documentado** - Fácil de entender e manter

---

**Última atualização:** 2026-02-05  
**Status:** ✅ Testado e funcionando
