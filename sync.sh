#!/bin/bash

# Terminate execution if any individual compilation step encounters an error
set -e

# Capture the commit description from the command line argument (Default fallback if empty)
COMMIT_MSG="${1:-Update technical register datasets and sync documentation tracks}"

echo "=================================================="
echo "🚀 Starting Extended Rukwangali Sync Pipeline..."
echo "=================================================="

# 1. Execute the Python database extraction engine to update the web Markdown layouts
echo "📁 Parsing Typst dictionary and updating domain tracks..."
python3 generate_web_tables.py

# 2. Stage all updated data structures, documentation text, and Typst build modules
echo "📦 Staging workspace modifications into Git tracking..."
git add .

# 3. Commit files using your custom log description
echo "💾 Documenting commit state..."
git commit -m "$COMMIT_MSG"

# 4. Push the programmatic database records upstream to GitHub
echo "☁️  Syncing source assets to remote GitHub repository..."
git push origin main

# 5. Compile the Markdown sheets and launch the updated web configuration to GitHub Pages
echo "🌐 Re-compiling and deploying searchable web application portal..."
mkdocs gh-deploy --clean

echo "=================================================="
echo "🎉 System Sync Complete! Your updates are live at:"
echo "👉 https://github.io"
echo "=================================================="
