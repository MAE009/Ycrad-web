#!/bin/bash
# build.sh - Script de build pour Render
set -o errexit

echo "🔨 Installation des dépendances système..."
apt-get update
apt-get install -y $(cat aptfile.txt)

echo "🐍 Installation des dépendances Python..."
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ Build terminé avec succès!"