# GitHub Codespaces Configuration

This directory contains the configuration for running the Discord Cough Bot in GitHub Codespaces.

## What is GitHub Codespaces?

GitHub Codespaces provides a complete, cloud-hosted development environment that's accessible from your browser. No local setup required!

## Getting Started with Codespaces

### 1. Open in Codespaces

From the repository on GitHub:
1. Click the green "Code" button
2. Select the "Codespaces" tab
3. Click "Create codespace on main" (or your branch)

GitHub will automatically:
- Create a containerized development environment
- Install Python 3.11
- Install FFmpeg for audio processing
- Install all Python dependencies from `requirements.txt`
- Set up the project structure

### 2. Configure Your Bot

Once the Codespace is ready:

```bash
# Edit the .env file with your Discord credentials
# (A template .env file is already created for you)
nano .env
```

Add your Discord bot token and channel IDs:
```
DISCORD_TOKEN=your_bot_token_here
TEXT_CHANNEL_ID=your_text_channel_id
VOICE_CHANNEL_ID=your_voice_channel_id
```

### 3. Run the Bot

```bash
# (Optional) Generate a test sound file
python generate_sound.py

# Start the bot
python bot.py
```

## Configuration Details

### devcontainer.json

The main configuration file that defines:
- **Base Image**: Python 3.11 container
- **Features**: Common utilities, zsh shell
- **VS Code Extensions**: Python, Pylance for better development experience
- **Post-Create Command**: Runs `setup.sh` to install dependencies

### setup.sh

Automated setup script that:
1. Updates package lists
2. Installs FFmpeg
3. Installs Python dependencies
4. Creates `.env` file from template
5. Creates assets directory

## Limitations in Codespaces

### Audio Playback
- Codespaces runs in a container without audio output devices
- The bot can still detect coughs and post messages
- Audio file playback will work for Discord but you won't hear it locally
- This is normal and expected behavior

### Voice Channel Audio
- The bot can join voice channels and receive audio
- Audio processing and cough detection work normally
- Responses are posted to Discord, which you'll see in the Discord client

## Development Workflow

### Testing the Bot

Since Codespaces doesn't have audio I/O, test the bot by:

1. **Use Discord Client**: Open Discord in a browser tab or desktop app
2. **Join Voice Channel**: Have the bot join using `!join` command
3. **Test Detection**: Play cough sounds in the voice channel
4. **Check Responses**: Verify messages appear in the text channel

### Debugging

View logs in the Codespace terminal:
```bash
python bot.py
```

All bot activity (connections, detections, errors) is logged to the console.

### Making Changes

1. Edit files in the Codespace using VS Code
2. The environment automatically saves to GitHub
3. Test your changes by running `python bot.py`
4. Commit and push when ready

## Troubleshooting

### FFmpeg Not Found

If you see "FFmpeg not found" errors:
```bash
sudo apt-get update
sudo apt-get install -y ffmpeg
```

### Python Dependencies Missing

Reinstall dependencies:
```bash
pip install -r requirements.txt
```

### Bot Won't Connect

Check your `.env` file:
- Verify `DISCORD_TOKEN` is set correctly
- Ensure channel IDs are valid integers
- Check bot permissions in Discord Developer Portal

## Additional Resources

- [GitHub Codespaces Documentation](https://docs.github.com/en/codespaces)
- [Dev Container Specification](https://containers.dev/)
- Main project [README.md](../README.md)
- Quick setup [QUICKSTART.md](../QUICKSTART.md)

## Updating the Configuration

To modify the Codespace setup:

1. Edit `devcontainer.json` for container settings
2. Edit `setup.sh` for post-creation commands
3. Rebuild the container: Command Palette → "Codespaces: Rebuild Container"

## Cost Considerations

GitHub Codespaces usage:
- Free tier: 60 hours/month for personal accounts
- The bot itself uses minimal resources
- Consider stopping the Codespace when not actively developing
- The bot can run on free tier for testing and development

Stop a Codespace:
- GitHub.com → Your Codespaces → Stop

## Running the Bot Long-Term

For production deployment, consider:
- **GitHub Actions**: Run bot as a workflow (limited)
- **Cloud Hosting**: Deploy to AWS, GCP, Azure, or DigitalOcean
- **Docker**: Use the included `docker-compose.yml`
- **Local Machine**: Run on your own computer

Codespaces is ideal for development and testing, but not for 24/7 bot hosting.
