# Quick Start Guide

Get your cough detection bot running in 5 minutes!

## Prerequisites

- Python 3.8+
- FFmpeg installed
- A Discord account
- Admin access to a Discord server

## Step-by-Step Setup

### 1. Install Dependencies

```bash
# Install Python packages
pip install -r requirements.txt

# Install FFmpeg
# Ubuntu/Debian:
sudo apt install ffmpeg

# macOS:
brew install ffmpeg
```

### 2. Create Your Discord Bot

1. Visit https://discord.com/developers/applications
2. Click "New Application" → Give it a name (e.g., "Cough Police")
3. Go to "Bot" section → Click "Add Bot"
4. **Copy your bot token** (keep this secret!)
5. Enable these Privileged Gateway Intents:
   - ✅ Message Content Intent
   - ✅ Server Members Intent  
   - ✅ Presence Intent

### 3. Invite Bot to Your Server

1. In Developer Portal, go to "OAuth2" → "URL Generator"
2. Select scope: `bot`
3. Select permissions:
   - ✅ View Channels
   - ✅ Send Messages
   - ✅ Connect
   - ✅ Speak
   - ✅ Use Voice Activity
4. Copy the generated URL and open in browser
5. Select your server and click "Authorize"

### 4. Configure the Bot

```bash
# Copy the example config
cp .env.example .env

# Edit .env with your values
nano .env  # or use your favorite editor
```

Fill in these values:
```
DISCORD_TOKEN=your_bot_token_from_step_2
TEXT_CHANNEL_ID=your_text_channel_id
VOICE_CHANNEL_ID=your_voice_channel_id  # optional
```

**Getting Channel IDs:**
1. In Discord: Settings → Advanced → Enable "Developer Mode"
2. Right-click any channel → "Copy ID"

### 5. Generate the Audio File (Optional)

```bash
python generate_sound.py
```

This creates a polite beep sound. Skip this step if you want to provide your own MP3 file.

### 6. Run the Bot

```bash
# Check everything is set up correctly
python setup.py

# Start the bot
python bot.py
```

You should see: `CoughDetectionBot#1234 has connected to Discord!`

### 7. Test It Out

1. Join a voice channel in your Discord server
2. In a text channel, type: `!join`
3. The bot joins your voice channel
4. Make a cough sound (or play a cough sound effect)
5. Watch the bot respond! 🎉

## Quick Commands

- `!join` - Bot joins your voice channel
- `!leave` - Bot leaves voice channel  
- `!status` - Check bot status

## Troubleshooting

**Bot won't detect my cough?**
- Lower the `VOLUME_THRESHOLD` in `.env` (try 300 or 200)
- Speak/cough louder
- Check your microphone is working

**Bot can't join voice channel?**
- Verify bot permissions in Discord
- Check `VOICE_CHANNEL_ID` is correct

**No sound plays?**
- Run `python generate_sound.py` to create the audio file
- Verify FFmpeg is installed: `ffmpeg -version`

## What's Next?

- Customize the detection sensitivity in `.env`
- Add your own audio file in `assets/stop_coughing.mp3`
- Set up auto-join by configuring `VOICE_CHANNEL_ID`

## Need Help?

Check the full [README.md](README.md) for detailed information or open an issue on GitHub.

---

Happy cough detecting! 🤧
