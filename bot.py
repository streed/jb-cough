"""Main Discord bot file for cough detection."""
import discord
from discord.ext import commands
import asyncio
import time
import os
from typing import Optional

import config
from cough_detector import CoughDetector


class CoughDetectionBot(commands.Bot):
    """Discord bot that detects coughs in voice channels."""
    
    def __init__(self):
        """Initialize the bot with necessary intents."""
        intents = discord.Intents.default()
        intents.message_content = True
        intents.voice_states = True
        intents.guilds = True
        
        super().__init__(command_prefix=config.COMMAND_PREFIX, intents=intents)
        
        self.cough_detector = CoughDetector(
            volume_threshold=config.VOLUME_THRESHOLD
        )
        self.is_listening = False
        self.text_channel: Optional[discord.TextChannel] = None
        
    async def on_ready(self):
        """Called when the bot is ready."""
        print(f'{self.user} has connected to Discord!')
        print(f'Bot is in {len(self.guilds)} guild(s)')
        
        # Get the text channel for notifications
        if config.TEXT_CHANNEL_ID:
            self.text_channel = self.get_channel(config.TEXT_CHANNEL_ID)
            if self.text_channel:
                print(f'Text channel set to: {self.text_channel.name}')
            else:
                print(f'Warning: Could not find text channel with ID {config.TEXT_CHANNEL_ID}')
        
    async def on_voice_state_update(self, member, before, after):
        """Handle voice state changes."""
        # Auto-join voice channel if configured
        if (after.channel and after.channel.id == config.VOICE_CHANNEL_ID 
            and member != self.user and not self.voice_clients):
            await self.join_voice_channel(after.channel)
    
    async def join_voice_channel(self, channel: discord.VoiceChannel):
        """Join a voice channel and start listening."""
        try:
            voice_client = await channel.connect()
            print(f'Connected to voice channel: {channel.name}')
            
            # Start listening to audio
            await self.start_listening(voice_client)
            
        except Exception as e:
            print(f'Error joining voice channel: {e}')
    
    async def start_listening(self, voice_client: discord.VoiceClient):
        """Start listening to voice channel audio."""
        if self.is_listening:
            return
            
        self.is_listening = True
        print('Started listening for coughs...')
        
        # Create custom audio sink to process audio
        sink = CoughAudioSink(self, voice_client)
        
        # Note: discord.py v2.x uses a different API for receiving audio
        # This is a simplified version - actual implementation may need adjustments
        # based on discord.py version
        voice_client.listen(sink)
    
    async def on_cough_detected(self, user: discord.User):
        """Handle cough detection."""
        print(f'Cough detected from {user.name}!')
        
        # Send message to text channel
        if self.text_channel:
            try:
                await self.text_channel.send(
                    f'🤧 {user.mention} just coughed! Please mute yourself or cover your mouth!'
                )
            except Exception as e:
                print(f'Error sending message: {e}')
        
        # Play sound in voice channel
        for voice_client in self.voice_clients:
            if voice_client.is_connected():
                await self.play_cough_sound(voice_client)
                break
    
    async def play_cough_sound(self, voice_client: discord.VoiceClient):
        """Play a sound to interrupt the cougher."""
        if not os.path.exists(config.COUGH_SOUND_PATH):
            print(f'Warning: Sound file not found at {config.COUGH_SOUND_PATH}')
            return
            
        if voice_client.is_playing():
            voice_client.stop()
        
        try:
            audio_source = discord.FFmpegPCMAudio(config.COUGH_SOUND_PATH)
            voice_client.play(audio_source)
            print('Playing cough interruption sound')
        except Exception as e:
            print(f'Error playing sound: {e}')


class CoughAudioSink(discord.sinks.Sink):
    """Custom audio sink for processing voice data."""
    
    def __init__(self, bot: CoughDetectionBot, voice_client: discord.VoiceClient):
        """Initialize the audio sink."""
        super().__init__()
        self.bot = bot
        self.voice_client = voice_client
        self.user_audio_buffers = {}
    
    def write(self, data, user):
        """Process incoming audio data."""
        if user is None:
            return
            
        # Accumulate audio data
        if user not in self.user_audio_buffers:
            self.user_audio_buffers[user] = bytearray()
        
        self.user_audio_buffers[user].extend(data)
        
        # Process when we have enough data (e.g., 0.5 seconds at 48kHz, 16-bit stereo)
        buffer_size = 48000 * 2 * 2 * 0.5  # sample_rate * bytes_per_sample * channels * seconds
        
        if len(self.user_audio_buffers[user]) >= buffer_size:
            audio_data = bytes(self.user_audio_buffers[user])
            self.user_audio_buffers[user].clear()
            
            # Analyze audio for cough
            if self.bot.cough_detector.analyze_audio(audio_data):
                current_time = time.time()
                if self.bot.cough_detector.should_trigger(current_time):
                    # Schedule cough detection handler
                    asyncio.create_task(self.bot.on_cough_detected(user))
    
    def cleanup(self):
        """Clean up the sink."""
        self.user_audio_buffers.clear()


def main():
    """Main entry point for the bot."""
    if not config.DISCORD_TOKEN:
        print('Error: DISCORD_TOKEN not set in environment variables')
        print('Please create a .env file based on .env.example')
        return
    
    bot = CoughDetectionBot()
    
    @bot.command(name='join')
    async def join(ctx):
        """Join the voice channel."""
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            await bot.join_voice_channel(channel)
            await ctx.send(f'Joined {channel.name}!')
        else:
            await ctx.send('You need to be in a voice channel!')
    
    @bot.command(name='leave')
    async def leave(ctx):
        """Leave the voice channel."""
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            bot.is_listening = False
            await ctx.send('Left the voice channel!')
        else:
            await ctx.send('Not in a voice channel!')
    
    @bot.command(name='status')
    async def status(ctx):
        """Check bot status."""
        status_msg = f'Bot Status:\n'
        status_msg += f'Connected: {"Yes" if bot.voice_clients else "No"}\n'
        status_msg += f'Listening: {"Yes" if bot.is_listening else "No"}\n'
        status_msg += f'Text Channel: {bot.text_channel.name if bot.text_channel else "Not set"}'
        await ctx.send(status_msg)
    
    try:
        bot.run(config.DISCORD_TOKEN)
    except Exception as e:
        print(f'Error running bot: {e}')


if __name__ == '__main__':
    main()
