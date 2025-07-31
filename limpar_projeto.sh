#!/bin/bash

echo "🧹 Limpando arquivos temporários e desnecessários..."

# Remove arquivos .Identifier
find . -name "*.Identifier" -type f -delete

# Remove caches do Python
find . -name "__pycache__" -type d -exec rm -r {} +
find . -name "*.pyc" -type f -delete
find . -name "*.pyo" -type f -delete

# Remove arquivos temporários de editores
find . -name "*~" -type f -delete
find . -name ".DS_Store" -type f -delete

echo "✅ Projeto limpo com sucesso!"
