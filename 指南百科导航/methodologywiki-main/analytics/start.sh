#!/bin/bash
# WisdomWiki Analytics Dashboard — Start Script
set -e

cd "$(dirname "$0")"

echo "📊 WisdomWiki Analytics Dashboard"
echo "=================================="

# Create venv if not exists
if [ ! -d "venv" ]; then
  echo "→ Creating virtual environment..."
  python3 -m venv venv
fi

# Activate and install deps
source venv/bin/activate
echo "→ Installing dependencies..."
pip install -q -r requirements.txt

echo ""
echo "→ Starting server..."
python server.py
