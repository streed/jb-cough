"""Configuration module for the Discord cough detection bot."""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Discord Configuration
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

# Convert channel IDs to int, handling empty strings
def _get_channel_id(env_var: str) -> int:
    """Get channel ID from environment variable."""
    value = os.getenv(env_var, '0')
    try:
        return int(value) if value else 0
    except ValueError:
        print(f"Warning: Invalid {env_var} value '{value}', using 0")
        return 0

TEXT_CHANNEL_ID = _get_channel_id('TEXT_CHANNEL_ID')
VOICE_CHANNEL_ID = _get_channel_id('VOICE_CHANNEL_ID')

# Cough Detection Settings
COUGH_DETECTION_THRESHOLD = float(os.getenv('COUGH_DETECTION_THRESHOLD', 0.5))
VOLUME_THRESHOLD = int(os.getenv('VOLUME_THRESHOLD', 500))

# Bot Settings
COMMAND_PREFIX = '!'
COUGH_SOUND_PATH = 'assets/stop_coughing.mp3'
