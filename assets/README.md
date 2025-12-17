# Assets Directory

## Audio Files

Place your audio file here to play when a cough is detected.

### Required File
- `stop_coughing.mp3` - Audio file that plays when someone coughs

You can use any short audio clip (e.g., a polite reminder sound, a beep, or a recorded message).

### Generating a Sound File

If you don't have an audio file, you can:
1. Record a short message saying "Please mute yourself"
2. Use text-to-speech to generate an MP3
3. Download a free sound effect from sites like freesound.org
4. Use ffmpeg to create a simple beep:
   ```bash
   ffmpeg -f lavfi -i "sine=frequency=1000:duration=0.5" -af "volume=0.5" stop_coughing.mp3
   ```

The bot will automatically play this sound in the voice channel when a cough is detected.
