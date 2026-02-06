# 📦 Guia de Instalação Completo - Wildfire Detection System

## 📋 Índice

1. [Pré-requisitos](#-pré-requisitos)
2. [Instalação Passo a Passo](#-instalação-passo-a-passo)
3. [Verificação da Instalação](#-verificação-da-instalação)
4. [Troubleshooting Completo](#-troubleshooting-completo)
5. [FAQ](#-faq)

---

## 🔧 Pré-requisitos

### Sistema Operacional
- ✅ Linux (Ubuntu 20.04+, Debian 11+)
- ✅ macOS (Big Sur 11+)
- ✅ Windows 10/11 (com WSL2)

### Software Necessário

| Software | Versão Mínima | Como Verificar | Como Instalar |
|----------|---------------|----------------|---------------|
| **Docker** | 20.10+ | `docker --version` | [Instalar Docker](https://docs.docker.com/get-docker/) |
| **Docker Compose** | 2.0+ | `docker-compose --version` | Incluído no Docker Desktop |
| **Node.js** | 18.0+ | `node --version` | [Instalar Node.js](https://nodejs.org/) |
| **npm** | 9.0+ | `npm --version` | Incluído no Node.js |
| **Git** | 2.30+ | `git --version` | [Instalar Git](https://git-scm.com/) |

### Recursos do Sistema
- **RAM:** Mínimo 4GB (Recomendado 8GB+)
- **Disco:** Mínimo 10GB livres
- **CPU:** 2 cores (Recomendado 4+)

---

## 🚀 Instalação Passo a Passo

### **Passo 1: Clonar o Repositório**

```bash
# Clone o repositório
git clone https://github.com/p3dru/teste_tecnico_inforgeneses.git

# Entre no diretório
cd teste_tecnico_inforgeneses
```

**Verificação:**
```bash
ls -la
# Deve mostrar: back/, front/, README.md, etc.
```

**❌ Erro Comum:** `Permission denied (publickey)`
- **Solução:** Use HTTPS ao invés de SSH:
  ```bash
  git clone https://github.com/p3dru/teste_tecnico_inforgeneses.git
  ```

---

### **Passo 2: Configurar Backend**

```bash
# Entre no diretório backend
cd back

# Copie o template de variáveis de ambiente
cp .env.example .env

# (Opcional) Edite o .env se quiser mudar senhas
nano .env  # ou vim, code, etc.
```

**Conteúdo do `.env` (valores padrão funcionam):**
```bash
# Database
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DB=wildfire_db

# MongoDB
MONGO_INITDB_ROOT_USERNAME=user
MONGO_INITDB_ROOT_PASSWORD=password

# JWT (pode deixar como está)
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Kestra (será preenchido depois)
KESTRA_USER=admin@kestra.io
KESTRA_PASSWORD=kestra
```

**❌ Erro Comum:** `.env` não encontrado
- **Solução:** Certifique-se de estar no diretório `back/`
  ```bash
  pwd  # Deve mostrar: .../teste_tecnico_inforgeneses/back
  ```

---

### **Passo 3: Executar Setup Automatizado**

```bash
# Ainda no diretório back/
./setup.sh
```

**O que o script faz:**
1. ✅ Cria diretórios necessários
2. ✅ Sobe containers Docker (Postgres, MongoDB, Kestra, API)
3. ✅ Corrige permissões do volume compartilhado
4. ✅ Gera modelo AI customizado
5. ✅ Verifica status dos serviços

**Saída esperada:**
```
🚀 Iniciando setup do sistema...
✅ Diretórios criados
✅ Containers iniciados
✅ Permissões corrigidas
✅ Modelo AI gerado
✅ Setup concluído!
```

**❌ Erro: `Permission denied: ./setup.sh`**
- **Solução:**
  ```bash
  chmod +x setup.sh
  ./setup.sh
  ```

**❌ Erro: `docker: command not found`**
- **Solução:** Instale o Docker:
  - **Ubuntu/Debian:**
    ```bash
    sudo apt update
    sudo apt install docker.io docker-compose
    sudo systemctl start docker
    sudo usermod -aG docker $USER
    # Faça logout e login novamente
    ```
  - **macOS:** Instale [Docker Desktop](https://www.docker.com/products/docker-desktop)
  - **Windows:** Instale [Docker Desktop](https://www.docker.com/products/docker-desktop) + WSL2

**❌ Erro: `port 8080 is already allocated`**
- **Solução:** Outra aplicação está usando a porta. Mate o processo:
  ```bash
  # Linux/macOS
  sudo lsof -i :8080
  sudo kill -9 <PID>
  
  # Ou mude a porta no docker-compose.yml
  ```

**❌ Erro: `Cannot connect to the Docker daemon`**
- **Solução:**
  ```bash
  # Inicie o Docker
  sudo systemctl start docker  # Linux
  # ou abra Docker Desktop (macOS/Windows)
  
  # Adicione seu usuário ao grupo docker
  sudo usermod -aG docker $USER
  newgrp docker  # ou faça logout/login
  ```

---

### **Passo 4: Configurar Kestra (CRÍTICO)**

Este é o **único passo manual obrigatório**.

#### 4.1. Acessar Kestra UI

```bash
# Abra no navegador
http://localhost:8080
```

#### 4.2. Criar Primeiro Usuário

Na primeira vez, o Kestra pedirá para criar um usuário admin:

1. **Email:** `admin@kestra.io` (ou qualquer email)
2. **Password:** `kestra` (ou qualquer senha)
3. Clique em **Create**

**⚠️ IMPORTANTE:** Anote essas credenciais!

#### 4.3. Atualizar .env com as Credenciais

```bash
# Edite o arquivo .env
nano back/.env

# Atualize estas linhas com as credenciais que você criou:
KESTRA_USER=admin@kestra.io
KESTRA_PASSWORD=kestra
```

#### 4.4. Reiniciar API

```bash
cd back
docker-compose restart api
```

**Verificação:**
```bash
docker-compose logs api | grep "Kestra"
# Deve mostrar: "Kestra client initialized"
```

#### 4.5. Registrar Flow de Inferência

1. No Kestra UI, vá em **Flows** (menu lateral)
2. Clique em **Create** (botão superior direito)
3. Copie todo o conteúdo de `back/kestra/flows/fire_inference.yaml`
4. Cole no editor do Kestra
5. Clique em **Save**

**Verificação:**
- Você deve ver o flow `fire_inference` na lista de flows
- Status: `ENABLED`

**❌ Erro: "Invalid YAML"**
- **Solução:** Certifique-se de copiar TODO o conteúdo do arquivo, incluindo o cabeçalho

**❌ Erro: "Namespace not found"**
- **Solução:** O flow cria o namespace automaticamente. Apenas salve.

---

### **Passo 5: Configurar Frontend**

```bash
# Volte para a raiz do projeto
cd ..

# Entre no diretório frontend
cd front

# Copie o template de variáveis
cp .env.local.example .env.local

# Instale dependências
npm install

# Inicie o servidor de desenvolvimento
npm run dev
```

**Saída esperada:**
```
ready - started server on 0.0.0.0:3000
```

**❌ Erro: `npm: command not found`**
- **Solução:** Instale Node.js:
  - **Ubuntu/Debian:**
    ```bash
    curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
    sudo apt install -y nodejs
    ```
  - **macOS:** `brew install node`
  - **Windows:** Baixe de [nodejs.org](https://nodejs.org/)

**❌ Erro: `EACCES: permission denied`**
- **Solução:**
  ```bash
  sudo chown -R $USER:$USER ~/.npm
  npm install
  ```

**❌ Erro: `port 3000 already in use`**
- **Solução:** Mate o processo ou use outra porta:
  ```bash
  # Matar processo
  lsof -ti:3000 | xargs kill -9
  
  # Ou usar porta diferente
  PORT=3001 npm run dev
  ```

**❌ Erro: `Module not found: Can't resolve 'next'`**
- **Solução:** Limpe cache e reinstale:
  ```bash
  rm -rf node_modules package-lock.json
  npm install
  ```

---

## ✅ Verificação da Instalação

### Checklist de Serviços

Execute estes comandos para verificar se tudo está funcionando:

```bash
# 1. Verificar containers Docker
cd back
docker-compose ps
```

**Esperado:**
```
NAME              STATUS
back_api_1        Up (healthy)
back_kestra_1     Up
back_mongo_1      Up
back_postgres_1   Up (healthy)
```

```bash
# 2. Verificar API
curl http://localhost:8000/docs
# Deve retornar HTML do Swagger UI
```

```bash
# 3. Verificar Kestra
curl http://localhost:8080
# Deve retornar HTML da UI do Kestra
```

```bash
# 4. Verificar Frontend
curl http://localhost:3000
# Deve retornar HTML do Next.js
```

### Teste End-to-End Rápido

1. **Acesse:** http://localhost:3000
2. **Clique em:** "Sign Up"
3. **Crie conta:** `test@test.com` / `test123`
4. **Faça login**
5. **Faça upload** de qualquer imagem
6. **Aguarde** ~30 segundos
7. **Verifique** se o report aparece com status "DONE"

**✅ Se funcionou, instalação completa!**

---

## 🐛 Troubleshooting Completo

### Problema: Containers não sobem

**Sintomas:**
```bash
docker-compose ps
# Mostra containers com status "Exit" ou "Restarting"
```

**Diagnóstico:**
```bash
docker-compose logs <nome-do-container>
```

**Soluções:**

1. **Postgres não inicia:**
   ```bash
   # Limpar volumes e recriar
   docker-compose down -v
   docker-compose up -d
   ```

2. **Kestra não inicia:**
   ```bash
   # Verificar memória disponível
   free -h  # Precisa de pelo menos 2GB livres
   
   # Aumentar memória do Docker (Docker Desktop)
   # Settings → Resources → Memory → 4GB+
   ```

3. **API não inicia:**
   ```bash
   # Verificar logs
   docker-compose logs api
   
   # Erro comum: "Database connection failed"
   # Solução: Aguardar Postgres iniciar completamente
   docker-compose restart api
   ```

---

### Problema: Upload retorna erro 500

**Sintomas:**
- Upload de imagem falha
- Console mostra "Internal Server Error"

**Diagnóstico:**
```bash
docker-compose logs api | tail -50
```

**Soluções:**

1. **Permissão negada no volume:**
   ```bash
   # Executar fix de permissões
   cd back
   docker exec back_kestra_1 chmod -R 777 /shared-data
   docker-compose restart api
   ```

2. **Kestra não autenticado:**
   ```bash
   # Verificar .env
   cat .env | grep KESTRA
   
   # Deve ter:
   KESTRA_USER=admin@kestra.io  # Suas credenciais
   KESTRA_PASSWORD=kestra
   
   # Reiniciar API
   docker-compose restart api
   ```

3. **Flow não registrado:**
   - Acesse http://localhost:8080
   - Vá em **Flows**
   - Verifique se `fire_inference` está lá
   - Se não, registre conforme Passo 4.5

---

### Problema: Kestra não executa o flow

**Sintomas:**
- Upload funciona
- Report fica em "PROCESSING" para sempre
- Kestra não mostra execuções

**Diagnóstico:**
```bash
# Verificar logs do Kestra
docker-compose logs kestra | grep "fire_inference"
```

**Soluções:**

1. **Trigger não configurado:**
   - O flow é trigado via API, não automaticamente
   - Verifique se a API está chamando o Kestra:
     ```bash
     docker-compose logs api | grep "Triggering Kestra"
     ```

2. **Docker runner não funciona:**
   ```bash
   # Verificar se Kestra tem acesso ao Docker socket
   docker-compose exec kestra docker ps
   
   # Se der erro, adicione ao docker-compose.yml:
   volumes:
     - /var/run/docker.sock:/var/run/docker.sock
   ```

3. **Modelo AI não encontrado:**
   ```bash
   # Verificar se modelo existe
   docker exec back_kestra_1 ls -lh /shared-data/models/
   
   # Deve mostrar: custom_fire_model.pt (6.3M)
   
   # Se não existir, gerar novamente:
   cd back
   ./setup.sh
   ```

---

### Problema: Frontend não conecta com API

**Sintomas:**
- Login falha
- Console mostra "Network Error"
- CORS errors

**Diagnóstico:**
```bash
# Verificar .env.local do frontend
cat front/.env.local
```

**Soluções:**

1. **URL da API incorreta:**
   ```bash
   # Editar front/.env.local
   NEXT_PUBLIC_API_URL=http://localhost:8000
   
   # Reiniciar frontend
   npm run dev
   ```

2. **API não está rodando:**
   ```bash
   curl http://localhost:8000/docs
   
   # Se falhar:
   cd back
   docker-compose up -d api
   ```

3. **CORS bloqueado:**
   - Verifique se está acessando via `localhost` (não `127.0.0.1`)
   - O backend já tem CORS configurado para `localhost:3000`

---

### Problema: Banco de dados vazio após restart

**Sintomas:**
- Após `docker-compose down`, dados são perdidos
- Usuários e reports desaparecem

**Solução:**
```bash
# NÃO use -v (remove volumes)
docker-compose down

# Use apenas:
docker-compose down  # Mantém volumes
docker-compose up -d

# Para limpar TUDO (cuidado!):
docker-compose down -v  # Remove volumes e dados
```

---

### Problema: Testes não passam

**Sintomas:**
```bash
cd back/backend
./run_tests_venv.sh
# Falhas nos testes
```

**Soluções:**

1. **Dependências faltando:**
   ```bash
   # Criar venv e instalar
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   pip install -r tests/requirements-test.txt
   ```

2. **Banco de teste com erro:**
   ```bash
   # Limpar banco de teste
   rm -f /tmp/test_wildfire.db
   ./run_tests_venv.sh
   ```

---

## ❓ FAQ

### Q: Preciso ter GPU para rodar?
**A:** Não. O YOLOv8 roda em CPU (mais lento, mas funciona).

### Q: Posso mudar as portas?
**A:** Sim. Edite `docker-compose.yml` e `.env.local`.

### Q: Como parar tudo?
**A:**
```bash
# Parar containers (mantém dados)
cd back
docker-compose down

# Parar frontend
# Ctrl+C no terminal do npm
```

### Q: Como limpar tudo e recomeçar?
**A:**
```bash
cd back
docker-compose down -v  # Remove volumes
rm -rf shared-data/
./setup.sh  # Reconfigura tudo
```

### Q: Posso usar em produção?
**A:** Este é um projeto de demonstração. Para produção:
- Mude todas as senhas
- Use HTTPS
- Configure firewall
- Use banco de dados gerenciado
- Configure backups

### Q: Como atualizar o código?
**A:**
```bash
git pull origin main
cd back
docker-compose down
docker-compose up -d --build
cd ../front
npm install
npm run dev
```

---

## 📞 Suporte

Se encontrar problemas não cobertos aqui:

1. **Verifique os logs:**
   ```bash
   docker-compose logs <serviço>
   ```

2. **Consulte a documentação:**
   - `README.md` - Visão geral
   - `back/PERMISSIONS_FIX.md` - Problemas de permissão
   - `back/TRAINING.md` - Treinar modelo customizado

3. **Abra uma issue no GitHub:**
   https://github.com/p3dru/teste_tecnico_inforgeneses/issues

---

## ✅ Próximos Passos

Após instalação bem-sucedida:

1. 📖 Leia `back/TRAINING.md` para treinar um modelo real
2. 🧪 Execute os testes: `cd back/backend && ./run_tests_venv.sh`
3. 🎨 Customize o frontend em `front/`
4. 🚀 Faça deploy (consulte documentação de deploy)

**Boa sorte! 🔥**
