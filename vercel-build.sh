#!/bin/bash

# Script de build para o Vercel
echo "Usando Python $(python --version)"
echo "Instalando dependências com Python 3.9..."
python3.9 -m pip install -r requirements.txt

echo "Build concluído!" 