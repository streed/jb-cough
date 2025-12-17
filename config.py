"""Configuration module for the Discord cough detection bot."""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Discord Configuration
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
TEXT_CHANNEL_ID = int(os.getenv('TEXT_CHANNEL_ID', 0))
VOICE_CHANNEL_ID = int(os.getenv('VOICE_CHANNEL_ID', 0))

# Cough Detection Settings
COUGH_DETECTION_THRESHOLD = float(os.getenv('COUGH_DETECTION_THRESHOLD', 0.5))
VOLUME_THRESHOLD = int(os.getenv('VOLUME_THRESHOLD', 500))

# Bot Settings
COMMAND_PREFIX = '!'
COUGH_SOUND_PATH = 'assets/stop_coughing.mp3'
