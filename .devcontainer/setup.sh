#!/bin/bash

# GitHub Codespaces setup script for Discord Cough Detection Bot
echo "🚀 Setting up Discord Cough Bot in GitHub Codespaces..."
echo "=================================================="

# Update package lists
echo "📦 Updating package lists..."
sudo apt-get update -q

# Install FFmpeg (required for audio processing)
echo "🎵 Installing FFmpeg..."
sudo apt-get install -y ffmpeg

# Verify FFmpeg installation
if command -v ffmpeg &> /dev/null; then
    echo "✅ FFmpeg installed: $(ffmpeg -version | head -n1)"
else
    echo "❌ FFmpeg installation failed"
    exit 1
fi

# Install Python dependencies
echo "🐍 Installing Python dependencies..."
pip install --quiet -r requirements.txt

# Verify key packages (import using the actual module names)
echo "📋 Verifying Python packages..."
python3 -c "import discord; import numpy; import dotenv; print('✅ All Python packages installed')" || {
    echo "❌ Python package installation failed"
    exit 1
}

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env with your Discord bot credentials"
fi

# Create assets directory if it doesn't exist
mkdir -p assets

echo ""
echo "=================================================="
echo "✅ Setup complete!"
echo ""
echo "📚 Next steps:"
echo "1. Edit .env file with your Discord bot token and channel IDs"
echo "2. (Optional) Generate test sound: python generate_sound.py"
echo "3. Run the bot: python bot.py"
echo ""
echo "💡 Quick start guide: see QUICKSTART.md"
echo "=================================================="
