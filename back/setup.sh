#!/bin/bash
# Script para configuração inicial do ambiente
# Execute este script UMA VEZ após clonar o projeto

set -e

echo "🚀 Configurando ambiente do projeto..."

# 1. Criar diretórios necessários
echo "📁 Criando estrutura de diretórios..."
mkdir -p kestra/flows kestra/scripts backend/scripts shared-data/uploads shared-data/models

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

# Configurar diretórios locais (agora via bind mount)
mkdir -p shared-data/uploads shared-data/models
chmod -R 777 shared-data

# Configurar Docker Socket (precisa de acesso privilegiado ou via docker trick)
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock alpine sh -c "
    chmod 666 /var/run/docker.sock &&
    echo '✅ Docker Socket configurado!'
"

# 6. Gerar modelo customizado (APENAS se não existir)
echo "🤖 Verificando modelo de IA..."
docker run --rm -v "$(pwd)/shared-data:/data" --entrypoint python ultralytics/ultralytics:latest -c "
from ultralytics import YOLO
import os

model_path = '/data/models/custom_fire_model.pt'

if os.path.exists(model_path):
    print(f'✅ Modelo customizado já existe em {model_path}. Pulando geração.')
else:
    print('⚠️ Modelo não encontrado. Gerando modelo padrão (YOLOv8n)...')
    os.makedirs('/data/models', exist_ok=True)
    model = YOLO('yolov8n.pt')
    model.save(model_path)
    print('✅ Modelo padrão gerado com sucesso!')
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
