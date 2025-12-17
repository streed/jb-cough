# jb-cough 🤧

A Discord bot that listens to voice chat, detects when someone coughs, and posts a message to the main Discord chat channel. It also plays a sound to remind them to mute themselves.

## Features

- 🎤 **Voice Channel Monitoring**: Listens to audio in Discord voice channels
- 🔍 **Cough Detection**: Uses audio analysis to detect cough patterns
- 💬 **Automatic Notifications**: Posts messages to a text channel when coughs are detected
- 🔊 **Audio Feedback**: Plays a sound in the voice channel to remind users to mute
- ⚡ **Cooldown System**: Prevents spam by limiting notifications
- 🤖 **Simple Commands**: Easy-to-use bot commands for control

## Requirements

- Python 3.8 or higher
- FFmpeg (for audio processing)
- A Discord Bot Token
- Discord Server with appropriate permissions

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/streed/jb-cough.git
cd jb-cough
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Install FFmpeg

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Windows:**
Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH.

### 4. Create a Discord Bot

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and give it a name
3. Go to the "Bot" section and click "Add Bot"
4. Copy the bot token (you'll need this for the `.env` file)
5. Enable the following Privileged Gateway Intents:
   - Message Content Intent
   - Server Members Intent
   - Presence Intent

### 5. Invite the Bot to Your Server

1. In the Discord Developer Portal, go to "OAuth2" → "URL Generator"
2. Select scopes: `bot`
3. Select permissions:
   - View Channels
   - Send Messages
   - Connect (to voice channels)
   - Speak (in voice channels)
   - Use Voice Activity
4. Copy the generated URL and open it in your browser
5. Select your server and authorize the bot

### 6. Configure the Bot

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and fill in your values:
   ```
   DISCORD_TOKEN=your_bot_token_here
   TEXT_CHANNEL_ID=your_text_channel_id_here
   VOICE_CHANNEL_ID=your_voice_channel_id_here
   ```

   To get channel IDs:
   - Enable Developer Mode in Discord (User Settings → Advanced → Developer Mode)
   - Right-click on a channel and select "Copy ID"

3. (Optional) Add an audio file:
   - Place an MP3 file at `assets/stop_coughing.mp3`
   - Or generate one using the instructions in `assets/README.md`

## Usage

### Running the Bot

**Standard Method:**
```bash
python bot.py
```

**Using Docker:**
```bash
# Build and run with docker-compose
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the bot
docker-compose down
```

The bot will connect to Discord and start monitoring voice channels.

### Bot Commands

Once the bot is running, you can use these commands in any text channel:

- `!join` - Make the bot join your current voice channel
- `!leave` - Make the bot leave the voice channel
- `!status` - Check the bot's current status

### Automatic Behavior

If you configure `VOICE_CHANNEL_ID` in the `.env` file, the bot will automatically join that voice channel when someone else joins it.

## How It Works

1. **Audio Capture**: The bot connects to a voice channel and captures audio streams from users
2. **Audio Analysis**: Each audio chunk is analyzed using signal processing techniques
3. **Cough Detection**: The bot looks for characteristics typical of coughs:
   - Sudden volume spikes
   - High peak-to-RMS ratio (indicates burst of sound)
   - Energy levels above threshold
4. **Response**: When a cough is detected:
   - A message is posted to the configured text channel mentioning the user
   - An audio file is played in the voice channel (if available)
   - A cooldown prevents spam (3 seconds between detections per user)

## Configuration Options

Edit `.env` to customize behavior:

| Variable | Description | Default |
|----------|-------------|---------|
| `DISCORD_TOKEN` | Your bot's token from Discord Developer Portal | Required |
| `TEXT_CHANNEL_ID` | Channel ID where notifications are sent | Required |
| `VOICE_CHANNEL_ID` | Voice channel to auto-join (optional) | None |
| `COUGH_DETECTION_THRESHOLD` | Sensitivity of detection (0.0-1.0) | 0.5 |
| `VOLUME_THRESHOLD` | Minimum volume to trigger detection | 500 |

## Troubleshooting

### Bot doesn't detect coughs
- Try adjusting `VOLUME_THRESHOLD` in `.env` (lower = more sensitive)
- Ensure FFmpeg is properly installed
- Check that the bot has proper permissions in the voice channel

### Bot can't join voice channel
- Verify the bot has "Connect" and "Speak" permissions
- Check that `VOICE_CHANNEL_ID` is correct
- Ensure the voice channel isn't full or restricted

### Audio file doesn't play
- Verify `assets/stop_coughing.mp3` exists
- Check FFmpeg installation
- Ensure the bot has "Speak" permission

## Development

### Project Structure

```
jb-cough/
├── bot.py              # Main bot implementation
├── cough_detector.py   # Cough detection logic
├── config.py           # Configuration management
├── requirements.txt    # Python dependencies
├── .env.example        # Environment template
├── .gitignore         # Git ignore rules
├── assets/            # Audio files
│   └── README.md      # Asset documentation
└── README.md          # This file
```

### Testing

To test the cough detection:
1. Join a voice channel with the bot
2. Make a coughing sound or play a cough sound effect
3. Observe the bot's response in the text channel

## Notes

- The cough detection uses simple heuristics and may not be 100% accurate
- Audio quality and microphone settings affect detection accuracy
- The bot processes audio locally and does not store recordings
- Consider server load when deploying on multiple servers

## Privacy

This bot processes audio in real-time but does not record or store any voice data. All audio analysis happens in memory and is immediately discarded after processing.

## License

This project is provided as-is for educational and entertainment purposes.

## Contributing

Feel free to open issues or submit pull requests with improvements!

## Support

For issues or questions, please open an issue on GitHub.