# Development Notes

## Audio Receiving Limitations

### Discord.py Audio Receiving

As of discord.py v2.x, receiving audio from voice channels has some limitations:

1. **Voice Receiving is Limited**: Discord.py's audio receiving capabilities are experimental and may not work perfectly in all scenarios.

2. **Requires PyNaCl**: Audio encryption/decryption requires the PyNaCl library (included in requirements.txt).

3. **Bot Permissions**: The bot needs specific permissions:
   - Connect (to join voice channels)
   - Speak (to play audio)
   - Use Voice Activity (to receive audio)

### Alternative Approaches

If the built-in audio receiving doesn't work well, consider these alternatives:

1. **Discord Voice Gateway**: Use a lower-level implementation with discord.py's voice gateway
2. **discord.py-self**: A fork that may have better voice receiving support (use cautiously)
3. **External Audio Processing**: Record audio externally and process it
4. **Bot Commands**: Allow users to manually trigger the bot instead of automatic detection

### Current Implementation

The current implementation uses:
- `discord.sinks.Sink` for audio processing
- Real-time audio buffer analysis
- Simple heuristic cough detection based on volume spikes

### Testing Tips

To test the bot effectively:
1. Enable debug logging to see what audio data is being received
2. Test with different microphone qualities and volumes
3. Adjust `VOLUME_THRESHOLD` in config based on your environment
4. Consider the background noise in your voice channel

### Known Issues

- Audio receiving may not work in all Discord environments
- Detection accuracy depends on microphone quality and settings
- Some Discord voice channels may not support bot audio receiving

### Future Improvements

Potential enhancements for better cough detection:
1. Use machine learning models (e.g., audio classification)
2. Implement frequency analysis (coughs have specific frequency patterns)
3. Add user-specific calibration
4. Implement better noise filtering
5. Add support for multiple languages/regions in notifications

## Audio Processing Details

### Cough Characteristics

Coughs typically have these audio characteristics:
- **Duration**: 0.2-0.6 seconds
- **Frequency Range**: 100-8000 Hz with peaks around 500-2000 Hz
- **Volume Pattern**: Sudden onset with sharp peak
- **Energy**: High peak-to-RMS ratio (>3.0)

### Detection Algorithm

The current implementation uses:
1. **RMS Calculation**: Root Mean Square for average volume
2. **Peak Detection**: Maximum amplitude in the audio buffer
3. **Ratio Analysis**: Peak-to-RMS ratio to identify sudden bursts
4. **Threshold Comparison**: Both RMS and ratio must exceed thresholds

### Tuning Parameters

Adjust these in `.env` for better detection:
- `VOLUME_THRESHOLD`: Lower = more sensitive (try 200-800)
- `COUGH_DETECTION_THRESHOLD`: Currently unused, reserved for ML models
- Buffer size: Adjust in `CoughAudioSink.write()` (default: 0.5 seconds)
- Cooldown period: Adjust in `CoughDetector.__init__()` (default: 3 seconds)

## Security Considerations

### Privacy

- No audio data is stored or transmitted outside the bot
- All processing happens in memory and is discarded immediately
- Consider informing users that audio is being processed

### Bot Token Security

- **Never commit your `.env` file** to version control
- Use environment variables in production
- Rotate your token if it's ever exposed
- Limit bot permissions to only what's needed

### Rate Limiting

- Discord has rate limits for API calls
- The cooldown system prevents spam
- Consider implementing per-guild cooldowns for multi-server bots

## Deployment

### Running in Production

For production deployment:

1. **Use a Process Manager**:
   ```bash
   # Using systemd
   sudo systemctl enable cough-bot.service
   sudo systemctl start cough-bot.service
   ```

2. **Use Environment Variables**:
   - Don't rely on `.env` files in production
   - Use system environment variables or secrets management

3. **Add Logging**:
   - Implement proper logging to files
   - Monitor for errors and unusual activity

4. **Consider Docker**:
   - Package the bot in a Docker container
   - Use docker-compose for easier deployment

### Hosting Options

- **Self-hosted**: Run on your own server (VPS, Raspberry Pi, etc.)
- **Cloud**: AWS, Google Cloud, Azure, DigitalOcean
- **Bot Hosting**: Specialized Discord bot hosting services
- **Repl.it**: Free tier for testing (limited uptime)

### Performance

- CPU Usage: Low (mainly during audio processing)
- Memory: ~50-100MB typical
- Network: Depends on voice channel activity
- Disk: Minimal (no storage needed)

## Contributing

### Code Style

- Follow PEP 8 for Python code
- Use type hints where possible
- Add docstrings to all functions and classes
- Keep functions small and focused

### Testing

Before submitting a PR:
1. Test the bot in a real Discord server
2. Verify all commands work
3. Check error handling
4. Test with different configurations

### Pull Request Guidelines

- Describe what your change does
- Explain why it's needed
- Include any relevant issue numbers
- Add tests if applicable
- Update documentation if needed
