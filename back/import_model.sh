#!/bin/bash
# Script para facilitar a importação do modelo treinado para o volume Docker

if [ -z "$1" ]; then
  echo "❌ Erro: Caminho do arquivo não especificado."
  echo "Uso: ./import_model.sh <caminho_para_arquivo.pt>"
  echo "Exemplo: ./import_model.sh ~/Downloads/best.pt"
  exit 1
fi

MODEL_PATH=$(realpath "$1")

if [ ! -f "$MODEL_PATH" ]; then
  echo "❌ Erro: Arquivo '$MODEL_PATH' não encontrado."
  exit 1
fi

echo "🚀 Importando modelo para o sistema..."
echo "📂 Origem: $MODEL_PATH"

# Usar container auxiliar para copiar arquivo para dentro do volume
# Assume que o volume se chama 'back_shared-data' (padrão do docker-compose na pasta 'back')
docker run --rm \
  -v back_shared-data:/data \
  -v "$MODEL_PATH":/tmp/new_model.pt \
  alpine sh -c "mkdir -p /data/models && cp /tmp/new_model.pt /data/models/custom_fire_model.pt && chmod 777 /data/models/custom_fire_model.pt"

if [ $? -eq 0 ]; then
  echo ""
  echo "✅ Modelo importado com sucesso!"
  echo "📍 Salvo em: /shared-data/models/custom_fire_model.pt (dentro do Docker)"
  echo ""
  echo "🔄 Reiniciando API para aplicar mudanças..."
  docker-compose restart api
  echo "✅ Pronto! O novo modelo já está sendo usado."
else
  echo ""
  echo "❌ Falha ao importar modelo."
  echo "Verifique se o volume 'back_shared-data' existe (o projeto está rodando?)."
fi
