#!/bin/bash
# Script para configuração inicial do ambiente
# Execute este script UMA VEZ após clonar o projeto

set -e

echo "🚀 Configurando ambiente do projeto..."

# 1. Criar diretórios necessários
echo "📁 Criando estrutura de diretórios..."
mkdir -p kestra/flows kestra/scripts backend/scripts

# 2. Verificar se .env existe
if [ ! -f ".env" ]; then
    echo "📝 Criando .env a partir do .env.example..."
    cp .env.example .env
    echo "⚠️  IMPORTANTE: Edite o arquivo .env com suas credenciais!"
else
    echo "✅ Arquivo .env já existe"
fi

# 3. Subir containers
echo "🐳 Iniciando containers..."
docker-compose up -d

# 4. Aguardar containers iniciarem
echo "⏳ Aguardando containers iniciarem..."
sleep 10

# 5. Fixar permissões do volume compartilhado e Docker Socket
echo "🔧 Configurando permissões do volume e Docker Socket..."
docker run --rm -v back_shared-data:/data -v /var/run/docker.sock:/var/run/docker.sock alpine sh -c "
    mkdir -p /data/uploads /data/models && 
    chmod -R 777 /data &&
    chmod 666 /var/run/docker.sock &&
    echo '✅ Permissões configuradas com sucesso!'
"

# 6. Gerar modelo customizado
echo "🤖 Gerando modelo de IA customizado..."
docker run --rm -v back_shared-data:/data --entrypoint python ultralytics/ultralytics:latest -c "
from ultralytics import YOLO
import os
os.makedirs('/data/models', exist_ok=True)
model = YOLO('yolov8n.pt')
model.save('/data/models/custom_fire_model.pt')
print('✅ Modelo gerado com sucesso!')
"

# 7. Verificar status
echo ""
echo "📊 Status dos containers:"
docker-compose ps

echo ""
echo "✅ Setup concluído!"
echo ""
echo "📋 Próximos passos:"
echo "1. Acesse http://localhost:8080 (Kestra UI)"
echo "2. Faça login e registre o flow manualmente (veja README.md)"
echo "3. Acesse http://localhost:3000 (Frontend)"
echo ""
echo "🔄 Para resetar tudo e reconfigurar:"
echo "   docker-compose down -v && ./setup.sh"
