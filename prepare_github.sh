#!/bin/bash
# Script para preparar e subir o projeto no GitHub

set -e

echo "🚀 Preparando projeto para GitHub..."
echo ""

# 1. Remover diretório backend antigo do Git
echo "📁 Removendo diretório backend/ antigo..."
git rm -r backend/ 2>/dev/null || echo "  ℹ️  Diretório já removido"

# 2. Adicionar todos os arquivos
echo "➕ Adicionando arquivos ao Git..."
git add .

# 3. Mostrar status
echo ""
echo "📊 Status do repositório:"
git status --short

# 4. Mostrar o que será commitado
echo ""
echo "📝 Arquivos que serão commitados:"
git diff --cached --name-status

echo ""
echo "✅ Preparação concluída!"
echo ""
echo "📋 Próximos passos:"
echo "1. Revise os arquivos acima"
echo "2. Execute: git commit -m 'feat: complete MLOps wildfire detection system'"
echo "3. Crie um repositório no GitHub: https://github.com/new"
echo "4. Execute: git remote add origin https://github.com/SEU-USUARIO/SEU-REPO.git"
echo "5. Execute: git push -u origin main"
echo ""
echo "📖 Veja GITHUB_GUIDE.md para instruções detalhadas"
