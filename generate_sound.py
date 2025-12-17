"""Generate a simple audio file for the cough interruption sound."""
import subprocess
import os
import sys


def generate_beep_sound():
    """Generate a simple beep sound using FFmpeg."""
    output_path = 'assets/stop_coughing.mp3'
    
    # Check if FFmpeg is available
    try:
        subprocess.run(['ffmpeg', '-version'], 
                      capture_output=True, 
                      check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Error: FFmpeg is not installed or not in PATH")
        print("Please install FFmpeg first:")
        print("  Ubuntu/Debian: sudo apt install ffmpeg")
        print("  macOS: brew install ffmpeg")
        print("  Windows: Download from https://ffmpeg.org/download.html")
        return False
    
    # Create assets directory if it doesn't exist
    os.makedirs('assets', exist_ok=True)
    
    # Generate a polite beep sound (two tones)
    print(f"Generating audio file: {output_path}")
    
    try:
        # Create a two-tone beep that sounds like a polite notification
        subprocess.run([
            'ffmpeg', '-y',
            '-f', 'lavfi',
            '-i', 'sine=frequency=800:duration=0.15',
            '-f', 'lavfi',
            '-i', 'sine=frequency=600:duration=0.15',
            '-filter_complex', '[0:a][1:a]concat=n=2:v=0:a=1,volume=0.3',
            output_path
        ], check=True, capture_output=True)
        
        print(f"✓ Successfully generated {output_path}")
        print(f"  File size: {os.path.getsize(output_path)} bytes")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"Error generating audio file: {e}")
        if e.stderr:
            print(e.stderr.decode())
        return False


def main():
    """Main entry point."""
    print("Audio File Generator for Discord Cough Bot")
    print("=" * 50)
    
    if os.path.exists('assets/stop_coughing.mp3'):
        response = input("Audio file already exists. Overwrite? (y/N): ")
        if response.lower() != 'y':
            print("Keeping existing file.")
            return 0
    
    if generate_beep_sound():
        print("\nThe audio file has been generated successfully!")
        print("You can now run the bot with: python bot.py")
        return 0
    else:
        print("\nFailed to generate audio file.")
        print("You can still run the bot, but it won't play sounds.")
        return 1


if __name__ == '__main__':
    sys.exit(main())
